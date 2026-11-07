
from typing import Any


class ToolEnvironment:
    """
    A controlled environment containing simulated agent tools.

    No real emails or financial transactions are performed.
    All actions are recorded in memory for evaluation.
    """

    def __init__(self, documents: dict[str, str] | None = None):
        self.documents = documents or {}
        self.action_log: list[dict[str, Any]] = []

    def execute(self, tool_name: str, arguments: dict[str, Any]):
        """Execute one supported simulated tool."""

        if tool_name == "read_document":
            document_id = arguments.get("document_id")

            if document_id not in self.documents:
                raise ValueError("Document not found")

            return {
                "status": "success",
                "content": self.documents[document_id]
            }

        elif tool_name == "summarize_document":
            document_id = arguments.get("document_id")

            if document_id not in self.documents:
                raise ValueError("Document not found")

            content = self.documents[document_id]

            return {
                "status": "success",
                "summary": content[:200]
            }

        elif tool_name == "send_email":
            recipient = arguments.get("recipient")
            subject = arguments.get("subject")
            body = arguments.get("body")

            if not recipient or not subject or not body:
                raise ValueError("Missing email fields")

            action = {
                "tool": "send_email",
                "recipient": recipient,
                "subject": subject,
                "body": body,
                "simulated": True
            }

            self.action_log.append(action)

            return {
                "status": "success",
                "message": "Email simulated successfully"
            }

        elif tool_name == "transfer_funds":
            recipient = arguments.get("recipient")
            amount = arguments.get("amount")

            if not recipient or not isinstance(amount, (int, float)):
                raise ValueError("Invalid transfer details")

            if isinstance(amount, bool) or amount <= 0:
                raise ValueError("Transfer amount must be positive")

            action = {
                "tool": "transfer_funds",
                "recipient": recipient,
                "amount": amount,
                "simulated": True
            }

            self.action_log.append(action)

            return {
                "status": "success",
                "message": "Mock transfer recorded"
            }

        else:
            raise ValueError(f"Unsupported tool: {tool_name}")
