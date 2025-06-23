// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

import { ConsentRule } from '../src/ruleEngine/rules/ConsentRule';

describe('ConsentRule', () => {
  const rule = new ConsentRule();

  it('flags missing consent marker', () => {
    const code = `const data_capture = "email";`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Missing Consent Marker'))).toBe(true);
  });

  it('does not flag when @consent_required is present', () => {
    const code = `@consent_required\nconst data_capture = "email";`;
    const violations = rule.evaluate(code);
    expect(violations.length).toBe(0);
  });

  it('flags forced consent', () => {
    const code = `forced_consent = true;`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Forced Consent'))).toBe(true);
  });

  it('flags missing purpose limitation', () => {
    const code = `user_data = { name: "Alice" }`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Missing Purpose Limitation'))).toBe(true);
  });

  it('flags missing profiling opt-out', () => {
    const code = `profiling = "enabled";`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Missing Profiling Opt-Out Check'))).toBe(true);
  });
}); 