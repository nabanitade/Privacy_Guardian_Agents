// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE.
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

import { RuleEngine } from "./ruleEngine/RuleEngine";
import { JavaScanner } from "./scanners/JavaScanner";
import { GoScanner } from "./scanners/GoScanner";
import { TypeScriptScanner } from "./scanners/TypeScriptScanner";
import { PythonScanner } from "./scanners/PythonScanner";
import { JavaScriptScanner } from "./scanners/JavaScriptScanner";
import { CSharpScanner } from "./scanners/CSharpScanner";
import { PHPScanner } from "./scanners/PHPScanner";
import { RubyScanner } from "./scanners/RubyScanner";
import { SwiftScanner } from "./scanners/SwiftScanner";
import { KotlinScanner } from "./scanners/KotlinScanner";
import { RustScanner } from "./scanners/RustScanner";
import { ScalaScanner } from "./scanners/ScalaScanner";

const projectPath = process.argv[2] || '.';
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

// Configure Gemini if enabled
const geminiEnabled = process.env.GEMINI_ENABLED === 'true' || process.argv.includes('--gemini');
const geminiApiKey = process.env.GEMINI_API_KEY;
const googleCloudProject = process.env.GOOGLE_CLOUD_PROJECT;
const googleCloudLocation = process.env.GOOGLE_CLOUD_LOCATION;
const useVertexAI = process.env.GOOGLE_GENAI_USE_VERTEXAI === 'true';

if (geminiEnabled) {
    if (useVertexAI && googleCloudProject) {
        // Use Vertex AI with Google Cloud authentication
        engine.setGeminiEnabled(true);
        engine.setVertexAIConfig({
            project: googleCloudProject,
            location: googleCloudLocation || 'us-central1'
        });
        console.log("🤖 Google Gemini AI scanning enabled via Vertex AI");
    } else if (geminiApiKey) {
        // Use Gemini Developer API with API key
        engine.setGeminiApiKey(geminiApiKey);
        engine.setGeminiEnabled(true);
        console.log("🤖 Google Gemini AI scanning enabled via Developer API");
    } else {
        console.warn("⚠️  Gemini enabled but no authentication configured. Falling back to hardcoded rules.");
        console.warn("   For Vertex AI: Set GOOGLE_CLOUD_PROJECT and GOOGLE_GENAI_USE_VERTEXAI=true");
        console.warn("   For Developer API: Set GEMINI_API_KEY");
    }
} else {
    console.log("🔧 Using hardcoded privacy rules");
}

engine.run(projectPath).then((violations) => {
    if (violations.length > 0) {
        console.log("\n" + "=".repeat(80));
        console.log("🔍 Privacy Guardian Agents PRIVACY VULNERABILITIES CHECKER - SCAN RESULTS");
        console.log("=".repeat(80));
        
        // Group violations by language
        const violationsByLanguage: { [key: string]: string[] } = {};
        violations.forEach(v => {
            const match = v.match(/^\[([^\]]+)\]/);
            const language = match ? match[1] : 'Unknown';
            if (!violationsByLanguage[language]) {
                violationsByLanguage[language] = [];
            }
            violationsByLanguage[language].push(v);
        });

        // Display violations by language
        Object.keys(violationsByLanguage).forEach(language => {
            const langViolations = violationsByLanguage[language];
            console.log(`\n📁 ${language.toUpperCase()} FILES (${langViolations.length} violations)`);
            console.log("-".repeat(60));
            
            langViolations.forEach((violation, index) => {
                const cleanViolation = violation.replace(/^\[\w+\]\s+/, '');
                const [fileInfo, ...details] = cleanViolation.split(' - ');
                
                console.log(`\n${index + 1}. ${fileInfo}`);
                console.log(`   ${details.join(' - ')}`);
            });
        });

        console.log("\n" + "=".repeat(80));
        console.log(`📊 SUMMARY: ${violations.length} total violations found`);
        
        if (engine.isGeminiAvailable()) {
            console.log("🤖 Enhanced with Google Gemini AI for comprehensive analysis");
        } else {
            console.log("🔧 Analysis completed using hardcoded privacy rules");
        }
        
        console.log("=".repeat(80) + "\n");
        
        process.exit(1);
    } else {
        console.log("\n" + "=".repeat(80));
        console.log("✅ Privacy Guardian Agents PRIVACY VULNERABILITIES CHECKER - SCAN COMPLETE");
        console.log("=".repeat(80));
        console.log("🎉 No privacy violations found in your codebase!");
        
        if (engine.isGeminiAvailable()) {
            console.log("🤖 Scan completed using Google Gemini AI for comprehensive privacy analysis");
        } else {
            console.log("🔧 Scan completed using hardcoded privacy rules");
        }
        
        console.log("=".repeat(80) + "\n");
    }
});