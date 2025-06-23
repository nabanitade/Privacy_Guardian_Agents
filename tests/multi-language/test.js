// JavaScript test file with privacy violations
const userEmail = "test@example.com";
const userSSN = "123-45-6789";
const userPhone = "555-123-4567";

function processUserData(user) {
    console.log("Processing user:", user.email); // PII in console log
    return {
        id: user.id,
        email: user.email,
        ssn: user.ssn // Sensitive data
    };
}

const apiKey = "sk-1234567890abcdef"; // API key
const userData = {
    name: "John Doe",
    email: "john@example.com",
    phone: "555-987-6543",
    address: "123 Main Street, Anytown, CA 90210"
};

const { PiiRule } = require('../../dist/ruleEngine/rules/PiiRule');

describe('Multi-language PII Rule Detection', () => {
  const javaCode = 'public class User { String email = "test@example.com"; }';
  const pythonCode = 'email = "test@example.com" # user email';
  const jsCode = 'const email = "test@example.com";';

  it('detects PII in Java code', () => {
    const rule = new PiiRule();
    const violations = rule.evaluate(javaCode, 'User.java');
    expect(violations.length).toBeGreaterThan(0);
    expect(violations[0].match).toContain('test@example.com');
  });

  it('detects PII in Python code', () => {
    const rule = new PiiRule();
    const violations = rule.evaluate(pythonCode, 'user.py');
    expect(violations.length).toBeGreaterThan(0);
    expect(violations[0].match).toContain('test@example.com');
  });

  it('detects PII in JavaScript code', () => {
    const rule = new PiiRule();
    const violations = rule.evaluate(jsCode, 'user.js');
    expect(violations.length).toBeGreaterThan(0);
    expect(violations[0].match).toContain('test@example.com');
  });
}); 