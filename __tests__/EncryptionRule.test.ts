// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

import { EncryptionRule } from '../src/ruleEngine/rules/EncryptionRule';

describe('EncryptionRule', () => {
  const rule = new EncryptionRule();

  it('flags missing encryption-at-rest', () => {
    const code = `CREATE TABLE users (ssn VARCHAR(11));`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Missing Encryption-at-Rest'))).toBe(true);
  });

  it('flags insecure HTTP', () => {
    const code = `fetch('http://example.com')`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Insecure HTTP Protocol'))).toBe(true);
  });

  it('flags raw PII as primary key', () => {
    const code = `email = "a@b.com" AS PRIMARY KEY;`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Raw PII as Primary Key'))).toBe(true);
  });

  it('does not flag when @encrypt is present', () => {
    const code = `@encrypt\nCREATE TABLE users (ssn VARCHAR(11));`;
    const violations = rule.evaluate(code);
    expect(violations.length).toBe(0);
  });
}); 