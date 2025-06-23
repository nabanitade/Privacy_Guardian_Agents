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
 * GeminiPrivacyRule - AI-Powered Privacy Scanning with Google Gemini
 * 
 * This rule implements advanced AI-powered privacy violation detection using Google's Gemini model.
 * It provides intelligent, context-aware analysis of code to identify privacy violations that traditional
 * pattern-based rules might miss.
 * 
 * Key Features:
 * - Uses Google Gemini for intelligent privacy analysis
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
 * - GEMINI_ENABLED: Enable/disable AI scanning
 * - GEMINI_API_KEY: Your Google AI API key
 * - GEMINI_MODEL: Model to use (default: gemini-2.0-flash)
 * - GEMINI_MAX_TOKENS: Max tokens per request
 * - GEMINI_TEMPERATURE: AI creativity level
 * 
 * Usage:
 * This rule works in hybrid mode with hardcoded rules, providing enhanced accuracy
 * while maintaining reliability through fallback mechanisms.
 * 
 * @author Privacy Vulnerabilities Checker
 * @version 1.0.0
 */

import { Rule, Violation } from "./Rule";
import { GoogleGenAI } from '@google/genai';

const GOOGLE_CLOUD_PROJECT = process.env.GOOGLE_CLOUD_PROJECT;
const GOOGLE_CLOUD_LOCATION = process.env.GOOGLE_CLOUD_LOCATION || 'us-central1';
const GEMINI_MODEL = process.env.GEMINI_MODEL || 'gemini-2.0-flash';

interface GeminiConfig {
    enabled: boolean;
    model: string;
    maxTokens: number;
    temperature: number;
}

export class GeminiPrivacyRule implements Rule {
    id = "GEMINI001";
    description = "Google Gemini 2.0 Flash (Vertex AI) Privacy Scanning";
    private config: GeminiConfig;
    private ai: GoogleGenAI;
    private useVertexAI: boolean = true; // Default to Vertex AI

    constructor(config: Partial<GeminiConfig> = {}, apiKey?: string, vertexConfig?: { project: string; location: string }) {
        this.config = {
            enabled: config.enabled ?? false,
            model: config.model ?? GEMINI_MODEL,
            maxTokens: config.maxTokens ?? 4000,
            temperature: config.temperature ?? 0.1
        };
        if (apiKey) {
            this.useVertexAI = false;
            this.ai = new GoogleGenAI({ apiKey });
            process.stdout.write('🔑 GeminiPrivacyRule: Using Gemini API key mode\n');
        } else if (vertexConfig && vertexConfig.project) {
            this.useVertexAI = true;
            this.ai = new GoogleGenAI({
                vertexai: true,
                project: vertexConfig.project,
                location: vertexConfig.location || 'us-central1',
            });
            process.stdout.write('☁️ GeminiPrivacyRule: Using Vertex AI mode\n');
        } else if (process.env.GEMINI_API_KEY) {
            this.useVertexAI = false;
            this.ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
            process.stdout.write('🔑 GeminiPrivacyRule: Using Gemini API key mode (from env)\n');
        } else {
            this.useVertexAI = true;
            this.ai = new GoogleGenAI({
                vertexai: true,
                project: GOOGLE_CLOUD_PROJECT,
                location: GOOGLE_CLOUD_LOCATION,
            });
            process.stdout.write('☁️ GeminiPrivacyRule: Using Vertex AI mode (from env)\n');
        }
    }

    async evaluate(content: string, filePath?: string): Promise<Violation[]> {
        const violations: Violation[] = [];
        if (!this.config.enabled) {
            return violations;
        }
        try {
            const aiViolations = await this.scanWithGemini(content, filePath);
            return aiViolations;
        } catch (error) {
            console.warn(`Gemini scanning failed: ${error}. Falling back to hardcoded rules.`);
            return violations;
        }
    }

    private async scanWithGemini(content: string, filePath?: string): Promise<Violation[]> {
        const violations: Violation[] = [];
        const chunkSize = 200;
        const lines = content.split('\n');
        const fileName = filePath ? filePath.split('/').pop() || filePath : 'unknown file';
        process.stdout.write(`📄 Processing ${fileName} (${lines.length} lines) with ${this.useVertexAI ? 'Vertex AI' : 'Gemini API key'} in ${Math.ceil(lines.length / chunkSize)} chunks\n`);
        for (let i = 0; i < lines.length; i += chunkSize) {
            const chunkStart = i + 1;
            const chunkEnd = Math.min(i + chunkSize, lines.length);
            const chunk = lines.slice(i, chunkEnd).join('\n');
            
            if (chunk.trim().length === 0) {
                process.stdout.write(`⏭️  Skipping empty chunk in ${fileName} at lines ${chunkStart}-${chunkEnd}\n`);
                continue;
            }
            
            const codeLines = chunk.split('\n').filter(line => 
                line.trim().length > 0 && 
                !line.trim().startsWith('//') && 
                !line.trim().startsWith('/*') &&
                !line.trim().startsWith('*') &&
                !line.trim().startsWith('*/') &&
                !line.trim().startsWith('#') &&
                !line.trim().startsWith('<!--') &&
                !line.trim().startsWith('-->')
            );
            
            process.stdout.write(`🤖 Analyzing ${fileName} lines ${chunkStart}-${chunkEnd} (${chunkEnd - chunkStart + 1} total lines, ${codeLines.length} code lines)\n`);
            const chunkViolations = await this.analyzeChunk(chunk, chunkStart, fileName);
            violations.push(...chunkViolations);
        }
        process.stdout.write(`✅ Vertex AI analysis complete for ${fileName}. Found ${violations.length} AI-detected violations\n`);
        return violations;
    }

    private async analyzeChunk(content: string, startLine: number, fileName: string): Promise<Violation[]> {
        const prompt = this.buildPrompt(content);
        const startTime = Date.now();
        
        try {
            process.stdout.write(`   🔍 Starting AI analysis...\n`);
            
            const timeoutPromise = new Promise((_, reject) => {
                setTimeout(() => reject(new Error('Request timeout after 30 seconds')), 30000);
            });
            
            const responsePromise = this.ai.models.generateContent({
                model: this.config.model,
                contents: prompt
            });
            
            const response = await Promise.race([responsePromise, timeoutPromise]) as any;
            
            const responseText = response.text;
            if (!responseText) {
                process.stdout.write(`   ⚠️  No response text from Vertex AI for chunk at line ${startLine} in ${fileName}\n`);
                return [];
            }
            
            const duration = Date.now() - startTime;
            process.stdout.write(`   ✅ AI analysis completed in ${duration}ms\n`);
            
            const violations = this.parseGeminiResponse(responseText, startLine, fileName);
            process.stdout.write(`   📋 Found ${violations.length} violations in this chunk\n`);
            
            return violations;
        } catch (error) {
            const duration = Date.now() - startTime;
            const errorMessage = error instanceof Error ? error.message : String(error);
            process.stderr.write(`   ❌ Gemini Vertex AI call failed for chunk starting at line ${startLine} in ${fileName} after ${duration}ms: ${errorMessage}\n`);
            return [];
        }
    }

    private buildPrompt(content: string): string {
        return `
        
        You are a senior privacy-security auditor.  
Your task is to **statically review the following source code** and surface the **most impactful privacy or personal-data risks**.

📄  Code Snippet  
(lines 1-${content.split('\n').length})  
${content}

👁️‍🗨️  Review Scope  
Identify concrete issues in or caused by the code itself (not general policy/process gaps) that fall into ANY of the categories below.  
Group similar points into **at most 10 unique findings** ranked by severity > exploitability > regulatory risk.

1. Hard-coded or Plain-text PII / Secrets  
   – email, phone, SSN, CC, API keys, OAuth tokens, private keys, passwords, biometric templates, PHI, etc.  
2. Unsafe Logging & Debug Artefacts  
   – verbose logs containing identifiers, full request/response dumps, stack traces with tokens, un-redacted error traces.  
3. Consent & Transparency Defects  
   – data collected or transmitted without a lawful basis, opt-out/withdrawal missing, dark-patterned consent.  
4. Over-Collection & Data Minimisation Failure  
   – variables, DB columns, or API fields that store unused PII or collect beyond stated purpose.  
5. Data-Subject-Rights Gaps  
   – no path to delete/export/update user data; orphaned records after account deletion; immutable backups of PII.  
6. Security Misconfiguration  
   – HTTP rather than HTTPS, weak crypto (MD5, SHA-1, ECB), hard-coded hostnames, TLS bypass, missing HSTS.  
7. Third-Party / API Misuse  
   – sending raw PII to analytics, ads, or GPT endpoints; SDKs initialised before consent.  
8. Retention & Lifecycle Omissions  
   – infinite TTLs, localStorage caches, log rotation off, no expiration logic for PII blobs.  
9. Tracking & Cookie Non-Compliance  
   – cookies set before consent, fingerprinting JS, no Do-Not-Track honouring.  
10. Special-Category Data Mis-handling  
    – biometrics, health, children's data (<13 US / <16 EU) processed without safeguards.  
11. Cross-Border Transfer Risks  
    – code that uploads EU user data to non-adequacy regions w/o SCC, BCR, or explicit consent.  
12. Access Control & Least-Privilege Flaws  
    – SELECT *, missing tenant filters, unauthenticated endpoints, object-level auth issues.  
13. Weak Anonymisation / Re-ID Potential  
    – reversible hashing, truncation only, predictable pseudonyms.  
14. Regulatory References  
    – GDPR (Articles 5, 6, 15-22), CCPA/CPRA (§1798), HIPAA, PCI-DSS, ISO/IEC 27701, COPPA, etc.

⚙️  Output Format (JSON array)  
Return **ONLY** the JSON – no markdown, no commentary.

[
  {
    "id": "PV-1",
    "line": <int|[start,end]>,
    "category": "<one of the 14 scopes above>",
    "brief": "<≤120 chars>",
    "detail": "<actionable explanation (~1-2 sentences)>",
    "regulations": ["GDPR_Art6", "CCPA_§1798.120"],
    "severity": "HIGH | MEDIUM | LOW",
    "fix": "<single concise remediation step>"
  }
  …
]

Rules  
• Respect original line numbers (1-based). Use ranges if the issue spans multiple lines.  
• If multiple lines share the exact problem, merge them into one finding with a [start,end] range.  
• Map each finding to at least one relevant regulation (abbrev: GDPR_Art5, PCI_Req3, etc.).  
• Flag only *code-level* issues you can see; do not speculate on infrastructure.  
• If **no material risk** is present, return the empty array [].

────────────────────────────────────────
EXAMPLE OUTPUT
────────────────────────────────────────
[
  {
    "id": "PV-1",
    "line": 42,
    "category": "Hard-coded or Plain-text PII / Secrets",
    "brief": "AWS access key hard-coded",
    "detail": "The string 'AKIA.../wJ' is a live AWS key granting S3 full-access.",
    "regulations": ["ISO27001_A.9.2", "GDPR_Art32"],
    "severity": "HIGH",
    "fix": "Move key to env-secret manager (AWS Secrets Manager, Vault) and rotate immediately."
  },
  {
    "id": "PV-2",
    "line": [88,94],
    "category": "Unsafe Logging & Debug Artefacts",
    "brief": "Requests with full JWT logged",
    "detail": "Sensitive session tokens are printed to console, exposing auth in CloudWatch.",
    "regulations": ["GDPR_Art32", "CCPA_§1798.150"],
    "severity": "MEDIUM",
    "fix": "Mask or hash tokens before logging; set log level to WARN in production."
  }
]
.`;
    }

    private parseGeminiResponse(response: string, startLine: number, fileName: string): Violation[] {
        const violations: Violation[] = [];
        try {
            // Try to find JSON array in the response
            const jsonMatch = response.match(/\[[\s\S]*\]/);
            if (!jsonMatch) {
                console.warn(`No JSON array found in Gemini response for ${fileName}`);
                return violations;
            }

            let jsonString = jsonMatch[0];

            // Clean up the JSON string to handle escaped characters
            jsonString = jsonString.replace(/\\"/g, '"');
            jsonString = jsonString.replace(/\\n/g, ' ');
            jsonString = jsonString.replace(/\\t/g, ' ');
            jsonString = jsonString.replace(/\\r/g, ' ');
            // Additional cleaning for common JSON issues
            jsonString = jsonString.replace(/,\s*}/g, '}'); // Remove trailing commas
            jsonString = jsonString.replace(/,\s*]/g, ']'); // Remove trailing commas in arrays
            jsonString = jsonString.replace(/}\s*,\s*}/g, '}}'); // Fix double object endings
            jsonString = jsonString.replace(/]\s*,\s*]/g, ']]'); // Fix double array endings

            // Fix: Escape unescaped double quotes inside string values
            // This regex attempts to find unescaped quotes inside string values and escape them
            // It only targets values, not keys
            jsonString = jsonString.replace(/: "((?:[^"\\]|\\.)*)"/g, (match, p1) => {
                // Escape any unescaped double quotes in the value
                const fixed = p1.replace(/([^\\])"/g, '$1\\"');
                return `: "${fixed}"`;
            });

            try {
                const parsedViolations = JSON.parse(jsonString);

                for (const violation of parsedViolations) {
                    const lineNumber = violation.line;
                    const type = violation.type || violation.category || 'Privacy Violation';
                    const description = violation.description || violation.detail || violation.brief || 'Privacy violation detected';
                    const suggestedFix = violation.suggestedFix || violation.fix || 'Review and fix the privacy issue';
                    const severity = violation.severity || 'MEDIUM';

                    let actualLineNumber: number;
                    if (Array.isArray(lineNumber)) {
                        actualLineNumber = startLine + (lineNumber[0] - 1);
                    } else {
                        actualLineNumber = startLine + (parseInt(String(lineNumber)) - 1);
                    }

                    violations.push({
                        line: actualLineNumber,
                        match: `${type}: ${description}\n\nSuggested Fix: ${suggestedFix}\n\nSeverity: ${severity}`
                    });
                }
            } catch (parseError) {
                console.warn(`Failed to parse cleaned JSON for ${fileName}: ${parseError}`);
                console.warn(`Problematic JSON string: ${jsonString.substring(0, 200)}...`);
                // Try to extract any useful information from the response
                if (response.includes('undefined')) {
                    const lines = response.split('\n');
                    for (let i = 0; i < lines.length; i++) {
                        if (lines[i].includes('undefined')) {
                            violations.push({
                                line: startLine + i,
                                match: `Privacy Violation: Potential privacy issue detected\n\nSuggested Fix: Review this line for privacy compliance\n\nSeverity: MEDIUM`
                            });
                        }
                    }
                }
            }
        } catch (error) {
            console.warn(`Failed to parse Gemini response for ${fileName}: ${error}`);
            console.warn(`Raw response preview: ${response.substring(0, 300)}...`);
        }
        return violations;
    }

    setEnabled(enabled: boolean): void {
        this.config.enabled = enabled;
    }

    setApiKey(apiKey: string): void {
        this.useVertexAI = false;
        this.ai = new GoogleGenAI({
            apiKey: apiKey
        });
    }

    setVertexAIConfig(config: { project: string; location: string }): void {
        this.useVertexAI = true;
        this.ai = new GoogleGenAI({
            vertexai: true,
            project: config.project,
            location: config.location,
        });
    }

    isAvailable(): boolean {
        return this.config.enabled;
    }
} 