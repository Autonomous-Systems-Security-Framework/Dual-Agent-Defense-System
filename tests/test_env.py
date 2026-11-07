
import pytest

from src.core.tool_environment import ToolEnvironment


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
