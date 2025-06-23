

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
 * JavaScanner - Java File Discovery and Processing
 * 
 * The JavaScanner is responsible for discovering and processing Java (.java) files
 * in codebases for privacy violation analysis. It implements the Scanner interface to provide
 * language-specific file scanning capabilities for Java code.
 * 
 * Key Features:
 * - Recursive directory scanning for .java files
 * - Automatic path filtering for irrelevant directories
 * - UTF-8 content extraction for analysis
 * - Cross-platform path handling
 * - Memory-efficient file processing
 * 
 * File Discovery:
 * - Scans directories recursively for Java source files
 * - Filters out common irrelevant paths (node_modules, .git, etc.)
 * - Handles nested directory structures efficiently
 * - Supports large codebases with async processing
 * 
 * Content Processing:
 * - Reads file content as UTF-8 text
 * - Provides standardized ScannedFile interface
 * - Enables privacy rule analysis on Java code
 * - Supports both application and library Java code
 * 
 * Privacy Analysis Support:
 * - Detects hardcoded PII in Java code
 * - Identifies privacy policy violations
 * - Validates consent mechanisms
 * - Checks encryption and security practices
 * - Analyzes data flow and handling patterns
 * - Examines Java annotations for privacy compliance
 * 
 * Integration:
 * - Used by RuleEngine for Java privacy scanning
 * - Works with all privacy rule types
 * - Supports AI-enhanced analysis via Gemini
 * - Enables comprehensive Java codebase analysis
 * 
 * Performance:
 * - Async file system operations
 * - Efficient path filtering
 * - Memory-conscious file handling
 * - Scalable for large Java projects
 * 
 * @author Privacy Guardian Agents
 * @version 1.0.0
 */

import {Scanner, ScannedFile, IGNORED_PATHS} from "./Scanner";
import * as fs from 'fs/promises';
import * as path from 'path';

export class JavaScanner implements Scanner {
    language = "Java";

    async scanFiles(dir: string): Promise<ScannedFile[]> {
        return this.getFilesWithExtension(dir, ".java");
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

