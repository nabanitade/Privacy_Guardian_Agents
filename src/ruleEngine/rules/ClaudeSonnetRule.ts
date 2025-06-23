/**
 * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
* Licensed under the MIT License with the Commons Clause.
* 
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
 * 
 * ClaudeSonnetRule - AI-Powered Privacy Scanning with Claude Sonnet 4
 * 
 * This rule implements advanced AI-powered privacy violation detection using Anthropic's Claude Sonnet 4 model.
 * It provides intelligent, context-aware analysis of code to identify privacy violations that traditional
 * pattern-based rules might miss.
 * 
 * Key Features:
 * - Uses Claude Sonnet 4 for intelligent privacy analysis
 * - Provides detailed explanations with specific fixes
 * - References relevant privacy laws (GDPR, CCPA, etc.)
 * - Includes severity levels and actionable guidance
 * - Falls back gracefully if AI is unavailable
 * - Configurable via environment variables
 * 
 * Detection Capabilities:
 * - Hardcoded PII and sensitive data
 * - Privacy policy violations
 * - Data handling compliance issues
 * - Security vulnerabilities
 * - Consent mechanism violations
 * - Data flow and retention issues
 * 
 * Configuration:
 * - CLAUDE_ENABLED: Enable/disable AI scanning
 * - CLAUDE_API_KEY: Your Claude API key
 * - CLAUDE_MODEL: Model to use (default: claude-sonnet-4-20250514)
 * - CLAUDE_MAX_TOKENS: Max tokens per request
 * - CLAUDE_TEMPERATURE: AI creativity level
 * 
 * Usage:
 * This rule works in hybrid mode with hardcoded rules, providing enhanced accuracy
 * while maintaining reliability through fallback mechanisms.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";

interface ClaudeSonnetConfig {
    enabled: boolean;
    apiKey?: string;
    model: string;
    maxTokens: number;
    temperature: number;
}

export class ClaudeSonnetRule implements Rule {
    id = "CLAUDE001";
    description = "Claude Sonnet AI-Powered Privacy Scanning";
    private config: ClaudeSonnetConfig;

    constructor(config: Partial<ClaudeSonnetConfig> = {}) {
        this.config = {
            enabled: config.enabled ?? false,
            apiKey: config.apiKey ?? process.env.CLAUDE_API_KEY,
            model: config.model ?? "claude-sonnet-4-20250514",
            maxTokens: config.maxTokens ?? 4000,
            temperature: config.temperature ?? 0.1
        };
    }

    async evaluate(content: string): Promise<Violation[]> {
        const violations: Violation[] = [];
        
        // If Claude Sonnet is disabled, return empty violations (fallback to hardcoded rules)
        if (!this.config.enabled || !this.config.apiKey) {
            return violations;
        }

        try {
            const aiViolations = await this.scanWithClaude(content);
            return aiViolations;
        } catch (error) {
            console.warn(`Claude Sonnet scanning failed: ${error}. Falling back to hardcoded rules.`);
            return violations; // Return empty to allow fallback
        }
    }

    private async scanWithClaude(content: string): Promise<Violation[]> {
        const lines = content.split('\n');
        const violations: Violation[] = [];

        // Process content in chunks to avoid token limits
        const chunkSize = 50; // lines per chunk
        for (let i = 0; i < lines.length; i += chunkSize) {
            const chunk = lines.slice(i, i + chunkSize).join('\n');
            const chunkViolations = await this.analyzeChunk(chunk, i + 1);
            violations.push(...chunkViolations);
        }

        return violations;
    }

    private async analyzeChunk(content: string, startLine: number): Promise<Violation[]> {
        const prompt = this.buildPrompt(content);
        
        try {
            const response = await this.callClaudeAPI(prompt);
            return this.parseClaudeResponse(response, startLine);
        } catch (error) {
            console.warn(`Claude API call failed for chunk starting at line ${startLine}: ${error}`);
            return [];
        }
    }

    private buildPrompt(content: string): string {
        return `You are a privacy compliance expert. Analyze the following code for privacy violations and PII exposure.

Code to analyze:
\`\`\`
${content}
\`\`\`

Please identify any privacy violations, PII exposure, or compliance issues. For each violation found, provide:

1. Line number (relative to the provided code)
2. Type of violation (e.g., "Hardcoded PII", "GDPR Violation", "CCPA Violation", "Data Minimization", "Consent Issue", etc.)
3. Description of the issue
4. Suggested fix
5. Relevant privacy law/regulation

Format your response as JSON array:
[
  {
    "line": <line_number>,
    "type": "<violation_type>",
    "description": "<detailed_description>",
    "suggestedFix": "<specific_fix>",
    "relevantLaw": "<law_or_regulation>",
    "severity": "<HIGH|MEDIUM|LOW>"
  }
]

If no violations are found, return an empty array [].

Focus on:
- Hardcoded personal information (SSN, credit cards, addresses, etc.)
- GDPR violations (right to be forgotten, data minimization, consent)
- CCPA violations (do not sell, opt-out mechanisms)
- Privacy by design violations
- Data flow and logging issues
- API and database security issues
- Biometric data handling
- Medical data exposure`;
    }

    private async callClaudeAPI(prompt: string): Promise<string> {
        const response = await fetch('https://api.anthropic.com/v1/messages', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${this.config.apiKey}`,
                'anthropic-version': '2023-06-01'
            },
            body: JSON.stringify({
                model: this.config.model,
                max_tokens: this.config.maxTokens,
                temperature: this.config.temperature,
                messages: [
                    {
                        role: 'user',
                        content: prompt
                    }
                ]
            })
        });

        if (!response.ok) {
            throw new Error(`Claude API error: ${response.status} ${response.statusText}`);
        }

        const data = await response.json();
        return data.content[0].text;
    }

    private parseClaudeResponse(response: string, startLine: number): Violation[] {
        const violations: Violation[] = [];

        try {
            // Extract JSON from response (handle potential markdown formatting)
            const jsonMatch = response.match(/\[[\s\S]*\]/);
            if (!jsonMatch) {
                return violations;
            }

            const parsedViolations = JSON.parse(jsonMatch[0]);
            
            for (const violation of parsedViolations) {
                violations.push({
                    line: startLine + (violation.line - 1), // Adjust for chunk offset
                    match: `${violation.type}: ${violation.description}\n\nSuggested Fix: ${violation.suggestedFix}\n\nRelevant Law: ${violation.relevantLaw}\n\nSeverity: ${violation.severity}`
                });
            }
        } catch (error) {
            console.warn(`Failed to parse Claude response: ${error}`);
        }

        return violations;
    }

    // Method to enable/disable Claude Sonnet scanning
    setEnabled(enabled: boolean): void {
        this.config.enabled = enabled;
    }

    // Method to update API key
    setApiKey(apiKey: string): void {
        this.config.apiKey = apiKey;
    }

    // Method to check if Claude Sonnet is available
    isAvailable(): boolean {
        return this.config.enabled && !!this.config.apiKey;
    }
} 