# RAG Agent Backend Application

## Description

This is a RAG (Retrieval-Augmented Generation) agent that uses a FAISS vector store to retrieve relevant information and generate new content.

## Usage

1. Set up the environment variables:
2. Run the application:
3. Access the API endpoints:

- `http://localhost:8000/retrieve` (GET)
- `http://localhost:8000/generate` (POST)

## Flowchart

```mermaid
flowchart TB
  UserInput[User Input] --> Prompt1[Prompt]
  UserInput[User Input] --> CheckIsFollowUp
  subgraph CheckIsFollowUp[Check is follow up]
    Prompt2[Prompt] --> LLM1((LLM)) --> Parser1[Parser]
  end
  CheckIsFollowUp --> FAISS[("FAISS (Vector Store)")] -.-> Prompt1
  OutputModel[Output Model] --> FormatInstruction[Format Instruction] --> Prompt1
  MessageHistory[Message History] --> Prompt1
  MessageHistory[Message History] --> CheckIsFollowUp
  Prompt1 --> LLM2((LLM)) --> Parser2[Parser] --> Result
```
