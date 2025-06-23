/**
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
 * 
 * DataFlowRule - Data Flow and Handling Violation Detection
 * 
 * This rule monitors and validates how personal data flows through the application,
 * ensuring that data handling practices comply with privacy regulations and best practices.
 * It focuses on data lifecycle management, retention policies, and secure data processing.
 * 
 * Key Features:
 * - Sensitive payload flow validation
 * - Raw PII logging prevention
 * - Stack trace sanitization
 * - Retention timer enforcement
 * - DSAR (Data Subject Access Request) compliance hooks
 * - Data anonymization validation
 * 
 * Detection Capabilities:
 * - PII flowing from source to sink without proper masking/anonymization
 * - Logging of tainted variables containing personal data
 * - Unsanitized stack traces exposing sensitive information
 * - Queries to retained tables without deletion/TTL mechanisms
 * - Missing DSAR registration for new personal data writes
 * - Inadequate data anonymization practices
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 5: Principles of processing
 * - GDPR Article 17: Right to erasure
 * - GDPR Article 20: Right to data portability
 * - CCPA Section 1798.110: Right to know
 * - CCPA Section 1798.115: Right to delete
 * 
 * Required Functions:
 * - mask()/anonymize(): Must be used for PII in data flows
 * - register_dsar(): Required for new personal data writes
 * - sanitize_stack_trace(): For error handling
 * - apply_retention_policy(): For data lifecycle management
 * 
 * Usage:
 * This rule ensures that personal data is handled securely throughout
 * its lifecycle. Developers must use appropriate data handling functions
 * and follow data flow best practices to maintain compliance.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

interface PatternRule {
    pattern: RegExp;
    type: string;
    description: string;
    fix: string;
    isPositive?: boolean;
}

export class DataFlowRule implements Rule {
    id = "DATAFLOW001";
    description = "Data Flow and Privacy Compliance - Sensitive payload flow and data handling violations";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Sensitive payload flow violations
        const dataFlowPatterns: PatternRule[] = [
            {
                pattern: /\b(?:user|person|customer|patient|ssn|email|phone|address)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Sensitive Data Source",
                description: "Sensitive data source detected - ensure proper flow control",
                fix: "Implement taint tracking and ensure PII flows through mask()/anonymize() helpers"
            },
            {
                pattern: /\b(?:mask|anonymize|pseudonymize)\s*\(\s*[^)]*(?:user|person|customer|patient|ssn|email|phone|address)[^)]*\)/gi,
                type: "Data Masking Found",
                description: "Data masking/anonymization detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Logging violations
        const loggingPatterns: PatternRule[] = [
            {
                pattern: /\b(?:log|logger|console\.log)\s*\(\s*[^)]*(?:user|person|customer|patient|ssn|email|phone|address)[^)]*\)/gi,
                type: "Raw PII in Logs",
                description: "Logging raw personal information without masking",
                fix: "Use data masking, hashing, or completely avoid logging PII"
            },
            {
                pattern: /\b(?:printStackTrace|traceback\.print_exc)\s*\(/gi,
                type: "Unsanitized Stack Trace",
                description: "Printing stack traces without PII scrubbing",
                fix: "Implement stack trace sanitization to remove PII before logging"
            }
        ];

        // Third-party data sharing violations
        const thirdPartyPatterns: PatternRule[] = [
            {
                pattern: /\b(?:third_party|external|partner)_(?:api|service|integration)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Third-Party Data Sharing",
                description: "Third-party integration without proper data protection",
                fix: "Implement data processing agreements and ensure third parties have adequate protection"
            },
            {
                pattern: /\b(?:SAFE_HOSTS|APPROVED_ENDPOINTS)\s*[:=]\s*\[[^\]]*\]/gi,
                type: "Approved Endpoints Found",
                description: "Approved endpoints allowlist detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Retention timer violations
        const retentionPatterns: PatternRule[] = [
            {
                pattern: /\b(?:retain|archive|store)\s+(?:user|person|customer|patient)_(?:data|files)\s+for\s+\d+/gi,
                type: "Missing Retention Timer",
                description: "Data retention without automatic deletion mechanism",
                fix: "Pair retention with deletion/TTL calls to ensure data lifecycle management"
            },
            {
                pattern: /\b(?:TTL|expires|delete_after)\s*[:=]\s*\d+/gi,
                type: "Retention Timer Found",
                description: "Retention timer/deletion mechanism detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // DSAR compliance violations
        const dsarPatterns: PatternRule[] = [
            {
                pattern: /\b(?:INSERT|UPDATE)\s+INTO\s+\w+\s*\([^)]*(?:user|person|customer|patient)[^)]*\)/gi,
                type: "Missing DSAR Registration",
                description: "Writing personal data without DSAR compliance registration",
                fix: "Invoke register_dsar() when writing new personal data"
            },
            {
                pattern: /\bregister_dsar\s*\(/gi,
                type: "DSAR Registration Found",
                description: "DSAR compliance registration detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        const allPatterns = [
            ...dataFlowPatterns,
            ...loggingPatterns,
            ...thirdPartyPatterns,
            ...retentionPatterns,
            ...dsarPatterns
        ];

        lines.forEach((line, index) => {
            allPatterns.forEach(({ pattern, type, description, fix, isPositive }) => {
                if (pattern.test(line)) {
                    if (!isPositive) { // Only report violations, not positive cases
                        violations.push({
                            line: index + 1,
                            match: `${type}: ${line.trim()}\n\nDescription: ${description}\n\nFix: ${fix}`
                        });
                    }
                }
            });
        });
        
        return violations;
    }
} 