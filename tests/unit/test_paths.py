"""Unit tests for path management."""

import pytest
from pathlib import Path

from ecb_tool.core.paths import (
    find_project_root,
    get_project_paths,
    ensure_directories,
    ProjectPaths,
)


def test_find_project_root(temp_project_dir):
    """Test project root detection."""
    root = find_project_root(temp_project_dir)
    assert root == temp_project_dir


def test_get_project_paths(temp_project_dir):
    """Test ProjectPaths creation."""
    paths = get_project_paths(temp_project_dir)
    
    assert isinstance(paths, ProjectPaths)
    assert paths.root == temp_project_dir
    assert paths.config == temp_project_dir / 'config'
    assert paths.data == temp_project_dir / 'data'
    assert paths.beats == temp_project_dir / 'workspace' / 'beats'
    assert paths.covers == temp_project_dir / 'workspace' / 'covers'


def test_ensure_directories(project_paths):
    """Test directory creation."""
    # Remove a directory
    if project_paths.logs.exists():
        project_paths.logs.rmdir()
    
    # Ensure directories
    ensure_directories(project_paths)
    
    # Verify all exist
    assert project_paths.config.exists()
    assert project_paths.data.exists()
    assert project_paths.logs.exists()
    assert project_paths.beats.exists()
    assert project_paths.covers.exists()


def test_path_properties(project_paths):
    """Test all path properties are Path objects."""
    for attr_name in dir(project_paths):
        if not attr_name.startswith('_'):
            attr = getattr(project_paths, attr_name)
            if not callable(attr):
                assert isinstance(attr, Path), f"{attr_name} should be Path"
