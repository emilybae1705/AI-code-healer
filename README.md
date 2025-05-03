# AI Code Healer

An intelligent system for automated error detection, correction, and pattern learning in code. This project leverages advanced AI techniques to help developers identify and fix bugs, learn from common patterns, and improve code quality.

## Core Features

### 1. Intelligent Code Analysis
- Automated error detection and correction
- Pattern-based learning using vector databases (ChromaDB)
- Semantic code understanding and analysis
- Context-aware bug fixing

### 2. Multi-Language Support
- Python (primary support)
- JavaScript/TypeScript
- Java
- C/C++
- Ruby
- Go
- Rust
- PHP
- Swift
- Kotlin

Each language is supported through:
- Language-specific syntax parsers
- Custom error pattern recognition
- Language-specific code generation
- Runtime environment validation

### 3. Learning & Pattern Recognition
- Vector-based pattern storage and retrieval
- Similar bug detection across projects
- Historical fix tracking
- Pattern-based solution suggestions

### 4. Safety & Validation
- Runtime safety checks
- Code modification verification
- Test coverage analysis
- Security vulnerability detection

### 5. Web Interface
- Modern, responsive UI
- Real-time code editing with syntax highlighting
- Interactive error visualization
- Solution history tracking

## Project Structure

```
AI-code-healer/
├── code_healer/          # Django project settings
├── web/                  # Django application
│   ├── templates/        # HTML templates
│   ├── migrations/       # Database migrations
│   ├── views.py         # View logic
│   ├── urls.py          # URL routing
│   └── models.py        # Data models
├── src/                  # Core functionality
│   ├── core/            # Core implementation
│   ├── healer.py        # Main healing logic
│   └── test_*.py        # Test files
├── chroma_db/           # Vector database
├── manage.py            # Django management
├── requirements.txt     # Dependencies
└── setup.py            # Package config
```

## Getting Started

### Prerequisites
- Python 3.9.21 or higher
- Conda environment manager
- Modern web browser

### Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/AI-code-healer.git
cd AI-code-healer
```

2. Set up the conda environment:
```bash
conda create -n langgraph python=3.9.21
conda activate langgraph
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Start the development server:
```bash
python manage.py runserver
```

6. Access the web interface at http://localhost:8000

## Usage

1. Open the web interface
2. Input your code in the editor
3. Specify any function arguments if needed
4. Click "Execute" to run the code
5. View the analysis results and suggested fixes
6. Apply the fixes or explore alternative solutions

## Language Support Details

### Python
- Full syntax support
- Dynamic type checking
- Package dependency analysis
- Virtual environment validation

### JavaScript/TypeScript
- ES6+ syntax support
- TypeScript type checking
- NPM package analysis
- Browser compatibility checks

### Java
- JVM bytecode analysis
- Maven/Gradle dependency checking
- Spring framework support
- JUnit test integration

### C/C++
- Compiler-specific error detection
- Memory leak analysis
- Header file dependency checking
- Build system integration

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

MIT License

## Acknowledgments

- LangChain for LLM integration
- ChromaDB for vector storage
- Django for the web framework
- CodeMirror for the code editor
