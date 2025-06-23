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
 * PiiRule - Basic Email Address Detection
 * 
 * This rule provides basic detection of email addresses in code. It serves as a
 * foundational rule for identifying personally identifiable information (PII)
 * in the form of email addresses that may be hardcoded or improperly exposed.
 * 
 * Key Features:
 * - Email address pattern recognition
 * - Hardcoded email detection
 * - Email exposure in code validation
 * - Basic PII protection enforcement
 * - Simple and reliable detection
 * 
 * Detection Capabilities:
 * - Standard email address formats
 * - Hardcoded email strings
 * - Email addresses in variable assignments
 * - Email addresses in configuration files
 * - Email addresses in comments or documentation
 * 
 * Privacy Laws Addressed:
 * - GDPR Article 4: Definitions (personal data)
 * - CCPA Section 1798.140: Definitions
 * - Basic privacy protection requirements
 * 
 * Pattern Recognition:
 * - Standard email regex pattern matching
 * - Context-aware email detection
 * - Suppression support for legitimate use cases
 * 
 * Usage:
 * This rule serves as a basic building block for PII detection,
 * focusing specifically on email addresses. It provides simple
 * and reliable detection of email-related privacy violations.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

export class PiiRule implements Rule {
    id = "PII001";
    description = "Avoid hardcoding email addresses";

    evaluate(content: string, filePath?: string): Violation[] {
        const violations: Violation[] = [];
        const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,}/g;
        const lines = content.split('\n');
        
        lines.forEach((line, index) => {
            let match;
            while ((match = emailRegex.exec(line)) !== null) {
                violations.push({
                    line: index + 1,
                    match: match[0]
                });
            }
        });
        
        return violations;
    }
}