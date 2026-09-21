## Project Overview

This project focuses on improving the security and reliability of LLM-based AI agents against prompt injection and indirect prompt injection attacks.

Large Language Model (LLM) agents can interact with external data, tools, APIs, and applications. However, untrusted content can contain hidden or malicious instructions that may influence the agent and cause unintended actions. Previous research has demonstrated that indirect prompt injection can compromise LLM-integrated applications and affect tool usage, data access, and generated responses.

The proposed system introduces a semantic verification layer to check whether an agent's proposed action is consistent with the user's original goal. Textual inputs such as the user's goal and the agent's proposed action are converted into dense vector embeddings. Their semantic similarity/divergence is then calculated to identify possible deviations.

The system can be used as a verification layer before an agent performs an action:

User Goal → LLM Agent → Proposed Action → Semantic Verification → Allow / Reject

The project is inspired by recent research on indirect prompt injection, multi-agent defense pipelines, AgentDojo evaluation, context-aware prompt injection defense, and LLM firewall/validator-agent architectures. These works highlight the need for stronger security mechanisms that verify agent behavior instead of relying only on input filtering.

### Key Objectives

- Detect possible prompt injection and malicious instructions.
- Convert goals and proposed actions into semantic embeddings.
- Measure the semantic alignment between the user's goal and agent action.
- Reject or flag actions that significantly deviate from the original goal.
- Provide an additional security layer for LLM-based agents.
- Improve the reliability and safety of tool-using AI agents.

### Basic Workflow

1. Receive the user's original goal.
2. Generate a proposed action using the LLM agent.
3. Convert both texts into vector embeddings.
4. Calculate semantic similarity/divergence.
5. Compare the result with a predefined threshold.
6. Allow aligned actions and flag/reject suspicious actions.
7. Log the verification result for analysis.

### References

1. Greshake et al., *Not What You've Signed Up For: Compromising Real-World LLM-Integrated Applications with Indirect Prompt Injection*.
2. Weng et al., *ARGUS: Defending LLM Agents Against Context-Aware Prompt Injection*.
3. Hossain et al., *A Multi-Agent LLM Defense Pipeline Against Prompt Injection Attacks*.
4. Debenedetti et al., *AgentDojo: A Dynamic Environment to Evaluate Prompt Injection Attacks and Defenses for LLM Agents*.
5. Gulyamov et al., *Prompt Injection Attacks in Large Language Models and AI Agent Systems: A Comprehensive Review of Vulnerabilities, Attack Vectors, and Defense Mechanisms*.
6. Podpora et al., *LLM Firewall Using Validator Agent for Prevention Against Prompt Injection Attacks*.
