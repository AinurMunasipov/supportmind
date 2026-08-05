# SupportMind Project Definition

## Goal

Build an open-source AI Support Agent that uses CockroachDB Cloud as persistent agent memory. SupportMind is not a chatbot: its main feature is durable memory. It recalls previous conversations, customer preferences, uploaded documents, unresolved issues, and historical context so that assistance improves across sessions instead of starting from zero.

The project is being developed for the CockroachDB × AWS Hackathon and must satisfy the official hackathon requirements.

## Product problem

Customer support interactions are often fragmented across sessions. Traditional chatbots forget prior context, customers repeat information, agents miss relevant history, and unresolved issues lose continuity. SupportMind addresses this by treating support memory as a durable, searchable product capability inside CockroachDB Cloud.

## Target outcome

A customer can return in a later session and receive support informed by relevant prior interactions and open issues. The response should be grounded in memory stored in CockroachDB, with semantic retrieval powered by its Distributed Vector Index.

## In scope

- A Python and FastAPI support-assistant API
- Persistent memory in CockroachDB Cloud
- SQLAlchemy-based database access
- Conversation, preference, support-history, and unresolved-issue memory
- Semantic retrieval using the CockroachDB Distributed Vector Index
- Response generation and semantic representations through the LLM provider (initial implementation uses OpenAI API)
- AWS Lambda integration for asynchronous background jobs, document ingestion, embedding generation, and memory maintenance
- Amazon S3 storage for uploaded PDFs, screenshots, attachments, and knowledge documents
- CockroachDB Cloud Managed MCP Server integration
- Documentation and verification needed for an open-source hackathon submission

## Out of scope for the foundation

- Backend implementation
- Frontend implementation
- Python source files
- Database schemas or migrations
- Cloud resources and deployment configuration
- Additional frameworks, services, queues, caches, or infrastructure

Future scope changes require explicit approval.

## Functional requirements

1. Record conversations and messages durably.
2. Associate memories with the correct customer and support context.
3. Store and update customer preferences.
4. Preserve support history and the state of unresolved issues.
5. Create semantic representations of relevant support content.
6. Retrieve semantically related memory using CockroachDB's Distributed Vector Index.
7. Provide selected memory to the LLM provider (initial implementation uses OpenAI API) when generating a support response.
8. Persist the new interaction and resulting support state.
9. Connect S3-hosted support artifacts to authoritative metadata in CockroachDB.
10. Demonstrate a controlled workflow using the CockroachDB Cloud Managed MCP Server.

## Quality requirements

- **Correctness:** retrieved memory belongs to the correct customer and context.
- **Traceability:** semantic results link back to their source records.
- **Durability:** support state survives process and session boundaries.
- **Security:** secrets and customer information are handled with least privilege.
- **Clarity:** code and documentation favor direct, readable designs.
- **Testability:** important memory and response flows can be verified independently.
- **Operability:** failures are visible and do not silently corrupt memory.

## Delivery milestones

### 1. Project foundation

- Establish project, architecture, license, and repository documentation.

### 2. Contracts and data design

- Define API boundaries.
- Define the CockroachDB memory schema and vector indexing strategy.
- Define ownership, issue state, artifact references, and retrieval constraints.

### 3. Core memory implementation

- Add CockroachDB Cloud connectivity through SQLAlchemy.
- Implement durable structured and semantic memory operations.
- Verify customer-scoped vector retrieval.

### 4. Assistant workflow

- Integrate the LLM provider (initial implementation uses OpenAI API).
- Assemble relevant memory for support responses.
- Persist conversations and support-state changes.

### 5. AWS and MCP integration

- Implement the approved AWS Lambda responsibilities.
- Integrate Amazon S3 for approved support artifacts.
- Demonstrate the approved CockroachDB Cloud Managed MCP Server workflow.

### 6. Submission readiness

- Add focused tests and operational documentation.
- Validate the end-to-end demonstration against official hackathon requirements.
- Prepare the open-source submission materials.

Each milestone should be delivered in small, reviewable tasks. Architecture decisions must be documented before implementation when they affect system boundaries.

## Success criteria

- A returning customer's previous conversations, preferences, uploaded documents, unresolved issues, and historical context can affect a later support response.
- Unresolved issues remain visible across separate conversations.
- Semantic recall uses the CockroachDB Distributed Vector Index.
- Structured and semantic memory remain durable and traceable in CockroachDB Cloud.
- The solution visibly and meaningfully uses AWS Lambda and Amazon S3.
- The solution demonstrates the CockroachDB Cloud Managed MCP Server.
- The final project meets the official hackathon submission requirements without unapproved technologies.

## Current phase

Project foundation only. No implementation has been started.
