# AI Code Healer

An intelligent system for automated error detection, correction, and pattern learning in code. This project leverages advanced AI techniques to help developers identify and fix bugs, learn from common patterns, and improve code quality.

## Core Features

### 1. Intelligent Code Analysis
- Automated error detection and correction
- Pattern-based learning using vector databases (ChromaDB)
- Semantic code understanding and analysis
- Context-aware bug fixing

### 2. Multi-Language Support
Currently supports:
- Python (with self-healing capabilities)
- JavaScript/TypeScript (using Node.js runtime)
- C/C++ (using GCC compiler)

Each language is supported through:
- Language-specific syntax highlighting
- Custom execution environments
- Language-specific error handling
- JSON-based argument passing

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
- Language selection dropdown
- JSON-based argument input

## Project Structure

```
AI-code-healer/
├── code_healer/          # Django project settings
├── web/                  # Django application
│   ├── templates/        # HTML templates
│   ├── migrations/       # Database migrations
│   ├── views.py         # View logic and language execution
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
- Node.js 20.0.0 or higher (for JavaScript/TypeScript support)
- GCC 13.0.0 or higher (for C/C++ support)
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

3. Install system dependencies:
```bash
# For macOS (using Homebrew)
brew install node
brew install gcc

# For Ubuntu/Debian
sudo apt-get install nodejs
sudo apt-get install gcc
```

4. Install Python dependencies:
```bash
pip install -r requirements.txt
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Start the development server:
```bash
python manage.py runserver
```

7. Access the web interface at http://localhost:8000

## Usage

1. Open the web interface
2. Select your programming language from the dropdown
3. Input your code in the editor
4. Provide arguments in JSON format (e.g., `{"x": 10, "y": 2}`)
5. Click "Execute" to run the code
6. View the analysis results and suggested fixes
7. Apply the fixes or explore alternative solutions

## Language-Specific Features

### Python
- Full syntax support
- Dynamic type checking
- Package dependency analysis
- Virtual environment validation
- Self-healing capabilities

### JavaScript/TypeScript
- ES6+ syntax support
- Node.js runtime execution
- JSON argument parsing
- Console output capture

### C/C++
- GCC compilation
- Standard library support
- Integer-based argument handling
- Compilation error reporting

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
- Node.js for JavaScript execution
- GCC for C/C++ compilation
