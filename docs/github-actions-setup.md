# GitHub Actions Setup Guide

## Overview

This guide explains how to set up the Privacy Vulnerabilities Checker with GitHub Actions for automated privacy scanning in your CI/CD pipeline.

## Features

The GitHub Actions workflow provides:

- **Automated privacy scanning** on every push and pull request
- **Multi-language support** (JavaScript, TypeScript, Java, Python, Go, C#, PHP, Ruby, Swift, Kotlin, Rust, Scala)
- **AI-enhanced analysis** using Google Gemini (optional)
- **Real-time PR comments** with privacy violation summaries
- **Automatic issue creation** for high-severity violations
- **Compliance reporting** with GDPR/CCPA status
- **Security scanning** with npm audit integration
- **Scheduled daily scans** for ongoing monitoring

## Quick Setup

### 1. Add the Workflow File

Copy the `.github/workflows/privacy-scan.yml` file to your repository.

### 2. Configure Secrets (Optional)

For AI-enhanced analysis, add these secrets in your GitHub repository:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Add the following secrets:

```
GEMINI_API_KEY=your-google-ai-api-key
```

### 3. Configure Environment Variables (Optional)

You can customize the workflow behavior by setting these environment variables in the workflow file:

```yaml
env:
  NODE_VERSION: '20'
  GEMINI_ENABLED: 'true'
  HARDCODED_RULES_ENABLED: 'true'
  PRIVACY_SCAN_TIMEOUT: '300'
  FAIL_ON_HIGH_SEVERITY: 'true'
  MAX_VIOLATIONS_THRESHOLD: '50'
```

## Workflow Jobs

### 1. Validate and Build
- Installs dependencies
- Builds the project
- Runs tests
- Uploads build artifacts

### 2. Privacy Vulnerability Scan
- Runs comprehensive privacy scanning
- Parses results and extracts violation counts
- Generates detailed reports
- Comments on pull requests
- Creates issues for high-severity violations
- Fails build on high-severity violations (configurable)

### 3. AI-Enhanced Privacy Analysis (Optional)
- Runs AI-powered analysis using Google Gemini
- Provides enhanced insights and explanations
- Comments AI analysis on pull requests
- Only runs if `GEMINI_API_KEY` secret is configured

### 4. Security Scan
- Runs npm security audit
- Identifies vulnerable dependencies
- Uploads security reports

### 5. Compliance Report
- Generates comprehensive compliance summary
- Shows GDPR/CCPA compliance status
- Provides actionable next steps
- Comments summary on pull requests

## Triggers

The workflow runs on:

- **Push** to main, develop, or feature branches
- **Pull requests** to main or develop branches
- **Scheduled** daily at 2 AM UTC

## Output Examples

### Pull Request Comment
```
## 🔍 Privacy Scan Summary

**Scan Date:** 2024-01-15 10:30:00 UTC
**Repository:** your-org/your-repo
**Branch:** feature/new-feature
**Commit:** abc123def456

## Results
- **Total Violations:** 5
- **High Severity:** 1
- **Medium Severity:** 2
- **Low Severity:** 2

## Detailed Report
```
📁 JAVASCRIPT FILES (3 violations)
1. src/userService.js:15 - Avoid hardcoding email addresses
2. src/userService.js:23 - Comprehensive PII Detection - SSN
3. src/userService.js:45 - Data Flow and Privacy Compliance
```

[View Full Report](artifact://privacy-scan-report.txt)
```

### AI Analysis Comment
```
## 🤖 AI-Enhanced Privacy Analysis

**Analysis completed using Google Gemini AI**

### Key Findings:
- Hardcoded email addresses detected in user service
- SSN validation missing proper encryption
- Data flow violations in user processing logic

[View Full AI Analysis](artifact://ai-privacy-analysis/ai-privacy-report.txt)
```

### Compliance Report
```
## Privacy & Security Compliance Report

**Repository:** your-org/your-repo
**Branch:** feature/new-feature
**Commit:** abc123def456
**Report Date:** 2024-01-15 10:30:00 UTC

## Scan Results Summary

### Privacy Scan
- **Status:** success
- **Violations:** 5

### Security Scan
- **Status:** success

### AI Analysis
- **Status:** success

## Compliance Status
- **GDPR Compliance:** ❌ Issues Found
- **CCPA Compliance:** ❌ Issues Found
- **Security Standards:** ✅ Compliant

## Next Steps
1. Review all privacy violations
2. Address high-severity issues
3. Implement suggested fixes
4. Re-run scan after fixes

[View Detailed Reports](artifact://reports/)
```

## Customization

### Modify Scan Behavior

Edit the workflow file to customize:

```yaml
# Change timeout for large codebases
PRIVACY_SCAN_TIMEOUT: '600'

# Disable build failure on high-severity violations
FAIL_ON_HIGH_SEVERITY: 'false'

# Adjust violation threshold
MAX_VIOLATIONS_THRESHOLD: '100'
```

### Add Custom Rules

The workflow uses your existing privacy rules. To add custom rules:

1. Add new rule files in `src/ruleEngine/rules/`
2. Import and register them in `src/ruleEngine/RuleEngine.ts`
3. Rebuild the project

### Integrate with Other Tools

You can extend the workflow to integrate with:

- **Slack notifications** for privacy violations
- **Jira ticket creation** for high-severity issues
- **Email alerts** for compliance failures
- **Custom reporting** tools

## Troubleshooting

### Common Issues

1. **Workflow fails to start**
   - Check that the workflow file is in `.github/workflows/`
   - Verify YAML syntax is correct

2. **No violations detected**
   - Ensure your code contains test files
   - Check that file extensions are supported
   - Verify the scanner is finding your files

3. **AI analysis not running**
   - Check that `GEMINI_API_KEY` secret is set
   - Verify the API key is valid
   - Check GitHub Actions logs for errors

4. **Timeout errors**
   - Increase `PRIVACY_SCAN_TIMEOUT` for large codebases
   - Consider scanning specific directories instead of entire repo

### Debug Mode

To enable debug output, add this to your workflow:

```yaml
- name: Run privacy scan with debug
  run: |
    echo "🔍 Starting comprehensive privacy vulnerability scan..."
    DEBUG=* timeout ${{ env.PRIVACY_SCAN_TIMEOUT }} npm start . || {
      echo "⚠️ Privacy scan timed out, but continuing with results..."
    }
```

## Best Practices

1. **Start with hardcoded rules only** - Add AI analysis later
2. **Set appropriate timeouts** for your codebase size
3. **Review violation thresholds** based on your project needs
4. **Use branch protection rules** to require privacy scans
5. **Regularly review and update** privacy rules
6. **Monitor compliance reports** for trends

## Support

For issues with the GitHub Actions workflow:

1. Check the GitHub Actions logs
2. Review the troubleshooting section above
3. Open an issue in the repository
4. Contact the development team

## Security Considerations

- **API keys** are stored as GitHub secrets and are encrypted
- **Scan results** are uploaded as artifacts with configurable retention
- **No code or data** is sent to third parties except Google Vertex AI (when enabled)
- **All scanning** happens in GitHub's secure runner environment 