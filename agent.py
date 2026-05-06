from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands_tools import calculator, current_time

# Define a custom tool as a Python function using the @tool decorator
@tool
def letter_counter(word: str, letter: str) -> int:
    """
    Count occurrences of a specific letter in a word.

    Args:
        word (str): The input word to search in
        letter (str): The specific letter to count

    Returns:
        int: The number of occurrences of the letter in the word
    """
    if not isinstance(word, str) or not isinstance(letter, str):
        return 0

    if len(letter) != 1:
        raise ValueError("The 'letter' parameter must be a single character")

    return word.lower().count(letter.lower())

# Create a configured Ollama model
ollama_model = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1:8b",
    temperature=0.7,
    keep_alive="10m",
    stop_sequences=["###", "END"],
    options={"top_k": 40}
)

# Create an agent with the configured model
# Create an agent with tools from the community-driven strands-tools package
# as well as our custom letter_counter tool
agent = Agent(model=ollama_model, tools=[calculator, current_time, letter_counter])

# Ask the agent a question that uses the available tools
message = """
I have 4 requests:

1. What is the time right now?
2. Calculate 3111696 / 74088
3. Tell me how many letter R's are in the word "strawberry" 🍓
"""
agent(message)
