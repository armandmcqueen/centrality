# CLI Assistant

A proof-of-life demo of an AI-centric CLI that can translate natural language into outputs (stdout, code, streamlit 
apps, etc.) that satisfy the user's intent.

Specifically, the assistant takes in NL, reads Centrality documentation (possibly via RAG), generates tool use code
(Centrality Python SDK) to collect data, and then generates code to present the data to the user. 

This should initially be human-in-the-loop. The code should be run in a sandboxed environment.

## Ideas

- RAG
- Automatically generate the relevant documentation as part of SDK generation.
- Conversational refining
- Data system to start collecting future training and preference data.

## TODO

- Move GPT to common?
- Add graphviz as dependency




