/**
 * 
 * 
  * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
* Licensed under the MIT License with the Commons Clause.
* This file is provided for personal, educational, and non-commercial use only.
* Commercial use including selling, sublicensing, internal deployment in for-profit
* environments, SaaS integration, or submission to hackathons, accelerators, or competitive evaluations—is strictly prohibited without a commercial license.
* 
* For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
* Commercial use is prohibited without a license.
* To request a Commercial License or integration approval, contact: nabanita@privacylicense.com | https://privacylicense.ai
* 
* 
 * DeveloperGuidanceRule - Real-time Developer Guidance and Privacy Impact Assessment
 * 
 * This rule provides real-time guidance to developers during the coding process,
 * offering IDE-like warnings and suggestions for privacy-violating code. It includes
 * privacy impact assessments and actionable guidance to help developers write
 * privacy-compliant code from the start.
 * 
 * Key Features:
 * - IDE-like warnings for privacy-violating code
 * - Privacy impact assessments for each violation
 * - Real-time suggestions for developers
 * - Actionable guidance with emojis and clear explanations
 * - Risk level indicators (High/Medium/Low impact)
 * - Best practices recommendations
 * 
 * Detection Capabilities:
 * - Privacy violation pattern recognition
 * - Code quality assessment for privacy compliance
 * - Risk level evaluation and categorization
 * - Developer experience optimization
 * - Educational content delivery
 * - Compliance guidance integration
 * 
 * Privacy Laws Addressed:
 * - GDPR: All articles with developer-focused guidance
 * - CCPA: All sections with practical implementation tips
 * - Regional privacy regulations
 * - Industry standards and best practices
 * - Security guidelines and recommendations
 * 
 * Guidance Features:
 * - Inline code suggestions
 * - Alternative implementation patterns
 * - Privacy-by-design principles
 * - Risk mitigation strategies
 * - Compliance verification steps
 * - Educational explanations
 * 
 * Usage:
 * This rule enhances the developer experience by providing immediate
 * feedback and guidance on privacy compliance. It helps developers
 * understand privacy requirements and implement compliant solutions
 * during the development process.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

export class DeveloperGuidanceRule implements Rule {
    id = "DEV001";
    description = "Real-time Developer Guidance and Privacy Impact Assessment";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Real-time developer guidance patterns
        const developerGuidancePatterns = [
            {
                pattern: /\b(?:new|create)\s+(?:user|person|customer|patient|employee)\s*\(/gi,
                type: "Object Creation with PII",
                guidance: "⚠️  Creating objects that may contain PII. Consider implementing privacy by design principles.",
                impact: "Medium - May lead to unnecessary data collection",
                suggestion: "Use data minimization - only collect fields that are absolutely necessary for the current operation."
            },
            {
                pattern: /\b(?:save|store|insert|update)\s+(?:user|person|customer|patient)_(?:data|info|details)/gi,
                type: "Data Storage Operation",
                guidance: "🔒  Storing personal data. Ensure you have proper consent and data retention policies.",
                impact: "High - Direct data storage operation",
                suggestion: "Implement data retention policies and ensure proper consent mechanisms are in place."
            },
            {
                pattern: /\b(?:send|email|sms|notification)\s*\(\s*[^)]*(?:user|person|customer|patient)[^)]*\)/gi,
                type: "Communication with PII",
                guidance: "📧  Sending communications with personal data. Verify consent and opt-out mechanisms.",
                impact: "Medium - Communication with personal data",
                suggestion: "Always include opt-out links and verify consent before sending communications."
            },
            {
                pattern: /\b(?:export|download|generate)\s+(?:report|data|file)\s+(?:with|containing)\s+(?:user|person|customer|patient)/gi,
                type: "Data Export with PII",
                guidance: "📊  Exporting data with personal information. Implement proper access controls and audit trails.",
                impact: "High - Data export operation",
                suggestion: "Implement role-based access controls and audit all data export activities."
            },
            {
                pattern: /\b(?:api|endpoint|route)\s*[:=]\s*['"`][^'"`]*(?:user|person|customer|patient)[^'"`]*['"`]/gi,
                type: "API Endpoint with PII",
                guidance: "🌐  API endpoint that handles personal data. Implement proper authentication and rate limiting.",
                impact: "High - API exposure of personal data",
                suggestion: "Implement proper authentication, authorization, and rate limiting. Consider API versioning."
            },
            {
                pattern: /\b(?:database|db|table)\s*[:=]\s*['"`][^'"`]*(?:user|person|customer|patient)[^'"`]*['"`]/gi,
                type: "Database Schema with PII",
                guidance: "🗄️  Database schema containing personal data. Implement proper encryption and access controls.",
                impact: "High - Database storage of personal data",
                suggestion: "Use encryption at rest and in transit. Implement proper database access controls."
            },
            {
                pattern: /\b(?:cache|redis|memcached)\s*[:=]\s*['"`][^'"`]*(?:user|person|customer|patient)[^'"`]*['"`]/gi,
                type: "Caching with PII",
                guidance: "⚡  Caching personal data. Implement proper cache expiration and encryption.",
                impact: "Medium - Cached personal data",
                suggestion: "Set appropriate cache expiration times and consider encrypting sensitive cached data."
            },
            {
                pattern: /\b(?:search|query|filter)\s*[:=]\s*['"`][^'"`]*(?:user|person|customer|patient)[^'"`]*['"`]/gi,
                type: "Search/Query with PII",
                guidance: "🔍  Searching or querying with personal data. Implement proper access controls and audit logging.",
                impact: "Medium - Search operations with personal data",
                suggestion: "Implement proper access controls and log all search queries for audit purposes."
            }
        ];

        lines.forEach((line, index) => {
            developerGuidancePatterns.forEach(({ pattern, type, guidance, impact, suggestion }) => {
                if (pattern.test(line)) {
                    violations.push({
                        line: index + 1,
                        match: `${type}: ${line.trim()}\n\n${guidance}\n\nPrivacy Impact: ${impact}\n\nDeveloper Suggestion: ${suggestion}`
                    });
                }
            });
        });
        
        return violations;
    }
} 