// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

export interface PrivacyConfig {
    claudeSonnet: {
        enabled: boolean;
        apiKey?: string;
        model: string;
        maxTokens: number;
        temperature: number;
    };
    hardcodedRules: {
        enabled: boolean;
    };
    scanning: {
        chunkSize: number;
        maxFileSize: number;
    };
}

export const defaultConfig: PrivacyConfig = {
    claudeSonnet: {
        enabled: false,
        apiKey: process.env.CLAUDE_API_KEY,
        model: "claude-3-sonnet-20240229",
        maxTokens: 4000,
        temperature: 0.1
    },
    hardcodedRules: {
        enabled: true
    },
    scanning: {
        chunkSize: 50,
        maxFileSize: 1024 * 1024 // 1MB
    }
};

export class ConfigManager {
    private config: PrivacyConfig;

    constructor(config: Partial<PrivacyConfig> = {}) {
        this.config = { ...defaultConfig, ...config };
    }

    getClaudeConfig() {
        return this.config.claudeSonnet;
    }

    getHardcodedConfig() {
        return this.config.hardcodedRules;
    }

    getScanningConfig() {
        return this.config.scanning;
    }

    setClaudeEnabled(enabled: boolean) {
        this.config.claudeSonnet.enabled = enabled;
    }

    setClaudeApiKey(apiKey: string) {
        this.config.claudeSonnet.apiKey = apiKey;
    }

    isClaudeAvailable(): boolean {
        return this.config.claudeSonnet.enabled && !!this.config.claudeSonnet.apiKey;
    }

    isHardcodedEnabled(): boolean {
        return this.config.hardcodedRules.enabled;
    }

    // Load config from environment variables
    loadFromEnv(): void {
        if (process.env.CLAUDE_ENABLED === 'true') {
            this.config.claudeSonnet.enabled = true;
        }
        
        if (process.env.CLAUDE_API_KEY) {
            this.config.claudeSonnet.apiKey = process.env.CLAUDE_API_KEY;
        }

        if (process.env.CLAUDE_MODEL) {
            this.config.claudeSonnet.model = process.env.CLAUDE_MODEL;
        }

        if (process.env.CLAUDE_MAX_TOKENS) {
            this.config.claudeSonnet.maxTokens = parseInt(process.env.CLAUDE_MAX_TOKENS);
        }

        if (process.env.CLAUDE_TEMPERATURE) {
            this.config.claudeSonnet.temperature = parseFloat(process.env.CLAUDE_TEMPERATURE);
        }

        if (process.env.HARDCODED_RULES_ENABLED === 'false') {
            this.config.hardcodedRules.enabled = false;
        }
    }
} 