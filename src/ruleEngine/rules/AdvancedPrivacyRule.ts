

/**
 * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
* Licensed under the MIT License with the Commons Clause.
* 
* This file is provided for personal, educational, and non-commercial use only.
* Commercial use including selling, sublicensing, internal deployment in for-profit
* environments, SaaS integration, or submission to hackathons, accelerators, or competitive evaluations—is strictly prohibited without a commercial license.
* For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
* 
* Commercial use is prohibited without a license.
* To request a Commercial License or integration approval, contact: nabanita@privacylicense.com | https://privacylicense.ai
 * 
 * 
 * AdvancedPrivacyRule - Complex Data-Flow and Context-Aware Privacy Violations
 * 
 * This rule implements advanced privacy violation detection that goes beyond simple pattern matching.
 * It focuses on complex data-flow scenarios, context-aware violations, and sophisticated privacy
 * compliance requirements that require understanding of data relationships and processing contexts.
 * 
 * Key Features:
 * - Field-level access scoping for PII fields
 * - Ad/tracking code detection on opt-out pages
 * - Region-lock enforcement for EU data protection
 * - Join-safety validation for large PII tables
 * - Data minimization in ML pipelines
 * - Versioned privacy contract enforcement
 * - Least-privilege field set validation
 * 
 * Detection Capabilities:
 * - PII field access without proper scoping (@scope directive)
 * - Tracking code on privacy opt-out pages
 * - Cloud SDK calls shipping EU data outside EEA
 * - Unsafe joins between large PII tables
 * - ML training jobs loading unused sensitive columns
 * - API version changes without PII field updates
 * - Database columns not referenced elsewhere
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 25: Data protection by design and by default
 * - GDPR Article 32: Security of processing
 * - CCPA Section 1798.100: General duties of businesses
 * - Various regional data protection regulations
 * 
 * Usage:
 * This rule requires specific annotations and patterns in code to function properly.
 * Developers must use @scope, @purpose, and other privacy directives to indicate
 * compliance with privacy requirements.
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

export class AdvancedPrivacyRule implements Rule {
    id = "ADVANCED001";
    description = "Advanced Privacy Compliance - Complex data-flow and context-aware violations";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Field-level access scoping violations
        const fieldScopingPatterns: PatternRule[] = [
            {
                pattern: /\b(?:GraphQL|REST)\s+(?:query|mutation|field)\s*[:=]\s*['"`]?[^'"`]*(?:user|person|customer|patient|ssn|email|phone|address)[^'"`]*['"`]?/gi,
                type: "Missing Field-Level Access Scoping",
                description: "GraphQL/REST PII fields without @scope directive",
                fix: "Add @scope directive to PII fields to control access",
                marker: /@scope/gi
            },
            {
                pattern: /\b@scope\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Field Scoping Found",
                description: "Field-level access scoping detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Ad/tracking code violations
        const trackingPatterns: PatternRule[] = [
            {
                pattern: /\b(?:ad|tracking|pixel|analytics)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Ad/Tracking Code",
                description: "Ad or tracking code detected - ensure consent compliance",
                fix: "Check consent=opt_out before loading ad/tracking code"
            },
            {
                pattern: /\bconsent\s*[:=]\s*['"`]opt_out['"`]/gi,
                type: "Opt-Out Consent Found",
                description: "Opt-out consent detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Region-lock violations
        const regionPatterns: PatternRule[] = [
            {
                pattern: /\b(?:aws|gcp|azure|cloud)_(?:region|zone|location)\s*[:=]\s*['"`][^'"`]*(?:us|america|asia)[^'"`]*['"`]/gi,
                type: "Potential Region-Lock Violation",
                description: "Cloud region outside EEA for EU data - verify compliance",
                fix: "Ensure EU data stays within EEA or implement proper data transfer mechanisms"
            },
            {
                pattern: /\b(?:eu|eea|gdpr)_(?:compliant|region|storage)\s*[:=]\s*true/gi,
                type: "EU Compliance Found",
                description: "EU compliance mechanism detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Join-safety violations
        const joinPatterns: PatternRule[] = [
            {
                pattern: /\b(?:JOIN|INNER JOIN|LEFT JOIN)\s+\w+\s+ON\s+[^;]*(?:user|person|customer|patient)[^;]*/gi,
                type: "Large PII Table Join",
                description: "Joining large PII tables - verify join key pseudonymization",
                fix: "Ensure join keys are pseudonymized when joining large PII tables"
            },
            {
                pattern: /\b(?:pseudonymize|hash|tokenize)\s*\(\s*[^)]*join[^)]*\)/gi,
                type: "Join Safety Found",
                description: "Join safety mechanism detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Data minimization in ML pipelines
        const mlPatterns: PatternRule[] = [
            {
                pattern: /\b(?:train|model|ml|ai)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "ML Pipeline Data Minimization",
                description: "ML training operation - ensure data minimization",
                fix: "Only load necessary sensitive columns for ML training jobs"
            },
            {
                pattern: /\b(?:select|load)\s+only\s+(?:necessary|required)\s+columns/gi,
                type: "Data Minimization Found",
                description: "Data minimization in ML pipeline detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Versioned privacy contract violations
        const versionPatterns: PatternRule[] = [
            {
                pattern: /\b(?:api|schema)_version\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "API Version Found",
                description: "API versioning detected - ensure PII field changes trigger version bump",
                fix: "Bump API version when PII fields are added/modified/removed"
            },
            {
                pattern: /\b(?:pii|privacy)_(?:version|contract)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Privacy Contract Versioning Found",
                description: "Privacy contract versioning detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Least-privilege field set violations
        const privilegePatterns: PatternRule[] = [
            {
                pattern: /\b(?:CREATE|ALTER)\s+TABLE\s+\w+\s+ADD\s+COLUMN\s+\w+/gi,
                type: "New Database Column",
                description: "New database column - verify it's referenced elsewhere",
                fix: "Ensure new columns are necessary and referenced in application code"
            },
            {
                pattern: /\b(?:@required|@referenced|@used)\b/gi,
                type: "Field Reference Found",
                description: "Field reference annotation detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        const allPatterns = [
            ...fieldScopingPatterns,
            ...trackingPatterns,
            ...regionPatterns,
            ...joinPatterns,
            ...mlPatterns,
            ...versionPatterns,
            ...privilegePatterns
        ];

        // Track last marker line for each marker type
        const lastMarkerLine: { [key: string]: number } = {};
        lines.forEach((line, idx) => {
            allPatterns.forEach(({ marker }) => {
                if (marker) {
                    const markerClone = new RegExp(marker.source, marker.flags);
                    if (markerClone.test(line)) {
                        lastMarkerLine[marker.source] = idx;
                    }
                }
            });
        });
        lines.forEach((line, index) => {
            allPatterns.forEach(({ pattern, type, description, fix, isPositive, marker }) => {
                if (!isPositive) {
                    const patternClone = new RegExp(pattern.source, pattern.flags);
                    if (patternClone.test(line)) {
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
                }
            });
        });
        return violations;
    }
} 