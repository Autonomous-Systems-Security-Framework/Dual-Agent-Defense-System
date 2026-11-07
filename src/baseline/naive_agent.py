
import json

from src.core.tool_environment import ToolEnvironment


class NaiveAgent:
    """
    Deterministic vulnerable baseline.

    Reads an untrusted document and executes a structured action
    found inside it without checking user authorization.
    """

    ACTION_MARKER = "UNTRUSTED_ACTION:"

    def __init__(self, environment: ToolEnvironment):
        self.environment = environment

    def run(self, user_request: str, document_id: str) -> dict:
        # Step 1: Read the external document.
        document_result = self.environment.execute(
            "read_document",
            {"document_id": document_id},
            agent="naive_baseline",
        )

        content = document_result["content"]
        action_payload = None

        # Step 2: Find an embedded action.
        marker_index = content.find(self.ACTION_MARKER)

        if marker_index != -1:
            raw_payload = content[
                marker_index + len(self.ACTION_MARKER):
            ].strip()

            try:
                action_payload, _ = json.JSONDecoder().raw_decode(
                    raw_payload
                )
            except json.JSONDecodeError:
                return {
                    "status": "invalid_payload",
                    "user_request": user_request,
                    "executed": False,
                }

        # Step 3: No action found.
        if action_payload is None:
            return {
                "status": "completed_without_action",
                "user_request": user_request,
                "executed": False,
            }

        # Step 4: Validate payload structure.
        if not isinstance(action_payload, dict):
            return {
                "status": "invalid_payload",
                "user_request": user_request,
                "executed": False,
            }

        tool_name = action_payload.get("tool")
        arguments = action_payload.get("arguments", {})

        if not isinstance(tool_name, str) or not isinstance(arguments, dict):
            return {
                "status": "invalid_payload",
                "user_request": user_request,
                "executed": False,
            }

        # Step 5: Execute without authorization checks.
        result = self.environment.execute(
            tool_name,
            arguments,
            agent="naive_baseline",
            authorized=None,
        )

        return {
            "status": "action_executed",
            "user_request": user_request,
            "executed": True,
            "action": action_payload,
            "tool_result": result,
        }
