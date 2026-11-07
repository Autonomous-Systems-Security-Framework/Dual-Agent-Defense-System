
import sys

import pytest
from datasets import Dataset

from src.core.tool_environment import ToolEnvironment
from src.core.dataset_loader import (
    DatasetLoader,
    OPEN_PROMPT_INJECTION,
    NEMOTRON_AGENTIC_INJECTION,
)


# ============================================================
# SIMULATED TOOL ENVIRONMENT TESTS
# ============================================================

def test_read_document():
    env = ToolEnvironment({
        "doc1": "This is a sample document."
    })

    result = env.execute(
        "read_document",
        {"document_id": "doc1"}
    )

    assert result["status"] == "success"
    assert result["content"] == "This is a sample document."


def test_summarize_document():
    env = ToolEnvironment({
        "doc1": "A" * 300
    })

    result = env.execute(
        "summarize_document",
        {"document_id": "doc1"}
    )

    assert result["status"] == "success"
    assert len(result["summary"]) == 200


def test_simulated_email():
    env = ToolEnvironment()

    result = env.execute(
        "send_email",
        {
            "recipient": "test@example.com",
            "subject": "Test",
            "body": "Hello"
        }
    )

    assert result["status"] == "success"
    assert len(env.action_log) == 1
    assert env.action_log[0]["simulated"] is True


def test_simulated_transfer():
    env = ToolEnvironment()

    env.execute(
        "transfer_funds",
        {
            "recipient": "test_account",
            "amount": 100
        }
    )

    assert env.action_log[0]["amount"] == 100
    assert env.action_log[0]["simulated"] is True


def test_unknown_tool_rejected():
    env = ToolEnvironment()

    with pytest.raises(ValueError):
        env.execute("unknown_tool", {})


def test_invalid_transfer_rejected():
    env = ToolEnvironment()

    with pytest.raises(ValueError):
        env.execute(
            "transfer_funds",
            {
                "recipient": "test_account",
                "amount": -100
            }
        )


# ============================================================
# PYTHON ENVIRONMENT TESTS
# ============================================================

class TestEnvironment:

    def test_python_version(self):
        assert sys.version_info >= (3, 9)

    def test_datasets_package(self):
        import datasets

        assert datasets.__version__


# ============================================================
# OPEN PROMPT INJECTION DATASET TESTS
# ============================================================

class TestOpenPromptInjection:

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


# ============================================================
# NEMOTRON AGENTIC INJECTION DATASET TESTS
# ============================================================

class TestNemotronAgenticInjection:

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
