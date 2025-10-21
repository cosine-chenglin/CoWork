#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置加载器 - 读取agent_library中的配置文件
"""

import os
import yaml
from typing import Dict, List, Any
from pathlib import Path


class ConfigLoader:
    """配置加载器，负责读取和合并agent配置"""
    
    def __init__(self, agent_system_name: str = "infiHelper"):
        """
        初始化配置加载器
        
        Args:
            agent_system_name: Agent系统名称，对应agent_library下的文件夹
        """
        self.agent_system_name = agent_system_name
        
        # 查找配置目录（支持MLA_V3和原Multi-Level-Agent）
        self.config_root = self._find_config_root()
        self.agent_config_dir = os.path.join(
            self.config_root, "agent_library", agent_system_name
        )
        
        if not os.path.exists(self.agent_config_dir):
            raise FileNotFoundError(f"Agent配置目录不存在: {self.agent_config_dir}")
        
        # 加载所有配置
        self.general_prompts = self._load_general_prompts()
        self.all_tools = self._load_all_tools()
        
    def _find_config_root(self) -> str:
        """查找配置根目录"""
        # 使用MLA_V3自己的config目录
        current_dir = Path(__file__).parent.parent
        mla_v3_config = current_dir / "config"
        
        if not mla_v3_config.exists():
            raise FileNotFoundError(f"配置目录不存在: {mla_v3_config}")
        
        return str(mla_v3_config)
    
    def _load_general_prompts(self) -> Dict:
        """
        加载通用提示词配置
        
        注意：general_prompts.yaml 现在使用 XML 格式
        由 ContextBuilder 直接读取，此方法保留为兼容性
        """
        prompts_file = os.path.join(self.agent_config_dir, "general_prompts.yaml")
        if not os.path.exists(prompts_file):
            return {}
        
        with open(prompts_file, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
            # 兼容旧格式
            return data.get("general_prompts", {})
    
    def _load_all_tools(self) -> Dict[str, Dict]:
        """加载所有工具和Agent配置"""
        all_tools = {}
        
        # 查找所有level配置文件
        for filename in os.listdir(self.agent_config_dir):
            if filename.startswith("level_") and filename.endswith(".yaml"):
                filepath = os.path.join(self.agent_config_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = yaml.safe_load(f)
                    tools = data.get("tools", {})
                    all_tools.update(tools)
        
        return all_tools
    
    def get_tool_config(self, tool_name: str) -> Dict:
        """
        获取指定工具的配置，并处理available_tool_level字段
        
        Args:
            tool_name: 工具名称
            
        Returns:
            工具配置字典
        """
        if tool_name not in self.all_tools:
            raise KeyError(f"工具 {tool_name} 不存在于配置中")
        
        config = self.all_tools[tool_name].copy()
        
        # 处理available_tool_level（特殊情况：judge_agent）
        if "available_tool_level" in config and "available_tools" not in config:
            tool_level = config["available_tool_level"]
            # 获取该level的所有工具
            level_tools = self.get_available_tools_by_level(tool_level)
            config["available_tools"] = level_tools
            print(f"✅ 为{tool_name}自动生成工具列表（Level {tool_level}）: {len(level_tools)}个工具")
        
        return config
    
    def build_agent_system_prompt(self, agent_config: Dict) -> str:
        """
        ⚠️ 已废弃：此方法不再使用
        
        上下文构建已移至 ContextBuilder.build_context()
        该方法负责读取 general_prompts.yaml（XML格式）并构建完整上下文
        """
        # 保留此方法仅为向后兼容
        return ""
    
    def get_available_tools_by_level(self, level: int) -> List[str]:
        """
        获取指定level的所有工具名称
        
        Args:
            level: 工具级别
            
        Returns:
            工具名称列表
        """
        tools = []
        for tool_name, tool_config in self.all_tools.items():
            if tool_config.get("level") == level:
                tools.append(tool_name)
        return tools


if __name__ == "__main__":
    # 测试配置加载
    loader = ConfigLoader("infiHelper")
    print(f"✅ 成功加载配置系统: {loader.agent_system_name}")
    print(f"📁 配置目录: {loader.agent_config_dir}")
    print(f"🔧 总共加载 {len(loader.all_tools)} 个工具/Agent")
    print(f"\nLevel 0 工具数量: {len(loader.get_available_tools_by_level(0))}")
    print(f"Level 1 Agent数量: {len(loader.get_available_tools_by_level(1))}")

