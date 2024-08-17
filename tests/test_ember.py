import sys
import os
import pytest

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from ember import create_folders_if_not_exist

@pytest.fixture
def temp_directory(tmp_path):
    """Fixture to create a temporary directory for testing."""
    return tmp_path

def test_create_folders_if_not_exist_creates_folders(temp_directory):
    folders_to_create = ["folder1", "folder2", "folder3"]
    create_folders_if_not_exist(temp_directory, folders_to_create)
    
    # Verify folders are created
    for folder in folders_to_create:
        assert (temp_directory / folder).exists()

def test_create_folders_if_not_exist_does_not_create_existing_folders(temp_directory):
    folders_to_create = ["folder1", "folder2"]
    # Create folders first
    for folder in folders_to_create:
        (temp_directory / folder).mkdir()
    
    create_folders_if_not_exist(temp_directory, folders_to_create)
    
    # Verify folders still exist (no errors, no new folders created)
    for folder in folders_to_create:
        assert (temp_directory / folder).exists()
