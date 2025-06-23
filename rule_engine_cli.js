#!/usr/bin/env node

// rule_engine_cli.js
// Node.js CLI wrapper for Privacy Guardian Agents RuleEngine
// Usage: node rule_engine_cli.js <project_path>

const path = require('path');
const fs = require('fs');

// Register ts-node to run TypeScript directly
require('ts-node').register({
  transpileOnly: true,
  project: path.join(__dirname, 'tsconfig.json'),
});

const { RuleEngine } = require('./src/ruleEngine/RuleEngine');
const { JavaScriptScanner } = require('./src/scanners/JavaScriptScanner');
const { TypeScriptScanner } = require('./src/scanners/TypeScriptScanner');
const { JavaScanner } = require('./src/scanners/JavaScanner');
const { PythonScanner } = require('./src/scanners/PythonScanner');
const { GoScanner } = require('./src/scanners/GoScanner');
const { CSharpScanner } = require('./src/scanners/CSharpScanner');
const { PHPScanner } = require('./src/scanners/PHPScanner');
const { RubyScanner } = require('./src/scanners/RubyScanner');
const { SwiftScanner } = require('./src/scanners/SwiftScanner');
const { KotlinScanner } = require('./src/scanners/KotlinScanner');
const { RustScanner } = require('./src/scanners/RustScanner');
const { ScalaScanner } = require('./src/scanners/ScalaScanner');

async function main() {
  const projectPath = process.argv[2] || '.';

  // Instantiate all language scanners
  const scanners = [
    new JavaScriptScanner(),
    new TypeScriptScanner(),
    new JavaScanner(),
    new PythonScanner(),
    new GoScanner(),
    new CSharpScanner(),
    new PHPScanner(),
    new RubyScanner(),
    new SwiftScanner(),
    new KotlinScanner(),
    new RustScanner(),
    new ScalaScanner(),
  ];

  const engine = new RuleEngine(scanners);

  try {
    const violations = await engine.run(projectPath);
    // Output as JSON array of violation strings
    process.stdout.write(JSON.stringify({ violations }));
  } catch (err) {
    process.stderr.write(JSON.stringify({ error: err.message || String(err) }));
    process.exit(1);
  }
}

main(); 