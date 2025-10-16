# Contributing to Enterprise AI Copilot

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing to this project.

## Development Setup

1. **Fork and clone the repository**
```bash
git clone https://github.com/WajdiHammami/ai-copilot.git
cd ai-copilot
```

2. **Create a virtual environment**
```bash
python3 -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt  # If you create this for dev tools
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Add your Azure OpenAI credentials
```

## Code Style

- Follow PEP 8 style guidelines
- Use type hints for function signatures
- Write docstrings for all public functions and classes
- Keep functions focused and under 50 lines when possible
- Use meaningful variable and function names

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

```bash
pytest tests/
pytest --cov=src tests/
```

## Pull Request Process

1. Create a new branch for your feature
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and commit with clear messages
   ```bash
   git commit -m "Add: brief description of what you added"
   ```

3. Push to your fork
   ```bash
   git push origin feature/your-feature-name
   ```

4. Open a Pull Request with:
   - Clear title and description
   - Reference to any related issues
   - Screenshots if UI changes
   - Test results

## Questions?

Feel free to open an issue for any questions or concerns.

Thank you for contributing! 🎉
