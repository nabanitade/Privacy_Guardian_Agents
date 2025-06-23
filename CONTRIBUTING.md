# Contributing to Privacy Guardian Agents

Thank you for your interest in contributing to Privacy Guardian Agents! This document provides guidelines and information for contributors to help maintain code quality and foster a collaborative community.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Contribution Process](#contribution-process)
- [Code Standards](#code-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [License](#license)

## Code of Conduct

### Our Pledge

As contributors and maintainers of Privacy Guardian Agents, we pledge to respect all people who contribute through reporting issues, posting feature requests, updating documentation, submitting pull requests or patches, and other activities.

We are committed to making participation in this project a harassment-free experience for everyone, regardless of level of experience, gender, gender identity and expression, sexual orientation, disability, personal appearance, body size, race, ethnicity, age, or religion.

### Our Standards

Examples of behavior that contributes to creating a positive environment include:

- Using welcoming and inclusive language
- Being respectful of differing opinions and viewpoints
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

Examples of unacceptable behavior by participants include:

- The use of sexual language or imagery, derogatory comments or personal attacks
- Trolling, insulting or derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information, such as physical or electronic addresses, without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

### Enforcement

Project maintainers have the right and responsibility to remove, edit, or reject comments, commits, code, wiki edits, issues, and other contributions that are not aligned to this Code of Conduct. Project maintainers who do not follow the Code of Conduct may be removed from the project team.

This code of conduct applies both within project spaces and in public spaces when an individual is representing the project or its community.

Instances of abusive, harassing, or otherwise unacceptable behavior can be reported by emailing nabanita@privacylicense.com.

This Code of Conduct is adapted from the [Contributor Covenant](https://contributor-covenant.org), version 1.1.0.

## Getting Started

### Prerequisites

- **Node.js** (v14 or higher)
- **npm** (v6 or higher)
- **TypeScript** knowledge (for development)
- **Git** for version control

### Fork and Clone

1. Fork the Privacy Guardian Agents repository
2. Clone your fork locally:
   ```bash
   git clone https://gitlab.com/your-username/privacysdk.git
   cd privacysdk
   ```
3. Add the upstream repository:
   ```bash
   git remote add upstream https://gitlab.com/tnabanitade/privacysdk.git
   ```

## Development Setup

### Installation

1. Install dependencies:
   ```bash
   npm install
   ```

2. Build the project:
   ```bash
   npm run build
   ```

3. Run tests:
   ```bash
   npm test
   ```

### Environment Configuration

For AI-enhanced scanning, set up environment variables:

```bash
# Google Cloud Configuration (for Vertex AI)
export GOOGLE_CLOUD_PROJECT=<YOUR_PROJECT_ID>
export GOOGLE_CLOUD_LOCATION=us-central1
export GOOGLE_GENAI_USE_VERTEXAI=true

# Gemini Configuration
export GEMINI_ENABLED=true
export GEMINI_API_KEY="your-google-ai-api-key"
export GEMINI_MODEL="gemini-2.0-flash"
export GEMINI_MAX_TOKENS=4000
export GEMINI_TEMPERATURE=0.1

# Hardcoded Rules Configuration
export HARDCODED_RULES_ENABLED=true
```

## Contribution Process

### 1. Create a Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Follow the [Code Standards](#code-standards) below
- Add tests for new functionality
- Update documentation as needed
- Ensure all tests pass

### 3. Commit Your Changes

Use conventional commit messages:

```bash
git commit -m "feat: add new privacy rule for data retention"
git commit -m "fix: resolve timeout issue in AI scanning"
git commit -m "docs: update README with new configuration options"
```

### 4. Push and Create Merge Request

```bash
git push origin feature/your-feature-name
```

Then create a merge request on GitLab with:
- Clear description of changes
- Link to related issues
- Screenshots (if applicable)
- Test results

## Code Standards

### TypeScript Guidelines

- Use TypeScript for all new code
- Follow ESLint configuration
- Use meaningful variable and function names
- Add JSDoc comments for public APIs
- Keep functions small and focused

### File Structure

```
src/
├── ruleEngine/          # Privacy rule implementations
│   ├── rules/          # Individual rule files
│   └── RuleEngine.ts   # Main rule orchestrator
├── scanners/           # Language-specific scanners
├── index.ts           # Main entry point
└── types/             # TypeScript type definitions
```

### Naming Conventions

- **Files**: PascalCase for classes, camelCase for utilities
- **Classes**: PascalCase (e.g., `JavaScriptScanner`)
- **Functions**: camelCase (e.g., `scanFiles`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `IGNORED_PATHS`)
- **Interfaces**: PascalCase with 'I' prefix (e.g., `IScanner`)

### Documentation Standards

- Add comprehensive JSDoc comments to all public APIs
- Include examples in documentation
- Update README.md for user-facing changes
- Document new environment variables

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage
```

### Writing Tests

- Place tests in `__tests__/` directories
- Use descriptive test names
- Test both positive and negative cases
- Mock external dependencies
- Aim for >80% code coverage

### Test Structure

```typescript
describe('JavaScriptScanner', () => {
  describe('scanFiles', () => {
    it('should find JavaScript files in directory', async () => {
      // Test implementation
    });

    it('should skip ignored paths', async () => {
      // Test implementation
    });
  });
});
```

## Documentation

### Code Documentation

- Add JSDoc comments to all public functions and classes
- Include parameter types and return values
- Provide usage examples for complex functions
- Document error conditions and edge cases

### User Documentation

- Update README.md for new features
- Add configuration examples
- Include troubleshooting guides
- Provide integration examples

### API Documentation

- Document all public APIs
- Include parameter descriptions
- Provide return value documentation
- Add usage examples

## Areas for Contribution

### High Priority

- **New Privacy Rules**: Add rules for emerging privacy regulations
- **Language Support**: Add scanners for new programming languages
- **AI Enhancements**: Improve Gemini integration and prompts
- **Performance**: Optimize scanning speed for large codebases

### Medium Priority

- **Documentation**: Improve guides and examples
- **Testing**: Add more comprehensive test coverage
- **CI/CD**: Enhance GitLab and GitHub Actions integration
- **Error Handling**: Improve error messages and recovery

### Low Priority

- **UI Improvements**: Enhance console output formatting
- **Configuration**: Add more configuration options
- **Logging**: Improve logging and debugging capabilities
- **Examples**: Add more example projects and use cases

## License

By contributing to Privacy Guardian Agents, you agree that your contributions will be licensed under the MIT License with Commons Clause. See the [LICENSE](LICENSE) file for details.

### Developer Certificate of Origin

By contributing to Privacy Guardian Agents, you certify that:

1. The contribution was created in whole or in part by you and you have the right to submit it under the open source license indicated in the file; or
2. The contribution is based upon previous work that, to the best of your knowledge, is covered under an appropriate open source license and you have the right under that license to submit that work with modifications, whether created in whole or in part by you, under the same open source license (unless you are permitted to submit under a different license), as indicated in the file; or
3. The contribution was provided directly to you by some other person who certified (a), (b) or (c) and you have not modified it; or
4. You understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information you submit with it, including your sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.

## Contact

For questions about contributing to Privacy Guardian Agents:

- **Email**: nabanita@privacylicense.com
- **Website**: https://privacylicense.ai/

Thank you for contributing to Privacy Guardian Agents! 
