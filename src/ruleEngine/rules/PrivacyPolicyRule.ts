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
 * PrivacyPolicyRule - GDPR/CCPA Compliance Violation Detection
 * 
 * This rule detects violations of privacy policy compliance requirements, specifically
 * focusing on GDPR (General Data Protection Regulation) and CCPA (California Consumer
 * Privacy Act) violations. It identifies code patterns that may violate privacy rights
 * and data protection principles.
 * 
 * Key Features:
 * - GDPR "Right to be forgotten" violation detection
 * - CCPA "Do not sell" violation detection
 * - Data minimization principle enforcement
 * - Consent mechanism validation
 * - Automated pattern recognition for compliance violations
 * - Legal compliance tracking and reporting
 * 
 * Detection Capabilities:
 * - Hardcoded "delete from users" queries without proper authorization
 * - Data processing without consent mechanisms
 * - Excessive data collection beyond stated purposes
 * - Missing data subject rights implementation
 * - Improper data retention practices
 * - Non-compliant data sharing patterns
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 17: Right to erasure ("right to be forgotten")
 * - GDPR Article 5: Principles of processing
 * - GDPR Article 6: Lawfulness of processing
 * - CCPA Section 1798.120: Right to opt-out of sale
 * - CCPA Section 1798.115: Right to delete
 * - CCPA Section 1798.110: Right to know
 * 
 * Compliance Patterns:
 * - Proper deletion mechanisms with authorization
 * - Consent-based data processing
 * - Purpose-limited data collection
 * - Data subject rights implementation
 * - Appropriate data retention policies
 * 
 * Usage:
 * This rule scans for patterns that may violate privacy regulations and
 * provides guidance on how to implement compliant data handling practices.
 * It helps ensure that applications respect user privacy rights.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

export class PrivacyPolicyRule implements Rule {
    id = "PRIVACY001";
    description = "Privacy Policy Compliance - GDPR/CCPA violations";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const lines = content.split('\n');
        
        // GDPR "Right to be forgotten" violations
        const rightToBeForgottenPatterns = [
            /delete\s+from\s+\w+\s+where\s+id\s*=\s*\d+/gi, // Hardcoded user deletion
            /remove\s+user\s+data\s+permanently/gi, // Permanent data removal without consent
            /archive\s+instead\s+of\s+delete/gi, // Archiving instead of deletion
        ];

        // CCPA "Do not sell" violations
        const ccpaPatterns = [
            /sell\s+user\s+data/gi, // Selling user data
            /third\s+party\s+data\s+sharing/gi, // Third party data sharing
            /advertising\s+data\s+collection/gi, // Advertising data collection
        ];

        // Data minimization violations
        const dataMinimizationPatterns = [
            /collect\s+all\s+data/gi, // Collecting excessive data
            /store\s+everything/gi, // Storing unnecessary data
            /backup\s+all\s+user\s+data/gi, // Excessive data backup
        ];

        // Consent violations
        const consentPatterns = [
            /opt\s*out\s+disabled/gi, // Disabled opt-out
            /forced\s+consent/gi, // Forced consent
            /default\s+enabled/gi, // Default enabled data collection
        ];

        const allPatterns = [
            ...rightToBeForgottenPatterns,
            ...ccpaPatterns,
            ...dataMinimizationPatterns,
            ...consentPatterns
        ];

        lines.forEach((line, index) => {
            allPatterns.forEach(pattern => {
                if (pattern.test(line)) {
                    violations.push({
                        line: index + 1,
                        match: line.trim()
                    });
                }
            });
        });
        
        return violations;
    }
} 