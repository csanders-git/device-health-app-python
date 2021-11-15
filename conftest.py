from typing import Dict
import pytest


@pytest.fixture
def config_file_mock() -> Dict[str, str]:
    config_file_content = {
        "config": "./config.yaml"
    }
    return config_file_content
