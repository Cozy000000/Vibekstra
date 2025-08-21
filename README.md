# Vibekstra 🔮

AI-powered single source shortest path using GPT.

The project name is an interesting tribute to the classic "Dijkstra" algorithm, emphasizing its essence based on "Vibe" (intuition) rather than deterministic computation.

## ✨ Features

-   **AI-Driven**: Utilizes OpenAI's latest models to calculate the shortest path.
-   **Type-Safe**: Uses Pydantic for robust input and output validation.
-   **Simple Interface**: Provides a clean and intuitive function to solve the problem.
-   **Purely Experimental**: This is a fun project. **Do NOT use it in any production environment!**

## 🚀 Installation

Once published to PyPI, you can install it using pip:

```bash
pip install vibekstra
💡 Usage
1. Set Your API Key
You need to set your OpenAI API key. It's best to set it as an environment variable.

code
Bash
export OPENAI_API_KEY="sk-..."
2. Call the Function
Here is a complete, runnable example of how to use vibekstra.

code
Python
from vibekstra import vibekstra

# 1. Define your graph
n = 4      # The number of vertices
s = 1      # The source vertex

# The list of edges: [start_vertex, end_vertex, weight]
edges = [
    [1, 2, 2],
    [2, 3, 2],
    [2, 4, 1],
    [1, 3, 5],
    [3, 4, 3],
    [1, 4, 4],
]

# 2. Let the AI calculate the shortest paths!
try:
    # Pass the arguments correctly, separated by commas
    distances = vibekstra(n=n, s=s, edges=edges)
    
    print(f"Shortest distances from source {s}: {distances}")
    # Expected output: Shortest distances from source 1: [0, 2, 4, 3]

except Exception as e:
    print(f"An error occurred: {e}")


🧪 Testing (For Developers)
If you have cloned the repository and want to run tests locally:
Install the project in editable mode with its dependencies.
Run pytest from the root directory.

code
Bash
# From the project root directory
pip install -e .
pytest

📄 License
This project is licensed under the MIT License. See the LICENSE file for details.

⚠️ Disclaimer: This project is highly experimental. Its results depend on an external AI service and may be inconsistent, inaccurate, or slow. Never use this in critical systems where reliability and performance are required.