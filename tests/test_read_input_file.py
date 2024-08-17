import os
import pytest
from read_input_file import pick_random_topic

@pytest.fixture
def temp_input_directory(tmp_path):
    """
    Fixture to create a temporary input directory with test files.
    """
    topics_file = tmp_path / "topics.txt"
    topics_file.write_text("Topic 1\nTopic 2\nTopic 3\n")
    return tmp_path

def test_pick_random_topic(temp_input_directory):
    random_topic = pick_random_topic(temp_input_directory)
    assert random_topic in ["Topic 1", "Topic 2", "Topic 3"]

def test_no_files_in_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        pick_random_topic(tmp_path)

def test_empty_file(tmp_path):
    empty_file = tmp_path / "empty.txt"
    empty_file.touch()
    with pytest.raises(ValueError):
        pick_random_topic(tmp_path)
