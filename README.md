# SupportMind

SupportMind is an open-source AI Support Agent with persistent memory, created for the CockroachDB × AWS Hackathon. It is not a chatbot: durable memory stored inside CockroachDB Cloud is its defining capability.

SupportMind remembers previous conversations, customer preferences, uploaded documents, unresolved issues, and historical context instead of starting every conversation from zero. CockroachDB Cloud is the agent's core memory layer: it stores durable support state and enables semantic retrieval through the CockroachDB Distributed Vector Index.

## Why SupportMind?

Traditional chatbots forget everything after a conversation ends. SupportMind continuously builds durable customer memory inside CockroachDB Cloud, allowing every future interaction to become smarter instead of starting from zero.

## Project status

SupportMind is currently at the project-foundation stage. Application code and deployment configuration have not been created yet.

## Required technology

- Python
- FastAPI
- CockroachDB Cloud
- SQLAlchemy
- LLM provider (initial implementation uses OpenAI API)
- AWS Lambda
- Amazon S3
- CockroachDB Distributed Vector Index
- CockroachDB Cloud Managed MCP Server

No additional infrastructure or application frameworks are part of the architecture at this stage.

## Intended capabilities

- Maintain durable customer and conversation history.
- Remember customer preferences across support sessions.
- Remember uploaded documents through durable metadata, extracted semantic context, and source references.
- Track support history and unresolved issues.
- Retrieve semantically relevant context for each request.
- Generate context-aware assistance with the LLM provider (initial implementation uses OpenAI API).
- Expose controlled access to CockroachDB-backed memory through the CockroachDB Cloud Managed MCP Server.
- Use AWS Lambda for asynchronous background jobs, document ingestion, embedding generation, and memory maintenance.
- Store uploaded PDFs, screenshots, attachments, and knowledge documents in Amazon S3.

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) describes the approved system boundaries and data flow.
- [PROJECT.md](PROJECT.md) defines the scope, requirements, milestones, and success criteria.

## Development principles

- Keep CockroachDB at the center of agent memory.
- Prefer small, reviewable iterations.
- Optimize for simplicity, readability, and production-quality code.
- Do not introduce technologies or alter architecture without an explicit decision.

## License

SupportMind is licensed under the [MIT License](LICENSE).
