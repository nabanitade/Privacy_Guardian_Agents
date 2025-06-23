// Copyright (c) 2025 Privacy Guardian Agents by Privacy License . All rights reserved.
// Licensed under the MIT License modified with the Commons Clause.
// For complete license terms, see https://gitlab.com/tnabanitade/privacysdk/-/blob/master/LICENSE
// Commercial use is prohibited without a license.
// Contact for Commercial License: nabanita@privacylicense.com | https://privacylicense.ai

import { DataFlowRule } from '../src/ruleEngine/rules/DataFlowRule';

describe('DataFlowRule', () => {
  const rule = new DataFlowRule();

  it('flags sensitive data source', () => {
    const code = `user = "Alice";`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Sensitive Data Source'))).toBe(true);
  });

  it('flags raw PII in logs', () => {
    const code = `logger.log(user);`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Raw PII in Logs'))).toBe(true);
  });

  it('flags missing retention timer', () => {
    const code = `retain user_data for 365`;
    const violations = rule.evaluate(code);
    expect(violations.some(v => v.match.includes('Missing Retention Timer'))).toBe(true);
  });

  it('does not flag when data is masked', () => {
    const code = `mask(user)`;
    const violations = rule.evaluate(code);
    expect(violations.length).toBe(0);
  });
}); 