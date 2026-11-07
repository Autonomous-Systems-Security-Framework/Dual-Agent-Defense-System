from typing import Any
from copy import deepcopy

class ExperimentRecorder:
    """
    Records agent tool-action events for reproducible evaluation.

    Authorization is supplied as experiment ground truth.
    The recorder does not make security decisions.
    """

    def __init__(self):
        self.events: list[dict[str, Any]] = []
        self._next_event_id = 1

    def record_event(
        self,
        agent: str,
        tool: str,
        arguments: dict[str, Any],
        attempted: bool,
        executed: bool,
        authorized: bool | None,
        outcome: str,
    ) -> dict[str, Any]:

        event = {
            "event_id": self._next_event_id,
            "agent": agent,
            "tool": tool,
            "arguments": deepcopy(arguments),
            "attempted": attempted,
            "executed": executed,
            "authorized": authorized,
            "outcome": outcome,
        }

        self.events.append(event)
        self._next_event_id += 1

        return deepcopy(event)

    def get_events(self) -> list[dict[str, Any]]:
        """Return a copy of recorded events."""
        return deepcopy(self.events)

    def reset(self) -> None:
        """Clear recorded events and reset event numbering."""
        self.events.clear()
        self._next_event_id = 1
