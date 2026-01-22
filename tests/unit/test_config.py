"""Unit tests for ConfigManager."""

import pytest
import json
from pathlib import Path

from ecb_tool.core.config import ConfigManager


def test_config_manager_init(temp_project_dir):
    """Test ConfigManager initialization."""
    config_file = temp_project_dir / 'test_config.json'
    schema = {'key': 'value', 'nested': {'item': 42}}
    
    manager = ConfigManager(config_file, schema)
    
    assert manager.path == config_file
    assert manager.schema == schema
    assert manager.config == schema


def test_config_manager_save_and_load(temp_project_dir):
    """Test saving and loading configuration."""
    config_file = temp_project_dir / 'test_config.json'
    schema = {'setting': 'default'}
    
    manager = ConfigManager(config_file, schema)
    manager.set('setting', 'modified')
    
    # Verify file exists
    assert config_file.exists()
    
    # Load with new instance
    manager2 = ConfigManager(config_file, schema)
    assert manager2.get('setting') == 'modified'


def test_config_manager_get(temp_project_dir):
    """Test getting configuration values."""
    config_file = temp_project_dir / 'test_config.json'
    schema = {'existing': 'value'}
    
    manager = ConfigManager(config_file, schema)
    
    assert manager.get('existing') == 'value'
    assert manager.get('missing', 'default') == 'default'


def test_config_manager_set(temp_project_dir):
    """Test setting configuration values."""
    config_file = temp_project_dir / 'test_config.json'
    schema = {'key': 'old'}
    
    manager = ConfigManager(config_file, schema)
    manager.set('key', 'new')
    
    assert manager.get('key') == 'new'
    assert config_file.exists()


def test_config_manager_deep_copy(temp_project_dir):
    """Test deep copy prevents reference sharing."""
    config_file = temp_project_dir / 'test_config.json'
    schema = {'nested': {'list': [1, 2, 3]}}
    
    manager = ConfigManager(config_file, schema)
    
    # Modify config
    manager.config['nested']['list'].append(4)
    
    # Schema should be unchanged
    assert len(schema['nested']['list']) == 3
