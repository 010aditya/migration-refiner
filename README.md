# Migration Refiner 

🚀 An intelligent, agent-based tool that refines partially migrated Java legacy systems (EJB, Struts, JSP, iBatis) into production-ready Spring Boot code.

## 🔥 Features

- ✅ Auto-verifies `mapping.json` with vector similarity
- ✅ Refines broken code using GPT-4o with stitched legacy context
- ✅ Recovers from build failures (retry agent)
- ✅ Generates JUnit tests
- ✅ Detects DB/cache/tool automatically from pom.xml or gradle
- ✅ Supports Java 21 + Gradle or Maven
- ✅ Docker-ready

## 🧱 Structure

```
.
├── legacy_code/              # Input legacy source
├── migrated_code/            # Initial migrated output
├── framework_code/           # Migrated base classes (optional)
├── agents/                   # All AI agents
├── main.py                   # Pipeline entrypoint
├── Dockerfile
├── init.sh
├── requirements.txt
├── README.md
```

## 🧪 How to Run

### Locally

```bash
bash init.sh
python main.py
```

### With Docker

```bash
docker build -t migration-refiner .
docker run -v $(pwd):/app migration-refiner
```

## 🤖 Prerequisites

- OpenAI API Key (set `OPENAI_API_KEY`)
- Python 3.10+
- Java 21
- Gradle or Maven (auto-detected)

## 🧠 Architecture

```
mapping.json
   ↓
MappingVerifierAgent → mapping.verified.json
   ↓
CoordinatorAgent
   ├── MetadataAgent
   ├── EmbeddingIndexerAgent
   ├── ContextStitcherAgent
   ├── FixAndCompleteAgent
   ├── TestGeneratorAgent
   ├── BuildValidatorAgent
   └── RetryAgent
```

## 🙋‍♂️ Need Help?

Open an issue or ping `@yourgithubhandle`.

---

© 2025 — Refactor everything.
