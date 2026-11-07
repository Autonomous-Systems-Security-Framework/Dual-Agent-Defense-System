"""
Dataset loader for the Dual-Agent Defense System.

Loads the training splits of the prompt-injection datasets
used by the project.
"""

from datasets import Dataset, load_dataset


OPEN_PROMPT_INJECTION = "guychuk/open-prompt-injection"
NEMOTRON_AGENTIC_INJECTION = (
    "nvidia/Nemotron-RL-Agentic-Indirect-Prompt-Injection-v1"
)


class DatasetLoader:
    """Loads project datasets from Hugging Face."""

    @staticmethod
    def load_open_prompt_injection() -> Dataset:
        """Load the training split of the Open Prompt Injection dataset."""
        return load_dataset(
            OPEN_PROMPT_INJECTION,
            split="train",
        )

    @staticmethod
    def load_nemotron_agentic_injection() -> Dataset:
        """Load the training split of the NVIDIA Nemotron dataset."""
        return load_dataset(
            NEMOTRON_AGENTIC_INJECTION,
            split="train",
        )