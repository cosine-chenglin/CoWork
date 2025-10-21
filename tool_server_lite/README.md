# Tool Server Lite - API 文档

轻量化工具服务器，为 MLA V3 Agent 框架提供核心工具支持。

**版本**: 1.0.0  
**端口**: 8001  
**工具数量**: 18

## 快速开始

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务器
python3 server.py --host 0.0.0.0 --port 8001
```

访问 API 文档：http://localhost:8001/docs

---

## 核心概念

### task_id（工作空间）
- **类型**: 绝对路径字符串
- **作用**: 指向工作目录，所有相对路径都基于此路径
- **示例**: `/Users/xxx/workspace/project1`

### 路径转换规则
```
task_id: /Users/xxx/workspace/project1
相对路径: data/file.txt
实际路径: /Users/xxx/workspace/project1/data/file.txt
```

### 统一返回格式
```json
{
  "success": true/false,
  "data": {
    "status": "success/error",
    "output": "操作结果",
    "error": "错误信息"
  }
}
```

---

## 基础 API 端点

### 服务器信息

#### `GET /`
获取服务器基本信息和可用工具列表

**响应**:
```json
{
  "message": "Tool Server Lite is running",
  "version": "1.0.0",
  "tools": ["file_read", "file_write", ...]
}
```

#### `GET /health`
健康检查

#### `GET /api/tools`
获取所有工具列表

---

### 任务管理

#### `GET /api/task/{task_id}/status`
检查任务状态

**示例**:
```bash
curl "http://localhost:8001/api/task/%2Fpath%2Fto%2Fworkspace/status"
```

#### `POST /api/task/create`
创建任务工作空间

**请求参数**（Query Params）:
- `task_id` (str, 必需): 绝对路径
- `task_name` (str, 可选): 任务名称

**示例**:
```bash
curl -X POST "http://localhost:8001/api/task/create?task_id=/path/to/workspace&task_name=MyTask"
```

**功能**:
- 创建工作目录
- 自动创建子目录: `upload/`, `code_run/`, `code_env/`

---

## 工具执行 API

### 统一调用格式

```bash
POST /api/tool/execute
Content-Type: application/json

{
  "task_id": "/absolute/path/to/workspace",
  "tool_name": "工具名称",
  "params": {
    参数字典
  }
}
```

**返回格式**:
```json
{
  "success": true,
  "data": {
    "status": "success",
    "output": "结果",
    "error": ""
  }
}
```

---

## 工具详细说明

### 📁 文件操作（6个）

#### 1. file_read

**描述**: 读取文件内容，支持行范围、自动编码检测

**参数**:
- `path` (str, 必需): 文件相对路径
- `start_line` (int, 可选): 起始行号（从1开始）
- `end_line` (int, 可选): 结束行号
- `encoding` (str, 可选): 文件编码

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -H "Content-Type: application/json" \
  -d '{
    "task_id": "/path/to/workspace",
    "tool_name": "file_read",
    "params": {
      "path": "data/file.txt",
      "start_line": 1,
      "end_line": 10
    }
  }'
```

---

#### 2. file_write

**描述**: 写入文件，支持覆盖/追加/行替换

**参数**:
- `path` (str, 必需): 文件相对路径
- `content` (str, 必需): 文件内容
- `mode` (str, 可选): 写入模式 `"write"`(默认) / `"append"`
- `start_line` (int, 可选): 行替换-起始行
- `end_line` (int, 可选): 行替换-结束行

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "file_write",
    "params": {
      "path": "test.txt",
      "content": "Hello World"
    }
  }'
```

---

#### 3. dir_list

**描述**: 列出目录内容，支持递归

**参数**:
- `path` (str, 可选): 相对路径，默认 `"."`
- `recursive` (bool, 可选): 是否递归，默认 `false`

**注意**: 递归时自动排除 `code_env/` 目录

---

#### 4. dir_create

**描述**: 创建目录（自动创建父目录）

**参数**:
- `path` (str, 必需): 目录相对路径

---

#### 5. file_move

**描述**: 移动或复制文件/目录

**参数**:
- `source` (str, 必需): 源文件相对路径
- `destination` (str, 必需): 目标相对路径
- `copy` (bool, 可选): 是否复制（保留原文件），默认 `false`

---

#### 6. file_delete

**描述**: 删除文件或目录

**参数**:
- `path` (str, 必需): 相对路径

---

### 🌐 网络工具（5个）

#### 7. web_search

**描述**: DuckDuckGo 搜索（免费、稳定）

**参数**:
- `query` (str, 必需): 搜索关键词
- `max_results` (int, 可选): 最大结果数，默认 `10`
- `save_path` (str, 可选): 保存路径（.md）

**输出**:
- 有 `save_path`: `"结果保存在 upload/xxx_查询词_nN.md"`
- 无 `save_path`: 完整搜索结果

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "web_search",
    "params": {
      "query": "FastAPI tutorial",
      "max_results": 5,
      "save_path": "upload/search.md"
    }
  }'
```

---

#### 8. google_scholar_search

**描述**: 谷歌学术搜索，使用 crawl4ai 爬取

**参数**:
- `query` (str, 必需): 搜索关键词
- `year_low` (int, 可选): 年份下限
- `year_high` (int, 可选): 年份上限
- `pages` (int, 可选): 爬取页数，默认 `1`
- `save_path` (str, 可选): 保存路径（.md）

**文件名**: `{原名}_{查询词}_y{下限}-{上限}_p{页数}.md`

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "google_scholar_search",
    "params": {
      "query": "machine learning",
      "year_low": 2020,
      "year_high": 2024,
      "pages": 2,
      "save_path": "upload/scholar.md"
    }
  }'
```

---

#### 9. arxiv_search

**描述**: arXiv 论文搜索（官方 API）

**参数**:
- `query` (str, 必需): 搜索关键词
- `max_results` (int, 可选): 最大结果数，默认 `10`
- `sort_by` (str, 可选): 排序方式，默认 `"relevance"`
  - `"relevance"`: 相关性
  - `"lastUpdatedDate"`: 更新时间
  - `"submittedDate"`: 提交时间
- `sort_order` (str, 可选): 排序顺序，默认 `"descending"`
  - `"descending"`: 降序
  - `"ascending"`: 升序
- `save_path` (str, 可选): 保存路径（.md）

**输出内容**:
- 标题、作者、发布日期、arXiv ID
- **PDF 下载地址**
- 分类、摘要

**文件名**: `{原名}_{查询词}_n{结果数}.md`

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "arxiv_search",
    "params": {
      "query": "transformer neural network",
      "max_results": 5,
      "sort_by": "submittedDate",
      "save_path": "upload/arxiv.md"
    }
  }'
```

---

#### 10. crawl_page

**描述**: 网页爬取，转换为 Markdown

**参数**:
- `url` (str, 必需): 网页URL
- `save_path` (str, 可选): 保存路径（.md）
- `download_images` (bool, 可选): 是否下载图片，默认 `false`

---

#### 11. file_download

**描述**: 从URL下载文件

**参数**:
- `url` (str, 必需): 文件URL
- `save_path` (str, 必需): 保存的相对路径

**输出**: `"Downloaded to xxx (N MB)"`

---

### 📄 文档处理（3个）

#### 12. parse_document

**描述**: 解析 PDF/Word 文档（使用 pdfplumber 高质量提取）

**参数**:
- `path` (str, 必需): 文档相对路径
- `save_path` (str, 可选): 保存解析结果路径

**支持格式**:
- PDF (.pdf) - pdfplumber（提取文本+表格）
- Word (.docx, .doc) - python-docx
- 文本 (.txt, .md)

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "parse_document",
    "params": {
      "path": "upload/paper.pdf",
      "save_path": "upload/parsed.txt"
    }
  }'
```

---

#### 13. md_to_pdf

**描述**: Markdown 转 PDF（支持数学公式和表格）

**参数**:
- `source_path` (str, 必需): Markdown 文件相对路径
- `output_path` (str, 可选): 输出 PDF 路径，默认与源文件同名
- `engine` (str, 可选): PDF 引擎，默认 `"xelatex"`
  - `"pdflatex"`: 英文文档
  - `"xelatex"`: 中文文档（推荐）
  - `"lualatex"`: 现代引擎

**配置**: 从 `config/run_env_config/document_convert_api.yaml` 读取 API 地址

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "md_to_pdf",
    "params": {
      "source_path": "upload/document.md",
      "output_path": "upload/document.pdf",
      "engine": "xelatex"
    }
  }'
```

---

#### 14. md_to_docx

**描述**: Markdown 转 Word

**参数**:
- `source_path` (str, 必需): Markdown 文件相对路径
- `output_path` (str, 可选): 输出 DOCX 路径

**配置**: 从 `config/run_env_config/document_convert_api.yaml` 读取 API 地址

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "md_to_docx",
    "params": {
      "source_path": "upload/document.md",
      "output_path": "upload/document.docx"
    }
  }'
```

---

### 👤 人类交互（1个）

#### 15. human_in_loop

**描述**: 挂起等待人类完成任务（异步，不阻塞服务器）

**参数**:
- `hil_id` (str, 必需): 人类任务唯一ID
- `instruction` (str, 必需): 给人类的指令
- `timeout` (int, 可选): 超时时间（秒），默认 `None`（无限等待）

**输出**: `"人类任务已完成: {结果}"`

**工作流程**:
1. 调用 `human_in_loop` → 挂起等待
2. 查看任务: `GET /api/hil/{hil_id}`
3. 完成任务: `POST /api/hil/complete/{hil_id}`
4. 步骤1的请求返回成功

**示例**:
```bash
# 1. 启动 HIL 任务（后台）
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "human_in_loop",
    "params": {
      "hil_id": "task_001",
      "instruction": "请上传文件到 upload 目录"
    }
  }' &

# 2. 查看 HIL 任务状态
curl http://localhost:8001/api/hil/task_001

# 3. 完成 HIL 任务
curl -X POST http://localhost:8001/api/hil/complete/task_001 \
  -H "Content-Type: application/json" \
  -d '{"result": "文件已上传"}'
```

**HIL 管理端点**:
- `GET /api/hil/tasks` - 列出所有 HIL 任务
- `GET /api/hil/{hil_id}` - 查看任务状态
- `POST /api/hil/complete/{hil_id}` - 完成任务

---

### 💻 代码执行（3个）

#### 16. execute_code

**描述**: 执行 Python/Bash 代码，支持虚拟环境

**参数**:
- `language` (str, 必需): `"python"` 或 `"bash"`
- `code` (str, 可选): 代码内容
- `file_path` (str, 可选): 代码文件相对路径
- `working_dir` (str, 可选): 执行目录，默认 `"code_run"`
- `use_venv` (bool, 可选): 使用虚拟环境，默认 `true`
- `timeout` (int, 可选): 超时时间（秒），默认 `30`

**输出**: 标准输出 + 标准错误 + 退出码

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "execute_code",
    "params": {
      "language": "python",
      "file_path": "code_run/script.py",
      "working_dir": "code_run"
    }
  }'
```

---

#### 17. pip_install

**描述**: 在虚拟环境中安装 Python 包

**参数**:
- `packages` (list[str] 或 str, 必需): 包名列表或单个包名
- `timeout` (int, 可选): 超时时间（秒），默认 `300`

**输出**: 每个包的安装结果（✅ 成功 / ❌ 失败）

**虚拟环境**: `{task_id}/code_env/venv/`

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "pip_install",
    "params": {
      "packages": ["numpy", "pandas", "matplotlib"]
    }
  }'
```

---

#### 18. execute_command

**描述**: 执行命令行命令

**参数**:
- `command` (str, 必需): 要执行的命令
- `working_dir` (str, 可选): 工作目录，默认 `"."`
- `timeout` (int, 可选): 超时时间（秒），默认 `30`

**输出**: 标准输出 + 标准错误 + 退出码

**示例**:
```bash
curl -X POST http://localhost:8001/api/tool/execute \
  -d '{
    "task_id": "/path",
    "tool_name": "execute_command",
    "params": {
      "command": "ls -la",
      "working_dir": "upload"
    }
  }'
```

---

## 完整工具列表

| # | 工具名 | 分类 | 描述 |
|---|--------|------|------|
| 1 | `file_read` | 文件 | 读取文件（行范围、编码检测） |
| 2 | `file_write` | 文件 | 写入文件（覆盖/追加/行替换） |
| 3 | `dir_list` | 文件 | 列出目录（递归，排除code_env） |
| 4 | `dir_create` | 文件 | 创建目录 |
| 5 | `file_move` | 文件 | 移动/复制文件 |
| 6 | `file_delete` | 文件 | 删除文件/目录 |
| 7 | `web_search` | 网络 | DuckDuckGo 搜索 |
| 8 | `google_scholar_search` | 网络 | 谷歌学术（年份筛选、分页） |
| 9 | `arxiv_search` | 网络 | arXiv 搜索（PDF地址、摘要） |
| 10 | `crawl_page` | 网络 | 网页爬取（转Markdown） |
| 11 | `file_download` | 网络 | URL 文件下载 |
| 12 | `parse_document` | 文档 | PDF/Word 解析（pdfplumber） |
| 13 | `md_to_pdf` | 文档 | Markdown 转 PDF（支持公式） |
| 14 | `md_to_docx` | 文档 | Markdown 转 Word |
| 15 | `human_in_loop` | 交互 | 人类任务等待（异步挂起） |
| 16 | `execute_code` | 代码 | 执行Python/Bash（虚拟环境） |
| 17 | `pip_install` | 代码 | 安装Python包 |
| 18 | `execute_command` | 代码 | 执行命令行 |

---

## Python 调用示例

```python
import requests

BASE_URL = "http://localhost:8001"

def call_tool(task_id, tool_name, params):
    """调用工具的通用函数"""
    response = requests.post(
        f"{BASE_URL}/api/tool/execute",
        json={
            "task_id": task_id,
            "tool_name": tool_name,
            "params": params
        }
    )
    return response.json()

# 示例1: 创建任务
task_id = "/Users/xxx/workspace/project1"
requests.post(
    f"{BASE_URL}/api/task/create",
    params={"task_id": task_id}
)

# 示例2: 搜索 arXiv
result = call_tool(task_id, "arxiv_search", {
    "query": "transformer",
    "max_results": 5,
    "save_path": "upload/arxiv.md"
})
print(result["data"]["output"])

# 示例3: 解析 PDF
result = call_tool(task_id, "parse_document", {
    "path": "upload/paper.pdf",
    "save_path": "upload/parsed.txt"
})

# 示例4: 执行代码
result = call_tool(task_id, "execute_code", {
    "language": "python",
    "file_path": "code_run/script.py"
})

# 示例5: 人类交互
import threading

def wait_human_task():
    result = call_tool(task_id, "human_in_loop", {
        "hil_id": "task_123",
        "instruction": "请上传文件"
    })
    print(result)

# 后台等待
threading.Thread(target=wait_human_task).start()

# 完成任务
requests.post(
    f"{BASE_URL}/api/hil/complete/task_123",
    json={"result": "已上传"}
)
```

---

## 配置文件

### document_convert_api.yaml
位置: `MLA_V3/config/run_env_config/document_convert_api.yaml`

```yaml
api_server: "http://192.168.31.4:8000/"
```

**用途**: `md_to_pdf` 和 `md_to_docx` 工具读取此配置调用转换服务

---

## 技术栈

| 库 | 用途 |
|----|------|
| FastAPI | Web 框架 |
| uvicorn | ASGI 服务器 |
| crawl4ai | 网页爬取（智能转Markdown） |
| ddgs | DuckDuckGo 搜索 |
| arxiv | arXiv 官方 API |
| pdfplumber | PDF 解析（高质量） |
| python-docx | Word 文档处理 |
| chardet | 文件编码检测 |
| pyyaml | 配置文件读取 |

---

## 与原 Tool Server 对比

| 特性 | 原 Tool Server | Tool Server Lite |
|------|----------------|------------------|
| **部署** | 需要 Docker | 直接运行 |
| **工具数** | 30+ | 18（核心功能） |
| **task_id** | 简单ID | 绝对路径 |
| **输出** | 详细信息+时间戳 | 精炼核心结果 |
| **PDF解析** | PyPDF2 | pdfplumber（更好） |
| **搜索** | Google（易封禁） | DuckDuckGo（稳定） |
| **arXiv** | 不支持 | 官方API ✓ |
| **文档转换** | PDF编译 | Markdown转换 ✓ |
| **人类交互** | 支持 | 异步挂起 ✓ |
| **API兼容** | 旧版格式 | 新旧双兼容 ✓ |

---

## 依赖安装

```bash
pip install -r requirements.txt
```

---

## 注意事项

1. **crawl4ai 首次运行**: 会自动下载 Chromium
2. **虚拟环境位置**: `{task_id}/code_env/venv/`，每个任务独立
3. **code_env 隐藏**: `dir_list` 递归时自动排除
4. **文档转换**: 需要 Pandoc API 服务可访问
5. **默认执行目录**: `execute_code` 默认在 `code_run/` 执行
6. **HIL 异步**: 人类交互不阻塞其他请求

---

## API 兼容性

### 旧版 API（兼容 tool_executor.py）

```bash
POST /api/tool/execute
{
  "task_id": "/path",
  "tool_name": "file_read",
  "params": {"path": "test.txt"}
}
```

### 新版 API

```bash
POST /api/execute/file_read
{
  "task_id": "/path",
  "parameters": {"path": "test.txt"}
}
```

**两种格式均支持！**

---

## 故障排查

### 问题: 虚拟环境创建失败
```bash
# Ubuntu/Debian
sudo apt install python3-venv
```

### 问题: crawl4ai 无法爬取
- 检查网络连接
- 等待 Chromium 首次下载完成

### 问题: PDF 转换失败
- 检查 `document_convert_api.yaml` 配置
- 确保转换服务 (http://192.168.31.4:8000) 可访问

### 问题: arXiv 搜索慢
- arXiv API 有速率限制，大量搜索时会变慢
- 建议设置合理的 `max_results`

### 问题: HIL 任务无响应
- 检查 `hil_id` 是否正确
- 使用 `GET /api/hil/tasks` 查看所有任务
- 确保调用了 `POST /api/hil/complete/{hil_id}`

---

## 开发指南

### 添加新工具

1. 在 `tools/` 下创建工具类
2. 继承 `BaseTool`，实现 `execute()` 或 `execute_async()`
3. 在 `tools/__init__.py` 导出
4. 在 `server.py` 的 `TOOLS` 注册

**模板**:
```python
class NewTool(BaseTool):
    def execute(self, task_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        try:
            # 参数获取
            param = parameters.get("param_name")
            
            # 处理逻辑
            result = do_something(param)
            
            return {
                "status": "success",
                "output": result,
                "error": ""
            }
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e)
            }
```

---

## 使用场景

### 场景1: 学术研究
```bash
# 1. 创建工作空间
POST /api/task/create

# 2. 搜索 arXiv 论文
tool_name: arxiv_search

# 3. 下载 PDF
tool_name: file_download

# 4. 解析 PDF
tool_name: parse_document

# 5. 转换为报告
tool_name: md_to_pdf
```

### 场景2: 自动化脚本
```bash
# 1. 写入代码
tool_name: file_write

# 2. 安装依赖
tool_name: pip_install

# 3. 执行代码
tool_name: execute_code
```

### 场景3: 人类协作
```bash
# 1. 自动收集数据
tool_name: web_search

# 2. 请求人类确认
tool_name: human_in_loop

# 3. 继续处理
...
```

---

## 🎉 项目完成

✅ 18 个核心工具  
✅ 新旧 API 双兼容  
✅ 异步 HIL 不阻塞  
✅ 完整测试验证  
✅ 文档齐全  

**Tool Server Lite 已完成，可投入使用！**
