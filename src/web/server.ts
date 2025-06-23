// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

import express from 'express';
import multer from 'multer';
import * as path from 'path';
import * as fs from 'fs';
import { RuleEngine } from '../ruleEngine/RuleEngine';
import { JavaScanner } from '../scanners/JavaScanner';
import { GoScanner } from '../scanners/GoScanner';
import { TypeScriptScanner } from '../scanners/TypeScriptScanner';
import { PythonScanner } from '../scanners/PythonScanner';
import { JavaScriptScanner } from '../scanners/JavaScriptScanner';
import { CSharpScanner } from '../scanners/CSharpScanner';
import { PHPScanner } from '../scanners/PHPScanner';
import { RubyScanner } from '../scanners/RubyScanner';
import { SwiftScanner } from '../scanners/SwiftScanner';
import { KotlinScanner } from '../scanners/KotlinScanner';
import { RustScanner } from '../scanners/RustScanner';
import { ScalaScanner } from '../scanners/ScalaScanner';

const app = express();
const port = process.env.PORT || 3000;

// Configure multer for file uploads
const upload = multer({
    dest: 'uploads/',
    limits: {
        fileSize: 10 * 1024 * 1024, // 10MB limit
        files: 50 // Max 50 files
    }
});

// Serve static files
app.use(express.static(path.join(__dirname, 'public')));

// Serve the main HTML file
app.get('/', (req: express.Request, res: express.Response) => {
    res.sendFile(path.join(__dirname, 'index.html'));
});

// Handle file upload and scanning
app.post('/scan', upload.array('files'), async (req: express.Request, res: express.Response) => {
    try {
        const files = req.files as Express.Multer.File[];
        const aiEnabled = req.body.aiEnabled === 'true';
        // Get Gemini/Vertex settings from request body or env
        const geminiApiKey = req.body.geminiApiKey || process.env.GEMINI_API_KEY;
        const vertexProjectId = req.body.vertexProjectId || process.env.GOOGLE_CLOUD_PROJECT;
        const vertexLocation = req.body.vertexLocation || process.env.GOOGLE_CLOUD_LOCATION || 'us-central1';

        if (!files || files.length === 0) {
            return res.status(400).json({ error: 'No files uploaded' });
        }

        console.log(`Processing ${files.length} files...`);

        // Create a temporary directory for processing
        const tempDir = path.join(__dirname, '../temp');
        if (!fs.existsSync(tempDir)) {
            fs.mkdirSync(tempDir, { recursive: true });
        }

        // Move uploaded files to temp directory
        const filePaths: string[] = [];
        for (const file of files) {
            const newPath = path.join(tempDir, file.originalname);
            fs.renameSync(file.path, newPath);
            filePaths.push(newPath);
        }

        // Initialize scanners and engine
        const scanners = [
            new JavaScanner(),
            new GoScanner(),
            new TypeScriptScanner(),
            new PythonScanner(),
            new JavaScriptScanner(),
            new CSharpScanner(),
            new PHPScanner(),
            new RubyScanner(),
            new SwiftScanner(),
            new KotlinScanner(),
            new RustScanner(),
            new ScalaScanner()
        ];

        const engine = new RuleEngine(scanners);
        
        // AI mode selection logic
        if (geminiApiKey) {
            engine.setGeminiEnabled(true);
            engine.setGeminiApiKey(geminiApiKey);
        } else if (vertexProjectId) {
            engine.setGeminiEnabled(true);
            engine.setVertexAIConfig({
                project: vertexProjectId,
                location: vertexLocation
            });
        } else {
            engine.setGeminiEnabled(false); // Only hardcoded rules
        }

        // Run the scan on the temp directory
        const violations = await engine.run(tempDir);

        // Clean up temporary files
        for (const filePath of filePaths) {
            try {
                fs.unlinkSync(filePath);
            } catch (error) {
                console.error(`Error deleting ${filePath}:`, error);
            }
        }

        // Parse violations into structured format
        const structuredViolations = violations.map(violation => {
            function cleanSeverity(severityRaw: string | undefined): string {
                let s = (severityRaw || "MEDIUM").replace(/[\)"\s]+$/g, "").trim().toUpperCase();
                if (!["HIGH", "MEDIUM", "LOW"].includes(s)) s = "MEDIUM";
                return s;
            }
            function cleanFix(fixRaw: string | undefined, type?: string, description?: string): string {
                let f = (fixRaw || "").trim();
                if (!f || f.toUpperCase() === "N/A") {
                    if (type && type.toLowerCase().includes("email")) {
                        return "Remove hardcoded email addresses and use configuration or environment variables.";
                    }
                    if (type && type.toLowerCase().includes("phone")) {
                        return "Remove hardcoded phone numbers and use configuration or environment variables.";
                    }
                    if ((type && type.toLowerCase().includes("api key")) || (description && description.toLowerCase().includes("api key"))) {
                        return "Move API keys to a secure configuration and rotate them immediately.";
                    }
                    if (type && type.toLowerCase().includes("consent")) {
                        return "Implement consent validation before processing user data.";
                    }
                    if (type && type.toLowerCase().includes("localstorage")) {
                        return "Encrypt the data before storing it in localStorage, or use a more secure storage mechanism.";
                    }
                    if (type && type.toLowerCase().includes("ssn")) {
                        return "Remove SSN collection or justify its necessity and obtain explicit consent.";
                    }
                    if (type && type.toLowerCase().includes("retention")) {
                        return "Implement an expiration mechanism for data stored in localStorage.";
                    }
                    // Add more generic suggestions as needed
                    return "Review and fix the privacy issue according to best practices.";
                }
                return f;
            }

            // First, try to parse AI response format (Gemini/Claude)
            const aiMatch = violation.match(/^([^:]+):\s*([^\n]+(?:\n(?!\n)[^\n]+)*)(?:\n\nSuggested Fix:\s*([^\n]+(?:\n(?!\n)[^\n]+)*))?(?:\n\nSeverity:\s*([^\n]+))?/s);
            if (aiMatch) {
                const type = aiMatch[1].trim();
                const description = aiMatch[2].trim();
                const fix = cleanFix(aiMatch[3], type, description);
                const severity = cleanSeverity(aiMatch[4]);
                // Extract file and line from the violation object
                const fileMatch = violation.match(/([\/\w\.-]+\.(?:js|ts|py|java|go|cs|php|rb|swift|kt|rs|scala)):(\d+)/);
                const file = fileMatch ? fileMatch[1] : "Unknown";
                const line = fileMatch ? parseInt(fileMatch[2]) : 0;
                return {
                    language: "AI Detected",
                    file: file,
                    line: line,
                    type: type,
                    finding: description,
                    description: description,
                    fix: fix,
                    severity: severity
                };
            }
            // Try to parse hardcoded rule output with Description, Fix, Severity
            const hardcodedMatch = violation.match(/^(\d+)\s*[–-]\s*([^:]+):?\s*(.*?)(?:\(found:\s*"([^"]+)"\))?\nDescription:\s*([\s\S]*?)\nFix:\s*([\s\S]*?)\nSeverity:\s*(HIGH|MEDIUM|LOW)/);
            if (hardcodedMatch) {
                return {
                    file: "Unknown",
                    line: parseInt(hardcodedMatch[1]),
                    type: hardcodedMatch[2].trim(),
                    finding: hardcodedMatch[4] || hardcodedMatch[3] || "N/A",
                    description: hardcodedMatch[5] || "N/A",
                    fix: cleanFix(hardcodedMatch[6], hardcodedMatch[2], hardcodedMatch[5]),
                    severity: cleanSeverity(hardcodedMatch[7])
                };
            }
            // Try alternative AI response format with different spacing
            const altAiMatch = violation.match(/^([^:]+):\s*([^\n]+(?:\n(?!\n)[^\n]+)*)(?:\n+Suggested Fix:\s*([^\n]+(?:\n(?!\n)[^\n]+)*))?(?:\n+Severity:\s*([^\n]+))?/s);
            if (altAiMatch) {
                const type = altAiMatch[1].trim();
                const description = altAiMatch[2].trim();
                const fix = cleanFix(altAiMatch[3], type, description);
                const severity = cleanSeverity(altAiMatch[4]);
                // Extract file and line from the violation object
                const fileMatch = violation.match(/([\/\w\.-]+\.(?:js|ts|py|java|go|cs|php|rb|swift|kt|rs|scala)):(\d+)/);
                const file = fileMatch ? fileMatch[1] : "Unknown";
                const line = fileMatch ? parseInt(fileMatch[2]) : 0;
                return {
                    language: "AI Detected",
                    file: file,
                    line: line,
                    type: type,
                    finding: description,
                    description: description,
                    fix: fix,
                    severity: severity
                };
            }
            
            // Try to match the full format, including rule name/description and found value
            let match = violation.match(/^[\[]([^\]]+)\]\s+(.+?):(\d+)\s+-\s+([^-]+?)(?:\s+-\s+)?(?:.*?\(found:\s*"([^"]+)"([\s\S]*?)?\))?/s);
            if (match) {
                // Extract the found value, description, and fix (multi-line)
                let finding = match[5] ? match[5].trim() : "N/A";
                let extra = match[6] ? match[6].trim() : "";
                let description = "N/A";
                let fix = "N/A";
                // Extract Description and Fix from the extra text (multi-line)
                const descMatch = extra.match(/Description:\s*([\s\S]*?)(?:\n|$)/);
                const fixMatch = extra.match(/Fix:\s*([\s\S]*?)(?:\n|$)/);
                if (descMatch && descMatch[1].trim()) description = descMatch[1].trim();
                if (fixMatch && fixMatch[1].trim()) fix = fixMatch[1].trim();
                return {
                    language: match[1],
                    file: match[2],
                    line: parseInt(match[3]),
                    type: match[4].trim(),
                    finding,
                    description,
                    fix: cleanFix(fix, match[4], description),
                    severity: "MEDIUM" // Default for hardcoded rules
                };
            }
            // Fallback: try to extract file and line from anywhere in the string
            match = violation.match(/([\/\w\.-]+\.js):(\d+)/);
            if (match) {
                return {
                    language: "Unknown",
                    file: match[1],
                    line: parseInt(match[2]),
                    type: "Unknown",
                    finding: "N/A",
                    description: violation,
                    fix: "N/A",
                    severity: "MEDIUM"
                };
            }
            // Fallback: show the whole string
            return {
                language: "Unknown",
                file: "Unknown",
                line: 0,
                type: "Unknown",
                finding: "N/A",
                description: violation,
                fix: "N/A",
                severity: "MEDIUM"
            };
        });

        // Sort violations by severity (HIGH → MEDIUM → LOW)
        structuredViolations.sort((a, b) => {
            const severityOrder: { [key: string]: number } = { 'HIGH': 3, 'MEDIUM': 2, 'LOW': 1 };
            const aOrder = severityOrder[a.severity?.toUpperCase()] || 0;
            const bOrder = severityOrder[b.severity?.toUpperCase()] || 0;
            return bOrder - aOrder; // Higher severity first
        });

        // Return results
        res.json({
            success: true,
            violations: structuredViolations,
            totalFiles: files.length,
            totalViolations: violations.length
        });

    } catch (error) {
        console.error('Scan error:', error);
        res.status(500).json({ 
            error: 'Internal server error',
            message: error instanceof Error ? error.message : 'Unknown error'
        });
    }
});

// Health check endpoint
app.get('/health', (req: express.Request, res: express.Response) => {
    res.json({ 
        status: 'healthy',
        timestamp: new Date().toISOString(),
        version: '1.0.0'
    });
});

app.listen(port, () => {
    console.log(`🔒 Privacy Guardian Agents Web Server running on port ${port}`);
    console.log(`🌐 Open http://localhost:${port} to use the web interface`);
});

export default app;