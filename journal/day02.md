1. The docs describe two modes: JSON outputs and strict tool use. What does each constrain, and which one fits tonight's triage task? Which one will matter in Week 3? 

The distinction is where the schema gets enforced — same constrained-decoding engine, two different targets:
JSON outputs (output_config.format) constrains the model's reply to you — the response text itself is grammar-locked to your schema. Use it when your code consumes the model's answer as data.
Strict tool use constrains the arguments the model generates when calling a tool — the inputs to get_meter_history(account_id=...) are guaranteed to match that tool's schema. Use it when the model is invoking functions and a malformed argument would break the integration.

2. What does constrained decoding guarantee about a response — and name three things it explicitly does not guarantee.

Constrained decoding guarantees the shape — parseable, typed, enum-bound — and nothing about the judgment: not the right category, not true statements, not grounded reasoning. Shape comes free; correctness is earned."

3. Why does the API impose complexity limits on schemas? (One sentence on the mechanism.)
"Schemas compile into grammars before generation — that compile step is the expensive part, so complex schemas inflate first-request TTFT and grammar size, and the API caps them (oversized = 400 error). Once compiled: cached 24 hours, masking nearly free. The extra token cost is real but incidental."

4. Product-design question: for the triage task, what information belongs in the schema, and what belongs in the prompt? Try a rule of thumb.

Data in the user message, shape in the schema, judgment in the system prompt. Contract / spec / acceptance tests. If it defines what's allowed → schema; if it defines what's right → prompt.



