// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

import { AdvancedPrivacyRule } from '../src/ruleEngine/rules/AdvancedPrivacyRule';

describe('AdvancedPrivacyRule', () => {
  const rule = new AdvancedPrivacyRule();

  it('flags missing field-level access scoping', () => {
    const code = `GraphQL field: email`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Missing Field-Level Access Scoping'))).toBe(true);
  });

  it('flags ad/tracking code', () => {
    const code = `ad = "pixel.js"`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Ad/Tracking Code'))).toBe(true);
  });

  it('flags region-lock violation', () => {
    const code = `aws_region = "us-east-1"`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Potential Region-Lock Violation'))).toBe(true);
  });

  it('does not flag when @scope is present', () => {
    const code = `@scope: "private"`;
    const violations = rule.evaluate(code);
    expect(violations.length).toBe(0);
  });
}); 