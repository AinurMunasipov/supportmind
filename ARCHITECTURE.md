# SupportMind Architecture

## Purpose

SupportMind is an AI Support Agent whose memory persists across requests and support sessions. It is not a chatbot: durable memory stored inside CockroachDB Cloud is its main feature. The agent remembers previous conversations, customer preferences, uploaded documents, unresolved issues, and historical context instead of starting every conversation from zero. CockroachDB Cloud is the authoritative memory layer, not merely application storage.

This document records the architecture boundaries approved for the project foundation. It deliberately avoids prescribing implementation details that have not yet been decided.

## Architecture principles

1. **Durable memory first:** conversations, preferences, support history, unresolved issues, and semantic context belong in CockroachDB Cloud.
2. **Relevant context only:** the assistant retrieves useful historical and semantic context before generating an answer.
3. **Clear responsibilities:** API handling, memory, AI generation, background processing, and document storage remain distinct concerns.
4. **Minimal technology set:** only the mandatory hackathon technologies are included.
5. **Incremental design:** schemas, API contracts, deployment topology, and operational policies will be specified before implementation.

## System components

### FastAPI application

The Python application exposes SupportMind's HTTP API. It validates requests, coordinates memory retrieval, calls the LLM provider (initial implementation uses OpenAI API), and persists the resulting support interaction through SQLAlchemy.

### CockroachDB Cloud memory layer

CockroachDB Cloud is the source of truth for persistent agent memory. Its responsibilities include:

- customer identity and preferences;
- conversations and messages;
- support history;
- issue state, including unresolved issues;
- semantic representations and their source references; and
- metadata needed to retrieve and explain remembered context.

The CockroachDB Distributed Vector Index supports similarity search over semantic memory. Relational filters and vector retrieval should work together so that recalled context is relevant to the correct customer and support scope.

SQLAlchemy provides application-side database access. Concrete tables, relationships, indexes, retention rules, and transaction boundaries are deferred to the data-model design task.

### LLM provider (initial implementation uses OpenAI API)

The LLM provider (initial implementation uses OpenAI API) provides the model capabilities needed to create semantic representations and produce support responses. Prompts should receive only the current request and the relevant memory selected by the application.

### AWS Lambda

AWS Lambda runs asynchronous background jobs for document ingestion, embedding generation, and memory maintenance. The exact function boundaries, invocation model, and relationship to the FastAPI application remain implementation decisions and will be documented before code is introduced.

### Amazon S3

Amazon S3 stores uploaded documents and support artifacts that should not be stored directly as relational records, including PDFs, screenshots, attachments, and knowledge documents. CockroachDB retains the durable metadata, semantic context, and references that connect each stored document or artifact to its customer, conversation, or issue. Limits, lifecycle rules, and access controls remain to be defined.

### CockroachDB Cloud Managed MCP Server

The CockroachDB Cloud Managed MCP Server provides managed, controlled access to CockroachDB data for MCP-compatible workflows. Its permitted operations and security boundaries must be defined before integration; it does not replace the application's normal SQLAlchemy persistence path.

## Core request flow

1. A support request reaches the FastAPI application.
2. The application identifies the relevant customer and support context.
3. SQLAlchemy queries CockroachDB for relational memory and unresolved issue state.
4. The Distributed Vector Index retrieves semantically related memory from CockroachDB.
5. The application assembles the current request and selected memory for the LLM provider (initial implementation uses OpenAI API).
6. The generated response and new support state are persisted to CockroachDB.
7. If the interaction involves an object stored in S3, its durable reference and support context are maintained in CockroachDB.
8. The response is returned to the caller.

## Memory model boundaries

The future data model must preserve these categories:

- **Conversation memory:** ordered conversations and messages.
- **Customer memory:** stable customer details and preferences.
- **Support memory:** prior cases, actions, outcomes, and relevant history.
- **Issue memory:** current status, ownership context, and unresolved items.
- **Document memory:** durable metadata, extracted semantic context, and source references for documents and artifacts stored in S3.
- **Semantic memory:** vectorized content linked back to its source record.

Semantic memory complements structured records; it does not replace them. Every vector should remain traceable to authoritative support data.

## Future AWS Integrations

Amazon Bedrock may be evaluated in future iterations if it provides advantages over the current LLM provider. It is not currently implemented and is not part of the present architecture.

## Security and reliability expectations

- Secrets must be provided through deployment configuration and never committed.
- Customer memory must be isolated by explicit scope in every retrieval path.
- Database and S3 access should follow least-privilege permissions.
- Stored semantic data must remain attributable to its source.
- Failures must not silently create a response without recording the intended support state.
- Logging must avoid exposing secrets or unnecessary customer content.

## Decisions intentionally deferred

- SQL schema and migration approach
- Public API endpoints and payloads
- Authentication and authorization model
- Lambda function boundaries and deployment packaging
- S3 artifact policy and object layout
- Embedding and generation model selection
- Memory ranking, summarization, and retention policies
- Managed MCP Server permissions and exposed workflows
- Observability and testing strategy

Any decision that changes these boundaries or introduces another technology requires explicit approval and a documentation update first.
