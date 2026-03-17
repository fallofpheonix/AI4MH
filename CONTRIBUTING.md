# Contributing to AI4MH

Thank you for your interest in contributing to AI4MH! This document provides guidelines and instructions for contributing to the project.

## Code of Conduct

AI4MH is committed to providing a safe and welcoming environment for all contributors. Please treat all participants with respect and courtesy.

## Getting Started

### Prerequisites
- Python 3.10+
- Node.js 16+
- Git

### Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/AI4MH.git
   cd AI4MH
   ```

2. **Set up the backend environment:**
   ```bash
   cd backend
   python -m venv .venv312
   source .venv312/bin/activate  # On Windows: .venv312\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Set up the frontend environment:**
   ```bash
   cd ../frontend
   npm install
   ```

## Running the Project

### Start the backend server:
```bash
cd backend
source .venv312/bin/activate
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Start the frontend development server:
```bash
cd frontend
npm run dev
```

The dashboard will be available at `http://localhost:5173`

## Running Tests

### Backend tests:
```bash
cd backend
python -m pytest tests/ -v
```

### Health check (full stack validation):
```bash
bash scripts/full_health_check.sh
```

## Commit Guidelines

- Use descriptive commit messages
- Reference issue numbers when applicable (e.g., "Fix #123")
- Keep commits focused on a single concern
- Follow conventional commit format when possible: `type(scope): description`

## Pull Request Process

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and commit them (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request with a clear description of changes

### PR Checklist:
- [ ] Tests pass locally (`pytest` for backend)
- [ ] Health check passes (`bash scripts/full_health_check.sh`)
- [ ] Documentation is updated if needed
- [ ] Commit messages are clear and descriptive
- [ ] No new warnings or errors introduced

## Development Guidelines

### Code Style

**Python:**
- Follow PEP 8
- Use type hints where practical
- Keep functions focused and under 100 lines
- Write docstrings for public functions

**JavaScript/React:**
- Use descriptive variable and function names
- Keep components focused and reusable
- Comment complex logic

### Architecture Principles

- **Modular Design**: Keep pipeline stages independent
- **Testability**: Write testable code with clear inputs/outputs
- **Documentation**: Update docs when changing functionality
- **No Framework Bloat**: Pipeline modules must not import FastAPI
- **Determinism**: Ensure reproducible results for fixed inputs

## Testing

All new features should include tests:

### Backend:
- Unit tests for scoring functions in `tests/test_scoring.py`
- Integration tests for API endpoints in `tests/test_api.py`
- Fixtures in `tests/conftest.py`

Run tests with coverage:
```bash
pytest tests/ -v --cov=backend
```

## Documentation

### When to Update Docs:
- Adding new features
- Changing API endpoints
- Modifying configuration options
- Updating dependencies

### Files to Update:
- `README.md` - Overview and setup
- `docs/ARCHITECTURE.md` - System architecture
- `docs/PROJECT_SPEC.md` - Requirements and constraints
- `docs/ROADMAP.md` - Development priorities
- Inline code comments for complex logic

## Issue Reporting

When reporting bugs, please include:
- Python and Node.js versions
- Operating system
- Steps to reproduce
- Expected vs actual behavior
- Error messages and stack traces

## Feature Requests

When proposing features:
- Describe the use case and benefit
- Explain the proposed implementation
- Consider backward compatibility
- Reference related issues or requirements

## Contact

For questions or discussions:
- Open an issue on GitHub
- Email: human-ai@cern.ch

## Licensing

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to AI4MH! 🎉
