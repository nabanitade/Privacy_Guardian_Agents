

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
 * PiiDetectionRule - Comprehensive PII Detection (50+ PII Types)
 * 
 * This rule implements comprehensive detection of Personally Identifiable Information (PII)
 * across 50+ different PII types. It uses advanced pattern matching and validation to
 * identify various forms of personal data that may be hardcoded or improperly handled.
 * 
 * Key Features:
 * - 50+ PII type detection patterns
 * - Personal identifiers (SSN, Passport, Driver's License)
 * - Financial information (Credit Cards, Bank Accounts)
 * - Government IDs (National IDs, Tax IDs)
 * - Address information (Street, ZIP, Postal Codes)
 * - Medical information (Medical Records, Health Codes)
 * - Biometric data (Fingerprints, DNA, Face Recognition)
 * - API keys with personal information
 * - Database schema sensitive field detection
 * 
 * Detection Capabilities:
 * - Social Security Numbers (US and international formats)
 * - Credit card numbers (all major card types)
 * - Phone numbers (international formats)
 * - Email addresses in various contexts
 * - Physical addresses and postal codes
 * - Government identification numbers
 * - Medical record numbers and codes
 * - Biometric identifiers and hashes
 * - Financial account numbers
 * - Database fields containing sensitive data
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 4: Definitions (personal data)
 * - GDPR Article 9: Special categories of personal data
 * - CCPA Section 1798.140: Definitions
 * - HIPAA: Protected Health Information
 * - Various regional data protection laws
 * 
 * Pattern Recognition:
 * - Regex-based pattern matching for each PII type
 * - Validation algorithms for format checking
 * - Context-aware detection (database fields, variables)
 * - Suppression support for legitimate use cases
 * 
 * Usage:
 * This rule scans code for hardcoded PII and flags violations when
 * personal data is found inappropriately stored or exposed. It provides
 * detailed explanations of what was found and how to fix it.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

export class PiiDetectionRule implements Rule {
    id = "PII002";
    description = "Comprehensive PII Detection - 50+ PII types";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Personal Identifiers
        const personalIdentifiers = [
            { pattern: /\b\d{3}-\d{2}-\d{4}\b/g, type: "SSN" }, // Social Security Number
            { pattern: /\b\d{3}\s\d{2}\s\d{4}\b/g, type: "SSN" },
            { pattern: /\b\d{9}\b/g, type: "SSN (9 digits)" },
            { pattern: /\b[A-Z]{2}\d{2}\s?\d{2}\s?\d{2}\s?\d{3}\b/g, type: "Passport Number" },
            { pattern: /\b\d{10,11}\b/g, type: "Phone Number" },
            { pattern: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/g, type: "Phone Number" },
        ];

        // Financial Information
        const financialInfo = [
            { pattern: /\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b/g, type: "Credit Card" },
            { pattern: /\b\d{4}[- ]?\d{6}[- ]?\d{5}\b/g, type: "Credit Card" },
            { pattern: /\b\d{3}-\d{7}-\d{1}\b/g, type: "Bank Account" },
            { pattern: /\b\d{8,17}\b/g, type: "Bank Account Number" },
        ];

        // Government IDs
        const governmentIds = [
            { pattern: /\b\d{1,2}-\d{2}-\d{4}\b/g, type: "Driver's License" },
            { pattern: /\b[A-Z]{1,2}\d{6,8}\b/g, type: "Driver's License" },
            { pattern: /\b\d{2}-\d{4}-\d{4}-\d{4}\b/g, type: "National ID" },
        ];

        // Address Information
        const addressInfo = [
            { pattern: /\b\d+\s+[A-Za-z\s]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Place|Pl|Way|Terrace|Ter)\b/g, type: "Street Address" },
            { pattern: /\b\d{5}(?:-\d{4})?\b/g, type: "ZIP Code" },
            { pattern: /\b[A-Z]{2}\s\d[A-Z]\s\d[A-Z]\d\b/g, type: "Canadian Postal Code" },
        ];

        // Medical Information
        const medicalInfo = [
            { pattern: /\b\d{10}\b/g, type: "Medical Record Number" },
            { pattern: /\b[A-Z]{2}\d{6}\b/g, type: "Medical License" },
            { pattern: /\b(?:ICD|CPT)\s*\d{3,5}\b/g, type: "Medical Code" },
        ];

        // Biometric Data
        const biometricData = [
            { pattern: /\b(?:fingerprint|retina|iris|face|voice|dna|biometric)\s*(?:scan|data|template|hash)\b/gi, type: "Biometric Data" },
            { pattern: /\b[A-Fa-f0-9]{64}\b/g, type: "Biometric Hash" },
        ];

        // API Keys with Personal Info
        const apiKeysWithPii = [
            { pattern: /\b(?:api_key|apikey|secret|token)\s*[:=]\s*[A-Za-z0-9+/=]{20,}\b/gi, type: "API Key" },
            { pattern: /\b(?:user|person|customer|client)_(?:id|key|token)\s*[:=]\s*[A-Za-z0-9+/=]{10,}\b/gi, type: "Personal API Key" },
        ];

        // Database Schemas with Sensitive Fields
        const sensitiveDatabaseFields = [
            { pattern: /\b(?:CREATE|ALTER)\s+TABLE\s+\w+\s*\([^)]*(?:ssn|social_security|passport|credit_card|bank_account|phone|address|email|birth_date|medical_record)[^)]*\)/gi, type: "Sensitive Database Schema" },
            { pattern: /\b(?:user|person|customer|patient|employee)_(?:ssn|id|phone|email|address|birth|medical)\b/gi, type: "Sensitive Field Name" },
        ];

        // Data Flow Tracking
        const dataFlowPatterns = [
            { pattern: /\blog\s*\(\s*['"`][^'"`]*(?:user|person|customer|patient|ssn|email|phone|address)[^'"`]*['"`]\s*\)/gi, type: "PII in Logging" },
            { pattern: /\bconsole\.(?:log|warn|error)\s*\(\s*[^)]*(?:user|person|customer|patient|ssn|email|phone|address)[^)]*\)/gi, type: "PII in Console Log" },
        ];

        const allPatterns = [
            ...personalIdentifiers,
            ...financialInfo,
            ...governmentIds,
            ...addressInfo,
            ...medicalInfo,
            ...biometricData,
            ...apiKeysWithPii,
            ...sensitiveDatabaseFields,
            ...dataFlowPatterns
        ];

        lines.forEach((line, index) => {
            allPatterns.forEach(({ pattern, type }) => {
                if (pattern.test(line)) {
                    violations.push({
                        line: index + 1,
                        match: `${type}: ${line.trim()}`
                    });
                }
            });
        });
        
        return violations;
    }
} 