
from typing import Any

from src.core.experiment_recorder import ExperimentRecorder


class ToolEnvironment:
    """
    Controlled environment containing simulated agent tools.

    No real emails or financial transactions are performed.
    Each side-effecting action attempt produces one experiment event.
    """

    ACTION_TOOLS = {"send_email", "transfer_funds"}

    def __init__(
        self,
        documents: dict[str, str] | None = None,
        recorder: ExperimentRecorder | None = None,
    ):
        self.documents = documents or {}
        self.action_log: list[dict[str, Any]] = []
        self.recorder = recorder

    def _record_action(
        self,
        agent: str,
        tool: str,
        arguments: dict[str, Any],
        authorized: bool | None,
        executed: bool,
        outcome: str,
    ) -> None:
        """Record exactly one completed action attempt."""

        if self.recorder:
            self.recorder.record_event(
                agent=agent,
                tool=tool,
                arguments=arguments,
                attempted=True,
                executed=executed,
                authorized=authorized,
                outcome=outcome,
            )

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        agent: str = "unknown",
        authorized: bool | None = None,
    ) -> dict[str, Any]:
        """Execute one supported simulated tool."""

        if tool_name == "read_document":
            document_id = arguments.get("document_id")

            if document_id not in self.documents:
                raise ValueError("Document not found")

            return {
                "status": "success",
                "content": self.documents[document_id],
            }

        elif tool_name == "summarize_document":
            document_id = arguments.get("document_id")

            if document_id not in self.documents:
                raise ValueError("Document not found")

            content = self.documents[document_id]

            return {
                "status": "success",
                "summary": content[:200],
            }

        elif tool_name == "send_email":
            try:
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
                    "simulated": True,
                }

                self.action_log.append(action)

                self._record_action(
                    agent=agent,
                    tool=tool_name,
                    arguments=arguments,
                    authorized=authorized,
                    executed=True,
                    outcome="success",
                )

                return {
                    "status": "success",
                    "message": "Email simulated successfully",
                }

            except ValueError:
                self._record_action(
                    agent=agent,
                    tool=tool_name,
                    arguments=arguments,
                    authorized=authorized,
                    executed=False,
                    outcome="rejected",
                )
                raise

        elif tool_name == "transfer_funds":
            try:
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
                    "simulated": True,
                }

                self.action_log.append(action)

                self._record_action(
                    agent=agent,
                    tool=tool_name,
                    arguments=arguments,
                    authorized=authorized,
                    executed=True,
                    outcome="success",
                )

                return {
                    "status": "success",
                    "message": "Mock transfer recorded",
                }

            except ValueError:
                self._record_action(
                    agent=agent,
                    tool=tool_name,
                    arguments=arguments,
                    authorized=authorized,
                    executed=False,
                    outcome="rejected",
                )
                raise

        else:
            raise ValueError(f"Unsupported tool: {tool_name}")
