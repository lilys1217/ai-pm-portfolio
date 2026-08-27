A trained LLM is two files: a huge parameter file   billions of learned numbers where all the capability lives and a small run file in any language that executes them. The code is trivial; the parameters are the model.

Training writes the weights weeks, millions of dollars, done rarely. Inference reads them seconds, fractions of a cent, done billions of times a day."

The model's atomic unit of text, be of a word. You pay per token (output costs more than input), you wait per output token, and you fit per token.

A database with no match returns zero rows; an LLM has no zero-rows mode  it always produces fluent, confident text, true or not, because it's predicting plausible tokens, not retrieving facts.

Same learning machinery, three datasets: internet scale for knowledge, curated conversations for assistant behavior, human preference rankings for polish.

The model's per-request working memory a fixed token budget. Weights are disk, context is RAM. Outside the window, information simply doesn't exist to the model.
 the same input can give different answers  
 this is why AI products need evals, not just QA

Every token costs money and latency AI features have 
unit economics
in a way normal software features don't.
Models predict plausible text, they don't look up facts 



Experiment 1: how different were the 4 runs — wording only, or genuinely different causes?
run 2 to 4 got the identical output. the output for run 1 is also very vlose to other runs, but a little bit more details. 
=== Experiment 1: run-to-run variability (same input, 4 runs) ===
[run 1] A sudden tripling of a residential electric bill is most likely caused by a malfunctioning or continuously running HVAC system, electric water heater, or other high-draw appliance that is stuck in an "on" state.

[run 2] A likely cause is a malfunctioning electric water heater or HVAC system running continuously due to a failed thermostat or heating element.

[run 3] A likely cause is a malfunctioning electric water heater or HVAC system running continuously due to a failed thermostat or heating element.

[run 4] A likely cause is a malfunctioning electric water heater or HVAC system running continuously due to a failed thermostat or heating element.

Experiment 2: did the format constraint make outputs more consistent? Fully identical? (Typical result: the format converges, the content still varies — prompting narrows variability but doesn't eliminate it.)
got fully identical results. 
[run 1] Cause: A malfunctioning electric water heater running continuously without shutoff.

[run 2] Cause: A malfunctioning electric water heater running continuously without shutoff.

[run 3] Cause: A malfunctioning electric water heater running continuously without shutoff.


Experiment 3: how did the persona change content, tone, and length — with the same question?
One sentence: the randomness dial is gone — consistency now comes from prompting and is proven by evals. Rewrite that in your own words ← it's the seed of your Week 4 eval report.
for the second due to we set the role as  friendly customer service rep , it does give more details. run 1 and run 3 get the same output. 
=== Experiment 3: system prompt personas ===
[You are a utility billing expert.]
A likely cause is a malfunctioning electric water heater or HVAC system running continuously due to a failed thermostat or heating element.

[You are a friendly customer service rep explaining to a worried member.]
A likely cause of a sudden triple electric bill is a malfunctioning HVAC system, electric water heater, or other large appliance running continuously instead of cycling on and off as it should.

[You are a regulatory compliance officer.]
A likely cause is a malfunctioning electric water heater or HVAC system running continuously due to a failed thermostat or heating element.



triage_vo.py
Correctness: Would you have triaged each the same way? Where would a 15-year billing analyst disagree?
Format discipline: Did it follow the format exactly, all 3 times? Any invented categories or extra prose?
Rationale grounding: Does the rationale cite the specific data, or is it generic filler?
Scale question: What breaks if this runs on 300 exceptions/day with no human review? (Write at least 3 things.)