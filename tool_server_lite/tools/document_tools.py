#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
文档处理工具
"""

from pathlib import Path
from typing import Dict, Any
from .file_tools import BaseTool, get_abs_path


class ParseDocumentTool(BaseTool):
    """PDF/文档解析工具"""
    
    def execute(self, task_id: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        解析PDF或其他文档
        
        Parameters:
            path (str): 文档相对路径
            save_path (str, optional): 保存解析结果的相对路径
        """
        try:
            path = parameters.get("path")
            save_path = parameters.get("save_path")
            
            abs_path = get_abs_path(task_id, path)
            
            if not abs_path.exists():
                return {
                    "status": "error",
                    "output": "",
                    "error": f"Document not found: {path}"
                }
            
            # 判断文件类型
            suffix = abs_path.suffix.lower()
            
            if suffix == '.pdf':
                content = self._parse_pdf(abs_path)
            elif suffix in ['.docx', '.doc']:
                content = self._parse_word(abs_path)
            elif suffix in ['.txt', '.md']:
                with open(abs_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            else:
                return {
                    "status": "error",
                    "output": "",
                    "error": f"Unsupported document type: {suffix}"
                }
            
            # 保存解析结果
            if save_path:
                abs_save_path = get_abs_path(task_id, save_path)
                abs_save_path.parent.mkdir(parents=True, exist_ok=True)
                with open(abs_save_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                output = f"结果保存在 {save_path}"
            else:
                output = content
            
            return {
                "status": "success",
                "output": output,
                "error": ""
            }
            
        except Exception as e:
            return {
                "status": "error",
                "output": "",
                "error": str(e)
            }
    
    def _parse_pdf(self, pdf_path: Path) -> str:
        """解析PDF文件 - 使用 pdfplumber（质量更高）"""
        try:
            import pdfplumber
            
            text_content = []
            with pdfplumber.open(pdf_path) as pdf:
                num_pages = len(pdf.pages)
                
                for page_num, page in enumerate(pdf.pages, 1):
                    # 提取文本
                    text = page.extract_text() or ""
                    
                    # 提取表格
                    tables = page.extract_tables()
                    
                    page_content = f"--- Page {page_num}/{num_pages} ---\n{text}\n"
                    
                    # 如果有表格，添加表格内容
                    if tables:
                        page_content += f"\n[Tables found: {len(tables)}]\n"
                        for table_idx, table in enumerate(tables, 1):
                            page_content += f"\n--- Table {table_idx} ---\n"
                            for row in table:
                                page_content += " | ".join([str(cell or "") for cell in row]) + "\n"
                    
                    text_content.append(page_content)
            
            return '\n'.join(text_content)
            
        except ImportError:
            raise Exception("pdfplumber not installed. Run: pip install pdfplumber")
        except Exception as e:
            raise Exception(f"PDF parsing error: {str(e)}")
    
    def _parse_word(self, doc_path: Path) -> str:
        """解析Word文档"""
        try:
            import docx
            
            doc = docx.Document(doc_path)
            paragraphs = [p.text for p in doc.paragraphs]
            return '\n'.join(paragraphs)
            
        except ImportError:
            raise Exception("python-docx not installed. Run: pip install python-docx")
        except Exception as e:
            raise Exception(f"Word document parsing error: {str(e)}")

