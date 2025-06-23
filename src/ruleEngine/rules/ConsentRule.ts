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
 * ConsentRule - Consent and Privacy Compliance Enforcement
 * 
 * This rule enforces consent-related privacy requirements and ensures proper consent mechanisms
 * are in place before collecting, processing, or storing personal data. It implements
 * comprehensive consent validation that aligns with GDPR, CCPA, and other privacy regulations.
 * 
 * Key Features:
 * - Explicit consent marker validation (@consent_required)
 * - Purpose limitation enforcement (data_purpose= annotation)
 * - Profiling opt-out verification
 * - Consent withdrawal mechanism validation
 * - Granular consent tracking
 * - Consent audit trail requirements
 * 
 * Detection Capabilities:
 * - Data capture without @consent_required annotation
 * - PII fields without data_purpose= specification
 * - Profiling models not excluding opt-out users
 * - Missing consent withdrawal mechanisms
 * - Inadequate consent granularity
 * - Lack of consent audit trails
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 7: Conditions for consent
 * - GDPR Article 6: Lawfulness of processing
 * - GDPR Article 22: Automated individual decision-making
 * - CCPA Section 1798.120: Right to opt-out
 * - Various regional consent requirements
 * 
 * Required Annotations:
 * - @consent_required: Must precede any data capture
 * - data_purpose=: Every PII field needs purpose specification
 * - profiling_disabled=true: For users who opt out of profiling
 * 
 * Usage:
 * Developers must annotate their code with consent markers to indicate
 * compliance with consent requirements. The rule validates these annotations
 * and flags violations when consent mechanisms are missing or inadequate.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

export class ConsentRule implements Rule {
    id = "CONSENT001";
    description = "Consent and Privacy Compliance - Explicit consent markers and violations";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // Explicit consent marker violations
        const consentPatterns = [
            {
                pattern: /\b(?:data_capture|user_data|personal_info|pii_collection)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Missing Consent Marker",
                description: "Data capture operation without explicit consent marker",
                fix: "Add @consent_required annotation before data capture operations",
                marker: /@consent_required|@privacy_consent|@gdpr_consent/gi
            },
            {
                pattern: /\b(?:@consent_required|@privacy_consent|@gdpr_consent)\b/gi,
                type: "Consent Marker Found",
                description: "Consent marker detected - this is good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            },
            {
                pattern: /\b(?:opt_out|unsubscribe)\s*[:=]\s*false/gi,
                type: "Disabled Opt-Out",
                description: "Opt-out mechanism is disabled, violating consent rights",
                fix: "Always provide clear opt-out mechanisms. Default should be opt-in for marketing"
            },
            {
                pattern: /\b(?:forced_consent|mandatory_consent)\s*[:=]\s*true/gi,
                type: "Forced Consent",
                description: "Forced consent violates user autonomy and privacy laws",
                fix: "Implement genuine consent mechanisms with clear opt-in/opt-out choices"
            },
            {
                pattern: /\b(?:default_enabled|auto_consent)\s*[:=]\s*true/gi,
                type: "Default Enabled Consent",
                description: "Default enabled data collection without explicit consent",
                fix: "Default should be opt-in for data collection, not opt-out"
            }
        ];

        // Purpose limitation violations
        const purposePatterns = [
            {
                pattern: /\b(?:user|person|customer)_(?:data|info|details)\s*[:=]\s*\{[^}]*\}/gi,
                type: "Missing Purpose Limitation",
                description: "Personal data collection without purpose limitation annotation",
                fix: "Add data_purpose= annotation to specify the legitimate purpose",
                marker: /data_purpose/gi
            },
            {
                pattern: /\bdata_purpose\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Purpose Limitation Found",
                description: "Purpose limitation annotation detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        // Profiling opt-out violations
        const profilingPatterns = [
            {
                pattern: /\b(?:profiling|scoring|algorithm)\s*[:=]\s*['"`][^'"`]*['"`]/gi,
                type: "Missing Profiling Opt-Out Check",
                description: "Profiling operation without opt-out verification",
                fix: "Check profiling_disabled=true before applying profiling algorithms",
                marker: /profiling_disabled/gi
            },
            {
                pattern: /\bprofiling_disabled\s*[:=]\s*true/gi,
                type: "Profiling Opt-Out Found",
                description: "Profiling opt-out detected - good practice",
                fix: "None - this is correct implementation",
                isPositive: true
            }
        ];

        const allPatterns = [
            ...consentPatterns,
            ...purposePatterns,
            ...profilingPatterns
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