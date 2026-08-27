"""Day 1: variability and system-prompt experiments (SDK v1.0)."""
from dotenv import load_dotenv
import anthropic

load_dotenv()
client = anthropic.Anthropic()

QUESTION = "Name a likely cause of a sudden 3x residential electric bill. One sentence."

def ask(system: str) -> str:
    resp = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=200,
        system=system,
        messages=[{"role": "user", "content": QUESTION}],
    )
    return resp.content[0].text.strip()

print("=== Experiment 1: run-to-run variability (same input, 4 runs) ===")
for i in range(1, 5):
    print(f"[run {i}] {ask('You are a utility billing expert.')}\n")

print("=== Experiment 2: constraining variability with prompting ===")
constrained = (
    "You are a utility billing expert. Respond in exactly this format and "
    "nothing else: 'Cause: <one specific cause, under 12 words>'"
)
for i in range(1, 4):
    print(f"[run {i}] {ask(constrained)}\n")

print("=== Experiment 3: system prompt personas ===")
personas = [
    "You are a utility billing expert.",
    "You are a friendly customer service rep explaining to a worried member.",
    "You are a regulatory compliance officer.",
]
for p in personas:
    print(f"[{p}]\n{ask(p)}\n")