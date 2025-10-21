# MLA V3 安装指南

本地安装 MLA Agent 系统为 Python 包。

---

## 安装步骤

### 1. 进入项目目录

```bash
cd /Users/chenglin/Desktop/research/agent_framwork/vscode_version/MLA_V3
```

### 2. 本地安装

**方式 1: 开发模式**（推荐，代码修改立即生效）

```bash
pip install -e .
```

**方式 2: 正式安装**

```bash
pip install .
```

### 3. 验证安装

```bash
mla-agent --help
mla-tool-server --help
```

---

## 配置 API Key

### 方法 1: 命令行设置（推荐）

```bash
# 查看当前配置 默认了 openrouter 为 baseurl
mla-agent --config-show

# 设置 API Key
mla-agent --config-set api_key "sk-your-api-key-here"

# 设置 Base URL（可选）
mla-agent --config-set base_url "https://api.openai.com/v1"

# 设置模型列表（可选）(第一个前缀取决于你的 base_url提供的响应格式，如果是 openai格式则使用 openai 前缀，然后再写入模型名称)
mla-agent --config-set models "["openai/anthropic/claude-haiku-4.5"]"

```

### 方法 2: 直接编辑配置文件

```bash
# 找到配置文件位置
mla-agent --config-show

# 会显示类似：
# 📋 配置文件: /usr/local/lib/python3.12/site-packages/config/run_env_config/llm_config.yaml

# 使用编辑器修改
nano /path/to/llm_config.yaml
```

---

## 使用

### 启动工具服务器

```bash
# 前台运行
mla-tool-server

# 后台运行
mla-tool-server &

# 指定端口
mla-tool-server --port 8002
```

### 运行 Agent

```bash
# 普通模式
mla-agent \
  --task_id /absolute/path/to/workspace \
  --user_input "写一篇关于AI的文章"

# JSONL 模式（VS Code 插件）
mla-agent \
  --task_id /path \
  --user_input "任务" \
  --agent_name writing_agent \
  --jsonl
```

---

## 卸载

```bash
pip uninstall mla-agent
```

---

## 本地开发

如果需要修改代码：

```bash
# 1. 使用开发模式安装
pip install -e .

# 2. 修改代码
# 代码修改会立即生效，无需重新安装

# 3. 测试
mla-agent --test

# 4. 重新安装（如果修改了 setup.py）
pip install -e . --force-reinstall
```

---

## 配置文件位置

安装后，配置文件位于包内：

```
site-packages/
└── MLA_V3/  (或包名目录)
    ├── config/
    │   ├── agent_library/
    │   └── run_env_config/
    │       ├── llm_config.yaml      ← 可编辑
    │       ├── tool_config.yaml
    │       └── document_convert_api.yaml
    ├── start.py
    ├── core/
    ├── services/
    └── tool_server_lite/
```

**查找路径**:
```bash
python3 -c "import MLA_V3; print(MLA_V3.__file__)"
```

---

## 常见问题

### Q: API Key 在哪里设置？
A: `mla-agent --config-set api_key "YOUR_KEY"`

### Q: 如何更换模型？
A: `mla-agent --config-set models "[model1,model2]"`

### Q: 工具服务器端口被占用？
A: `mla-tool-server --port 8002`

### Q: 如何卸载？
A: `pip uninstall mla-agent`

---

## 完整示例

```bash
# 1. 安装
cd /path/to/MLA_V3
pip install -e .

# 2. 配置
mla-agent --config-set api_key "sk-xxx"

# 3. 启动工具服务器
mla-tool-server &

# 4. 运行
mla-agent --task_id /Users/xxx/my_project --user_input "写代码" --jsonl
```

**安装完成！可以在任何地方使用 `mla-agent` 命令。**

