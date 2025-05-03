# AI Code Healer
An intelligent tool for automated error detection, correction, and pattern 
learning in code, helping developers identify and fix bugs, learn from common patterns, and improve code quality.

## Live Demo

Check out the live application at: [AI Code Healer](https://ai-code-healer-c6b5ae7a69a0.herokuapp.com/)

## Features

- Real-time code analysis and error detection
- Support for multiple programming languages (Python, JavaScript, TypeScript, C/C++)
- Interactive web interface with syntax highlighting
- AI-powered code fixing suggestions
- Secure and scalable deployment on Heroku
- Modern, responsive UI with Bootstrap

## Tech Stack

### Languages
- Python
- HTML/CSS
- JavaScript

### Frameworks/Libraries
- Django
- LangGraph
- Bootstrap 5
- Crispy Forms
- WhiteNoise
- LLM

### Tools/Technologies
- Heroku
- Conda

## Installation

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

3. Install Python dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Collect static files:
```bash
python manage.py collectstatic --noinput
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
4. Click "Execute" to run the code
5. View the analysis results and suggested fixes
6. Apply the fixes or explore alternative solutions

## Deployment

The application is deployed on Heroku with the following configuration:

1. Python 3.9.21 runtime
2. WhiteNoise for static file serving
3. Environment variables for security
4. Automatic static file collection
5. SSL/TLS enabled

To deploy to Heroku:

1. Create a Heroku account and install the Heroku CLI
2. Login to Heroku:
```bash
heroku login
```

3. Create a new Heroku app:
```bash
heroku create your-app-name
```

4. Set environment variables:
```bash
heroku config:set DJANGO_SECRET_KEY=your-secret-key
heroku config:set DJANGO_DEBUG=False
```

5. Deploy the application:
```bash
git push heroku main
```

## Core Features

### 1. Intelligent Code Analysis
- Automated error detection and correction
- Pattern-based learning using vector databases (ChromaDB)
- Semantic code understanding and analysis
- Context-aware bug fixing

### 2. Multi-Language Support
Currently supports:
- Python
- JavaScript/TypeScript
- C/C++

Each language is supported through:
- Language-specific syntax highlighting
- Custom execution environments
- Language-specific error handling

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

## Project Structure

```
AI-code-healer/
├── AI_code_healer/      # Django project settings
├── web/                 # Django application
│   ├── templates/       # HTML templates
│   ├── migrations/      # Database migrations
│   ├── views.py        # View logic and language execution
│   ├── urls.py         # URL routing
│   └── models.py       # Data models
├── static/             # Static files (CSS, JS)
├── manage.py           # Django management
└── requirements.txt    # Dependencies
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Acknowledgments

- [GenAI_Agents](https://github.com/NirDiamant/GenAI_Agents) - Repository that provided comprehensive tutorials and implementations for building AI agents