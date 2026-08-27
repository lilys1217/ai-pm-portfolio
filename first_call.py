"""Day 1: my first Claude API call."""
from dotenv import load_dotenv
import anthropic

load_dotenv()                      # reads .env into environment variables
client = anthropic.Anthropic()     # picks up ANTHROPIC_API_KEY automatically

response = client.messages.create(
    model="claude-sonnet-4-6",
    max_tokens=500,
    system="You are a billing operations assistant at an electric cooperative.",
    messages=[
        {
            "role": "user",
            "content": (
                "A member's bill this month is 3x their usual amount. "
                "List the top 5 causes a billing analyst should check first, "
                "ordered by likelihood, one line each."
            ),
        }
    ],
)

print(response.content[0].text)
print("\n--- usage ---")
print(f"input tokens: {response.usage.input_tokens}, "
      f"output tokens: {response.usage.output_tokens}")