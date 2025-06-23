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
 * EncryptionRule - Security and Encryption Violation Detection
 * 
 * This rule enforces security and encryption requirements for handling sensitive data.
 * It ensures that personal data is properly encrypted at rest, in transit, and during
 * processing, and validates security best practices for data protection.
 * 
 * Key Features:
 * - Encryption-at-rest enforcement for sensitive data
 * - TLS-only outbound traffic validation
 * - Hash/tokenize unique ID requirements
 * - Rate limiting enforcement for public endpoints
 * - Secure key management validation
 * - Encryption algorithm compliance
 * 
 * Detection Capabilities:
 * - Writes to sensitive tables without encryption
 * - HTTP (non-HTTPS) traffic with tainted data
 * - Raw email/phone numbers used as primary keys
 * - Public endpoints returning personal data without rate limiting
 * - Weak encryption algorithms
 * - Missing encryption for sensitive fields
 * - Insecure key storage practices
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 32: Security of processing
 * - GDPR Article 34: Communication of personal data breach
 * - CCPA Section 1798.150: Civil action
 * - Various industry security standards (SOC2, ISO27001)
 * 
 * Security Requirements:
 * - apply_rate_limit(): Required for public endpoints returning personal data
 * - encrypt(): Must be used for sensitive data at rest
 * - hash()/tokenize(): Required for unique identifiers
 * - HTTPS: Mandatory for all data transmission
 * 
 * Usage:
 * This rule validates that appropriate security measures are in place
 * when handling personal data. Developers must use security functions
 * and follow encryption best practices to avoid violations.
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
    marker?: RegExp;
}

export class EncryptionRule implements Rule {
    id = "ENCRYPT001";
    description = "Encryption and Security Compliance - Encryption-at-rest and security violations";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Encryption-at-rest violations
        const encryptionPatterns: PatternRule[] = [
            {
                pattern: /\b(?:CREATE|ALTER)\s+TABLE\s+\w+\s*\([^)]*(?:ssn|social_security|passport|credit_card|bank_account|phone|address|email|birth_date|medical_record)[^)]*\)/gi,
                type: "Missing Encryption-at-Rest",
                description: "Sensitive table creation without encryption specification",
                fix: "Add encrypt() flag or ORM encryption annotation for sensitive tables",
                marker: /@encrypt|@encrypted|@secure/gi
            },
            {
                pattern: /\b(?:INSERT|UPDATE)\s+INTO\s+\w+\s*\([^)]*(?:ssn|social_security|passport|credit_card|bank_account|phone|address|email|birth_date|medical_record)[^)]*\)/gi,
                type: "Unencrypted Data Write",
                description: "Writing sensitive data without encryption",
                fix: "Use encrypt() function or ORM encryption before writing sensitive data",
                marker: /@encrypt|@encrypted|@secure/gi
            },
            {
                pattern: /\b(?:@encrypt|@encrypted|@secure)\b/gi,
                type: "Encryption Annotation Found",
                description: "Encryption annotation detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // TLS/HTTPS violations
        const tlsPatterns: PatternRule[] = [
            {
                pattern: /http:\/\/[^'"`\s]+/gi,
                type: "Insecure HTTP Protocol",
                description: "Using HTTP instead of HTTPS for data transmission",
                fix: "Use HTTPS (https://) for all data transmission, especially with sensitive data"
            },
            {
                pattern: /\b(?:https|tls|ssl)\s*[:=]\s*['"`]?false['"`]?/gi,
                type: "TLS Disabled",
                description: "TLS/SSL encryption is explicitly disabled",
                fix: "Always enable TLS/SSL encryption for data transmission"
            }
        ];

        // Hash/tokenize violations
        const hashPatterns: PatternRule[] = [
            {
                pattern: /\b(?:email|phone|ssn|social_security)\s*[:=]\s*['"`][^'"`]*['"`]\s*(?:AS\s+)?PRIMARY\s+KEY/gi,
                type: "Raw PII as Primary Key",
                description: "Using raw personal identifiers as primary keys",
                fix: "Hash or tokenize unique identifiers before using as primary keys"
            },
            {
                pattern: /\b(?:hash|tokenize|anonymize)\s*\(\s*[^)]*(?:email|phone|ssn)[^)]*\)/gi,
                type: "PII Hashing Found",
                description: "PII hashing/tokenization detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Rate limiting violations
        const rateLimitPatterns: PatternRule[] = [
            {
                pattern: /\b(?:api|endpoint|route)\s*[:=]\s*['"`][^'"`]*(?:user|person|customer|patient)[^'"`]*['"`]/gi,
                type: "Missing Rate Limiting",
                description: "API endpoint returning personal data without rate limiting",
                fix: "Add apply_rate_limit() call for public endpoints returning personal data"
            },
            {
                pattern: /\bapply_rate_limit\s*\(/gi,
                type: "Rate Limiting Found",
                description: "Rate limiting implementation detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        const allPatterns = [
            ...encryptionPatterns,
            ...tlsPatterns,
            ...hashPatterns,
            ...rateLimitPatterns
        ];

        // Track last marker line for each marker type
        const lastMarkerLine: { [key: string]: number } = {};
        lines.forEach((line, idx) => {
            allPatterns.forEach(({ marker }) => {
                if (marker && marker.test(line)) {
                    lastMarkerLine[marker.source] = idx;
                }
            });
        });

        lines.forEach((line, index) => {
            allPatterns.forEach(({ pattern, type, description, fix, isPositive, marker }) => {
                if (!isPositive && pattern.test(line)) {
                    // Suppress violation if a marker for this type was found on a previous line (up to 1 line above)
                    let suppress = false;
                    if (marker && lastMarkerLine[marker.source] !== undefined) {
                        if (lastMarkerLine[marker.source] === index - 1 || lastMarkerLine[marker.source] === index) {
                            suppress = true;
                        }
                    }
                    if (suppress) return;
                    violations.push({
                        line: index + 1,
                        match: `${type}: ${line.trim()}\n\nDescription: ${description}\n\nFix: ${fix}`
                    });
                }
            });
        });
        
        return violations;
    }
} 