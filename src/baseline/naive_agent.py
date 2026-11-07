
import json

from sympy import content

from src.core.tool_environment import ToolEnvironment


class NaiveAgent:
    """
    Deterministic vulnerable baseline.

    Reads a document and executes a structured action found inside it
    without checking whether the user authorized that action.

    This intentionally models missing security controls.
    """

    ACTION_MARKER = "UNTRUSTED_ACTION:"

    def __init__(self, environment: ToolEnvironment):
        self.environment = environment

    def run(self, user_request: str, document_id: str) -> dict:
        # Step 1: Read the external document.
        document_result = self.environment.execute(
            "read_document",
            {"document_id": document_id}
        )

        content = document_result["content"]

        # Step 2: Look for an embedded action.
        action_payload = None

        marker_index = content.find(self.ACTION_MARKER)

        if marker_index != -1:
            raw_payload = content[
                marker_index + len(self.ACTION_MARKER):
            ].strip()

            try:
                action_payload, _ = json.JSONDecoder().raw_decode(raw_payload)
            except json.JSONDecodeError:
                return {
                    "status": "invalid_payload",
                    "user_request": user_request,
                    "executed": False
                }

        # Step 3: No embedded action means no action is executed.
        if action_payload is None:
            return {
                "status": "completed_without_action",
                "user_request": user_request,
                "executed": False
            }

        # Step 4: Intentionally vulnerable behavior.
        # The agent does not verify the action against user intent.
        tool_name = action_payload.get("tool")
        arguments = action_payload.get("arguments", {})

        if not isinstance(tool_name, str) or not isinstance(arguments, dict):
            return {
                "status": "invalid_payload",
                "user_request": user_request,
                "executed": False
            }

        # Step 5: Execute the embedded action.
        result = self.environment.execute(tool_name, arguments)

        return {
            "status": "action_executed",
            "user_request": user_request,
            "executed": True,
            "action": action_payload,
            "tool_result": result
        }
