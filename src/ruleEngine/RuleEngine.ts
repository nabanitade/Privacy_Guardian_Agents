/**
 * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
* Licensed under the MIT License modified with the Commons Clause.
* This file is provided for personal, educational, and non-commercial use only.
* Commercial use including selling, sublicensing, internal deployment in for-profit
* environments, SaaS integration, or submission to hackathons, accelerators, or competitive evaluations—is strictly prohibited without a commercial license.
* 
* For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
* Commercial use is prohibited without a license.
* To request a Commercial License or integration approval, contact: nabanita@privacylicense.com | https://privacylicense.ai
* 
 * RuleEngine - Core Privacy Scanning Engine
 * 
 * The RuleEngine is the central orchestrator of Privacy Guardian Agents's privacy violation detection system.
 * It manages a collection of privacy rules and scanners to provide comprehensive privacy compliance
 * analysis across multiple programming languages and file types.
 * 
 * Key Features:
 * - Orchestrates 10+ privacy rule engines for comprehensive violation detection
 * - Manages multi-language scanners for 12+ programming languages
 * - Provides hybrid AI + hardcoded rule scanning capabilities
 * - Implements robust fallback mechanisms for reliability
 * - Offers configurable scanning modes and rule management
 * 
 * Architecture:
 * - Rule-based detection using pattern matching and validation
 * - AI-enhanced analysis via Google Gemini (optional)
 * - Multi-language support through specialized scanners
 * - Hybrid approach combining traditional and AI-powered detection
 * 
 * Rule Types Managed:
 * - PII Detection: Email addresses, SSN, credit cards, phone numbers
 * - Privacy Policy: GDPR/CCPA compliance violations
 * - Consent Management: Explicit consent marker validation
 * - Encryption & Security: Data protection and encryption checks
 * - Data Flow: Sensitive data handling and retention
 * - Advanced Privacy: Complex data-flow and context-aware violations
 * - AI-Powered: Intelligent analysis and explanations
 * - Developer Guidance: Real-time privacy impact assessment
 * 
 * Supported Languages:
 * - JavaScript, TypeScript, Java, Python, Go, C#
 * - PHP, Ruby, Swift, Kotlin, Rust, Scala
 * 
 * Configuration Options:
 * - GEMINI_ENABLED: Enable/disable AI scanning
 * - HARDCODED_RULES_ENABLED: Enable/disable hardcoded rules
 * - GOOGLE_CLOUD_PROJECT: Vertex AI project configuration
 * - GEMINI_API_KEY: Google AI API key for direct access
 * 
 * Usage:
 * The RuleEngine processes code files through multiple rule engines,
 * combining traditional pattern-based detection with AI-powered analysis
 * to provide comprehensive privacy violation detection and remediation guidance.
 * 
 * Fallback System:
 * - Always runs hardcoded rules regardless of AI availability
 * - Gracefully falls back when AI services are unavailable
 * - Provides consistent results across different environments
 * - Maintains reliability in production deployments
 * 
 * @author Privacy Guardian Agents
 * @version 1.0.0
 * @since 2025-01-01
 */

import { Scanner } from "../scanners/Scanner";
import { Rule } from "./rules/Rule";
import { PiiRule } from "./rules/PiiRule";
import { PrivacyPolicyRule } from "./rules/PrivacyPolicyRule";
import { PiiDetectionRule } from "./rules/PiiDetectionRule";
import { AiPrivacyRule } from "./rules/AiPrivacyRule";
import { DeveloperGuidanceRule } from "./rules/DeveloperGuidanceRule";
import { GeminiPrivacyRule } from "./rules/GeminiPrivacyRule";
import { ConsentRule } from "./rules/ConsentRule";
import { EncryptionRule } from "./rules/EncryptionRule";
import { DataFlowRule } from "./rules/DataFlowRule";
import { AdvancedPrivacyRule } from "./rules/AdvancedPrivacyRule";

export class RuleEngine {
    constructor(private scanners: Scanner[]) {}

    private rules: Rule[] = [
        // Core PII Detection Rules
        new PiiRule(),
        new PiiDetectionRule(),
        
        // Privacy Policy and Compliance Rules
        new PrivacyPolicyRule(),
        new ConsentRule(),
        
        // Security and Encryption Rules
        new EncryptionRule(),
        
        // Data Flow and Handling Rules
        new DataFlowRule(),
        
        // Advanced Privacy Rules
        new AdvancedPrivacyRule(),
        
        // AI-Powered Rules
        new AiPrivacyRule(),
        new DeveloperGuidanceRule(),
        new GeminiPrivacyRule({ enabled: false }) // Disabled by default, can be enabled via config
    ];

    async run(projectPath: string): Promise<string[]> {
        const violations: string[] = [];

        for (const scanner of this.scanners) {
            const files = await scanner.scanFiles(projectPath);
            for (const file of files) {
                for (const rule of this.rules) {
                    const fileViolations = await rule.evaluate(file.content, file.path);
                    for (const violation of fileViolations) {
                        violations.push(
                            `[${scanner.language}] ${file.path}:${violation.line} - ${rule.description} (found: "${violation.match}")`
                        );
                    }
                }
            }
        }

        return violations;
    }

    // Method to enable/disable Gemini scanning
    setGeminiEnabled(enabled: boolean): void {
        const geminiRule = this.rules.find(rule => rule.id === "GEMINI001") as GeminiPrivacyRule;
        if (geminiRule) {
            geminiRule.setEnabled(enabled);
        }
    }

    // Method to set Gemini API key
    setGeminiApiKey(apiKey: string): void {
        const geminiRule = this.rules.find(rule => rule.id === "GEMINI001") as GeminiPrivacyRule;
        if (geminiRule && typeof geminiRule.setApiKey === 'function') {
            geminiRule.setApiKey(apiKey);
        }
    }

    // Method to set Vertex AI configuration
    setVertexAIConfig(config: { project: string; location: string }): void {
        const geminiRule = this.rules.find(rule => rule.id === "GEMINI001") as GeminiPrivacyRule;
        if (geminiRule) {
            geminiRule.setVertexAIConfig(config);
        }
    }

    // Method to check if Gemini is available
    isGeminiAvailable(): boolean {
        const geminiRule = this.rules.find(rule => rule.id === "GEMINI001") as GeminiPrivacyRule;
        return geminiRule ? geminiRule.isAvailable() : false;
    }

    // Method to get rule statistics
    getRuleStats(): { totalRules: number; ruleTypes: string[] } {
        return {
            totalRules: this.rules.length,
            ruleTypes: this.rules.map(rule => rule.description)
        };
    }
}