from setuptools import setup, find_packages

setup(
    name="code_healer",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "langgraph==0.0.8",
        "langchain==0.1.20",
        "langchain-openai==0.1.7",
        "chromadb>=0.4.22",
        "pydantic>=2.0.0",
        "python-dotenv>=1.0.0",
        "django>=4.2.0,<5.0.0",
        "django-crispy-forms>=2.1",
        "crispy-bootstrap5>=0.7",
        "typing-extensions>=4.5.0",
    ],
)
