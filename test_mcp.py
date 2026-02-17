#!/usr/bin/env python3
"""
Test script to check MCP functionality in MindsDB
"""
import os
import sys

# Add the mindsdb directory to Python path
sys.path.insert(0, '/Users/clifforddalsoniii/Documents/Brightforest/projects/experiments/active/ml/mindsdb')

try:
    # Try to import MCP-related modules
    print("Checking for MCP implementation...")

    # Check if MCP directory has any Python files
    import glob
    mcp_files = glob.glob('/Users/clifforddalsoniii/Documents/Brightforest/projects/experiments/active/ml/mindsdb/mindsdb/api/mcp/*.py')
    print(f"MCP directory files: {mcp_files}")

    # Try to import mindsdb config
    os.environ['MINDSDB_CONFIG_PATH'] = '/Users/clifforddalsoniii/.mindsdb/config.json'
    from mindsdb.utilities.config import config
    print("Config loaded successfully")

    # Check what APIs are configured
    apis = os.getenv('MINDSDB_APIS', 'http,mysql')
    print(f"APIs to start: {apis}")

    # Check if there are any MCP-related imports
    try:
        from mindsdb.api import mcp
        print("MCP module imported successfully")
        print(f"MCP module contents: {dir(mcp)}")
    except ImportError as e:
        print(f"MCP module import failed: {e}")

    # Check if there are MCP tools in the skills system
    try:
        from mindsdb.interfaces.skills.skill_tool import SkillToolController
        print("SkillToolController imported successfully")

        # Check what skills are available
        skill_controller = SkillToolController()
        print("SkillToolController instantiated")

    except Exception as e:
        print(f"SkillToolController import/init failed: {e}")

except Exception as e:
    print(f"General error: {e}")
    import traceback
    traceback.print_exc()