/**
 * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
* Licensed under the MIT License with the Commons Clause.
* This file is provided for personal, educational, and non-commercial use only.
* 
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
 * 
 * JavaScriptScanner - JavaScript File Discovery and Processing
 * 
 * The JavaScriptScanner is responsible for discovering and processing JavaScript (.js) files
 * in codebases for privacy violation analysis. It implements the Scanner interface to provide
 * language-specific file scanning capabilities for JavaScript code.
 * 
 * Key Features:
 * - Recursive directory scanning for .js files
 * - Automatic path filtering for irrelevant directories
 * - UTF-8 content extraction for analysis
 * - Cross-platform path handling
 * - Memory-efficient file processing
 * 
 * File Discovery:
 * - Scans directories recursively for JavaScript files
 * - Filters out common irrelevant paths (node_modules, .git, etc.)
 * - Handles nested directory structures efficiently
 * - Supports large codebases with async processing
 * 
 * Content Processing:
 * - Reads file content as UTF-8 text
 * - Provides standardized ScannedFile interface
 * - Enables privacy rule analysis on JavaScript code
 * - Supports both client-side and server-side JavaScript
 * 
 * Privacy Analysis Support:
 * - Detects hardcoded PII in JavaScript code
 * - Identifies privacy policy violations
 * - Validates consent mechanisms
 * - Checks encryption and security practices
 * - Analyzes data flow and handling patterns
 * 
 * Integration:
 * - Used by RuleEngine for JavaScript privacy scanning
 * - Works with all privacy rule types
 * - Supports AI-enhanced analysis via Gemini
 * - Enables comprehensive JavaScript codebase analysis
 * 
 * Performance:
 * - Async file system operations
 * - Efficient path filtering
 * - Memory-conscious file handling
 * - Scalable for large JavaScript projects
 * 
 * @author Privacy Guardian Agents
 * @version 1.0.0
 */

import {Scanner, ScannedFile, IGNORED_PATHS} from "./Scanner";
import * as fs from 'fs/promises';
import * as path from 'path';

export class JavaScriptScanner implements Scanner {
    language = "JavaScript";

    async scanFiles(dir: string): Promise<ScannedFile[]> {
        return this.getFilesWithExtension(dir, ".js");
    }

    private async getFilesWithExtension(dir: string, ext: string): Promise<ScannedFile[]> {
        let files: ScannedFile[] = [];
        const entries = await fs.readdir(dir, { withFileTypes: true });

        for (const entry of entries) {
            const fullPath = path.join(dir, entry.name);

            // Skip ignored paths
            if (IGNORED_PATHS.some(ignored => fullPath.includes(ignored))) {
                continue;
            }

            if (entry.isDirectory()) {
                files = files.concat(await this.getFilesWithExtension(fullPath, ext));
            } else if (entry.name.endsWith(ext)) {
                const content = await fs.readFile(fullPath, "utf-8");
                files.push({ path: fullPath, content });
            }
        }

        return files;
    }
} 