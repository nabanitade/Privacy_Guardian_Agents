// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License with the Commons Clause.
// 
// This file is provided for personal, educational, and non-commercial use only.
// Commercial use including selling, sublicensing, internal deployment in for-profit
// environments, SaaS integration, or submission to hackathons, accelerators, or competitive evaluations—is strictly prohibited without a commercial license.
// 
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
// Commercial use is prohibited without a license.
// To request a Commercial License or integration approval, contact: nabanita@privacylicense.com | https://privacylicense.ai

import {Scanner, ScannedFile, IGNORED_PATHS} from "./Scanner";
import * as fs from 'fs/promises';
import * as path from 'path';

export class RustScanner implements Scanner {
    language = "Rust";

    async scanFiles(dir: string): Promise<ScannedFile[]> {
        return this.getFilesWithExtension(dir, ".rs");
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