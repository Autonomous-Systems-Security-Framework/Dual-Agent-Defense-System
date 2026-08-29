"""
Unified Verification Suite for the Dual-Agent Defense System.

Run with:

    python -m pytest tests/test_env.py -v
"""

import sys

import pytest
from datasets import Dataset

from src.core.dataset_loader import (
    DatasetLoader,
    OPEN_PROMPT_INJECTION,
    NEMOTRON_AGENTIC_INJECTION,
)


class TestEnvironment:
    """Verify that the required Python environment is available."""

    def test_python_version(self):
        """Project requires Python 3.9 or newer."""
        assert sys.version_info >= (3, 9)

    def test_datasets_package(self):
        """Verify that Hugging Face datasets is installed."""
        import datasets

        assert datasets.__version__


class TestOpenPromptInjection:
    """Verify the Open Prompt Injection training dataset."""

    @pytest.fixture(scope="class")
    def dataset(self):
        return DatasetLoader.load_open_prompt_injection()

    def test_dataset_loads(self, dataset):
        assert isinstance(dataset, Dataset)

    def test_dataset_is_not_empty(self, dataset):
        assert len(dataset) > 0

    def test_required_columns_exist(self, dataset):
        required_columns = {
            "instruction",
            "normal_input",
            "attack_input",
            "task_type",
            "attack_type",
            "injected_task",
            "sample_id",
        }

        assert required_columns.issubset(set(dataset.column_names))

    def test_sample_id_is_present(self, dataset):
        assert dataset[0]["sample_id"] is not None


class TestNemotronAgenticInjection:
    """Verify the NVIDIA Nemotron training dataset."""

    @pytest.fixture(scope="class")
    def dataset(self):
        return DatasetLoader.load_nemotron_agentic_injection()

    def test_dataset_loads(self, dataset):
        assert isinstance(dataset, Dataset)

    def test_dataset_is_not_empty(self, dataset):
        assert len(dataset) > 0

    def test_required_columns_exist(self, dataset):
        required_columns = {
            "license",
            "id",
            "domain",
            "attack_category",
            "target_tool",
            "injection_vector",
            "agent_ref",
            "responses_create_params",
            "environment",
            "required_tools",
            "injection",
            "verifier_config",
            "used_in",
        }

        assert required_columns.issubset(set(dataset.column_names))

    def test_sample_id_is_present(self, dataset):
        assert dataset[0]["id"] is not None