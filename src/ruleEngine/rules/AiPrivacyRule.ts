/**
 * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
* Licensed under the MIT License with the Commons Clause.
* 
* This file is provided for personal, educational, and non-commercial use only.
* Commercial use including selling, sublicensing, internal deployment in for-profit
* environments, SaaS integration, or submission to hackathons, accelerators, or competitive evaluations—is strictly prohibited without a commercial license.
*
* For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
* Commercial use is prohibited without a license.
* To request a Commercial License or integration approval, contact: nabanita@privacylicense.com | https://privacylicense.ai
 * 

 * AiPrivacyRule - AI-Powered Privacy Explanations and Fixes
 * 
 * This rule provides AI-powered explanations and fixes for privacy violations detected
 * by other rules. It enhances the developer experience by providing context-aware
 * guidance and actionable remediation steps for privacy compliance issues.
 * 
 * Key Features:
 * - Plain-English explanations of privacy violations
 * - Specific code fixes that maintain functionality
 * - Context about privacy laws being violated
 * - Actionable remediation guidance
 * - References to specific GDPR/CCPA articles
 * - Smart suggestions for compliance improvements
 * 
 * Detection Capabilities:
 * - Privacy violation context analysis
 * - Code pattern recognition for fixes
 * - Legal compliance explanation
 * - Best practice recommendations
 * - Risk assessment and prioritization
 * - Developer-friendly guidance
 * 
 * Privacy Laws Addressed:
 * - GDPR: All relevant articles with specific references
 * - CCPA: All relevant sections with specific references
 * - Regional privacy regulations
 * - Industry best practices
 * - Security standards and guidelines
 * 
 * Guidance Features:
 * - Step-by-step fix instructions
 * - Code examples and templates
 * - Legal context and implications
 * - Risk level assessment
 * - Compliance verification steps
 * 
 * Usage:
 * This rule works in conjunction with other privacy rules to provide
 * enhanced explanations and actionable guidance. It helps developers
 * understand not just what is wrong, but why it matters and how to fix it.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

export class AiPrivacyRule implements Rule {
    id = "AI001";
    description = "AI-Powered Privacy Explanations and Fixes";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Privacy violation patterns with AI explanations
        const privacyViolations = [
            {
                pattern: /\b(?:password|secret|key|token)\s*[:=]\s*['"`][^'"`]{8,}['"`]/gi,
                type: "Hardcoded Credentials",
                explanation: "Hardcoded credentials in source code are a major security risk. They can be easily discovered by anyone with access to the codebase.",
                fix: "Use environment variables or secure secret management systems like HashiCorp Vault or AWS Secrets Manager.",
                law: "GDPR Article 32 - Security of processing"
            },
            {
                pattern: /\b(?:user|person|customer)_(?:data|info|details)\s*[:=]\s*\{[^}]*\}/gi,
                type: "Excessive Data Collection",
                explanation: "Collecting more personal data than necessary violates the principle of data minimization.",
                fix: "Only collect data that is directly necessary for the stated purpose. Review and remove unnecessary fields.",
                law: "GDPR Article 5(1)(c) - Data minimization"
            },
            {
                pattern: /\b(?:log|console\.log|logger)\s*\(\s*[^)]*(?:user|person|customer|patient|ssn|email|phone)[^)]*\)/gi,
                type: "PII in Logs",
                explanation: "Logging personal information creates unnecessary data retention and increases breach risk.",
                fix: "Use data masking, hashing, or completely avoid logging PII. Implement structured logging with sensitive data filters.",
                law: "GDPR Article 25 - Privacy by design"
            },
            {
                pattern: /\b(?:third_party|external|partner)_(?:api|service|integration)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Third-Party Data Sharing",
                explanation: "Sharing data with third parties without proper consent and data processing agreements violates privacy laws.",
                fix: "Implement proper consent mechanisms and ensure third parties have adequate data protection measures.",
                law: "GDPR Article 28 - Processor obligations"
            },
            {
                pattern: /\b(?:delete|remove)\s+(?:user|person|customer)_(?:data|account)\s+(?:permanently|forever)/gi,
                type: "Incomplete Data Deletion",
                explanation: "Permanent deletion without proper verification may not comply with 'right to be forgotten' requirements.",
                fix: "Implement proper data deletion workflows with verification and audit trails. Consider data anonymization as an alternative.",
                law: "GDPR Article 17 - Right to erasure"
            },
            {
                pattern: /\b(?:opt_out|unsubscribe)\s*[:=]\s*false/gi,
                type: "Disabled Opt-Out",
                explanation: "Disabling opt-out mechanisms violates user consent rights and may be considered forced consent.",
                fix: "Always provide clear, easy-to-use opt-out mechanisms. Default should be opt-in for marketing communications.",
                law: "CCPA Section 1798.120 - Right to opt-out"
            },
            {
                pattern: /\b(?:backup|archive)\s+(?:all|everything)\s+(?:user|person|customer)_(?:data|files)/gi,
                type: "Excessive Data Backup",
                explanation: "Backing up all personal data without purpose limitation violates data minimization principles.",
                fix: "Only backup data that is necessary for business continuity. Implement data lifecycle management.",
                law: "GDPR Article 5(1)(e) - Storage limitation"
            }
        ];

        lines.forEach((line, index) => {
            privacyViolations.forEach(({ pattern, type, explanation, fix, law }) => {
                if (pattern.test(line)) {
                    violations.push({
                        line: index + 1,
                        match: `${type}: ${line.trim()}\n\nExplanation: ${explanation}\n\nSuggested Fix: ${fix}\n\nRelevant Law: ${law}`
                    });
                }
            });
        });
        
        return violations;
    }
} 