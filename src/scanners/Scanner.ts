/**
 * Scanner.ts
 * 
 * Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
 * Licensed under the MIT License modified with the Commons Clause.
 * This file is provided for personal, educational, and non-commercial use only.
 * Commercial use including selling, sublicensing, internal deployment in for-profit
 * organizations, and commercial distribution is prohibited without explicit permission.
 * For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
 * 
 * The Scanner interface defines the contract for language-specific file scanners in Privacy Guardian Agents.
 * Each scanner is responsible for detecting privacy violations in a specific programming language
 * by analyzing source code files and applying relevant privacy rules.
 * 
 * Key Responsibilities:
 * - File type detection and validation
 * - Source code parsing and tokenization
 * - Privacy rule application
 * - Violation detection and reporting
 * - Context preservation for accurate reporting
 * 
 * Implementation Guidelines:
 * - Support multiple file extensions for the target language
 * - Implement efficient regex patterns for rule matching
 * - Provide detailed location information (file, line, column)
 * - Handle edge cases and parsing errors gracefully
 * - Maintain consistent violation format across scanners
 * 
 * Performance Considerations:
 * - Use streaming file reading for large files
 * - Implement caching for frequently accessed patterns
 * - Optimize regex patterns for speed and accuracy
 * - Provide configurable scan depth and exclusions
 * 
 * Error Handling:
 * - Graceful handling of unsupported file formats
 * - Detailed error reporting for debugging
 * - Fallback mechanisms for parsing failures
 * - Validation of input parameters and file content
 * 
 * @author Privacy Guardian Agents
 * @version 1.0.0
 * @since 2025-01-01
 */

export interface ScannedFile {
    path: string;
    content: string;
}

export interface Scanner {
    language: string;
    scanFiles(dir: string): Promise<ScannedFile[]>;
}

export const IGNORED_PATHS = ['tools/privacy-vulnerability-checker', 'node_modules', '.git'];