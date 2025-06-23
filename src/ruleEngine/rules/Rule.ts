

/**
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
 * Rule - Base Interface for Privacy Violation Detection Rules
 * 
 * This file defines the base interface and types for all privacy violation detection rules
 * in the Privacy Vulnerabilities Checker. It provides the foundational structure that
 * all specific privacy rules must implement.
 * 
 * Key Components:
 * - Rule interface: Base contract for all privacy rules
 * - Violation interface: Structure for detected privacy violations
 * - PatternRule interface: Extended interface for pattern-based rules
 * - Common types and utilities for rule implementation
 * 
 * Interface Features:
 * - Standardized rule structure for consistency
 * - Violation reporting format
 * - Pattern matching capabilities
 * - Suppression and marker support
 * - Extensible design for new rule types
 * 
 * Usage:
 * All privacy rules extend this base interface to ensure consistent
 * behavior and reporting across the entire rule engine. This provides
 * a unified approach to privacy violation detection and reporting.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

export interface Violation {
    line: number;
    match: string;
}

export interface Rule {
    id: string;
    description: string;
    evaluate(content: string, filePath?: string): Violation[] | Promise<Violation[]>;
}