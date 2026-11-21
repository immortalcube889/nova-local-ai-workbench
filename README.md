# Nova Local AI Workbench

A compact, local-first AI-assistant architecture demo built in Python. It demonstrates persistent SQLite memory, a transparent UI, system inspection, and approval-gated action planning without exposing personal data, credentials, or private integrations.

> This repository is a safe portfolio edition of a larger private project. It intentionally contains no model key, trading integration, user files, chat history, or automatic file modification.

## Why this exists

Many assistant demos hide important engineering decisions behind a chat box. Nova makes the boundaries visible:

- **Local persistence:** user-approved notes are stored in SQLite.
- **Inspectable behavior:** system inspection returns structured data.
- **Guarded actions:** file actions are proposals that explicitly require approval; the demo never reads, writes, or deletes user files.
- **No fake intelligence:** this edition uses local retrieval only. A production model provider can be attached behind the API without moving authorization into a prompt.

## Architecture

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Run locally

Requires Python 3.11+ and no third-party packages.

```bash
python -m unittest discover -s tests -v
python -m nova_workbench.app
```

Open `http://127.0.0.1:8080`.

## API

| Route | Purpose |
| --- | --- |
| `GET /health` | Health check for local or cloud hosting |
| `GET/POST /api/memories` | Inspect or save non-sensitive local notes |
| `POST /api/assistant/respond` | Demonstrates transparent local retrieval |
| `POST /api/tools/inspect-system` | Read-only environment inspection |
| `POST /api/tools/plan-file-action` | Returns an approval-required plan; never touches files |

## AWS-ready packaging

The included Dockerfile exposes the service on port `8080`, suitable for a container platform such as AWS App Runner, ECS/Fargate, or a development EC2 instance.

The AWS Blocks migration in `aws-blocks/` hosts a **read-only public portfolio preview** through S3 and CloudFront. The preview intentionally disables memory and tool controls because it does not deploy the local Python API or any personal data. Use the Docker path for a fully functional, authenticated deployment.

Before deploying:

1. Build and run locally: `docker build -t nova-workbench . && docker run --rm -p 8080:8080 nova-workbench`.
2. For a real hosted deployment, move SQLite to an appropriate managed datastore such as RDS or DynamoDB; container filesystems are not durable.
3. Put authentication in front of every non-health route.
4. Store model-provider credentials in AWS Secrets Manager or Parameter Store—not source code, images, browser storage, or `.env` files committed to Git.
5. Keep destructive tools approval-gated server-side.

## What I would add next

- Authentication and per-user memory isolation
- Semantic search using embeddings stored in a managed vector/search service
- A provider adapter for Bedrock or another model API
- Structured logging, metrics, and cost limits
- A CI workflow that runs these tests before deployment

## Portfolio talking points

This project demonstrates Python backend design, HTTP API design, SQLite data modeling, secure-by-default tool boundaries, Docker packaging, test coverage, and a clear path from a local prototype to AWS deployment.

## License

MIT. See [LICENSE](LICENSE).
