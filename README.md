# AI Code Healer

An intelligent system for automated error detection, correction, and pattern learning in code.

## Project Structure

```
src/
├── core/                 # Core system components
│   ├── state/           # State management and Pydantic models
│   ├── workflow/        # LangGraph workflow definitions
│   └── validation/      # Code validation and safety checks
├── llm/                 # LLM integration and prompt management
│   ├── prompts/         # System prompts and templates
│   └── models/          # LLM model configurations
├── memory/              # Vector database and memory management
│   ├── chroma/          # ChromaDB integration
│   ├── embeddings/      # Embedding generation and management
│   └── patterns/        # Bug pattern storage and retrieval
├── runtime/             # Runtime code modification
│   ├── patches/         # Code patch generation and application
│   └── safety/          # Runtime safety checks
└── utils/               # Utility functions and helpers
    ├── logging/         # Logging configuration
    └── testing/         # Test utilities and fixtures
```

## Features

- Automated error detection and correction
- Pattern-based learning using vector databases
- Safe runtime code modification
- Hierarchical error management
- Semantic search capabilities

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

3. Run the system:
```bash
python src/main.py
```

## Development

- Use `pytest` for running tests
- Follow the code style guide in `docs/style_guide.md`
- Submit PRs with comprehensive test coverage

## License

MIT License
