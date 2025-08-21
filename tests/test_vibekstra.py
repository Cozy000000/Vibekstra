import sys
import os
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')
sys.path.insert(0, src_path)
from vibekstra import vibekstra
from dotenv import load_dotenv


# Load environment variables from the .env file (e.g., OPENAI_API_KEY)
load_dotenv()


def test_vibekstra_example():
    """
    Test the provided input-output example for the single-source shortest path problem.
    """
    # Input
    n = 4  # Number of vertices in the graph
    m = 6  # Number of edges in the graph
    s = 1  # Source vertex is 1

    edges = [
        [1, 2, 2],  # Edge from vertex 1 to vertex 2 with weight 2
        [2, 3, 2],  # Edge from vertex 2 to vertex 3 with weight 2
        [2, 4, 1],  # Edge from vertex 2 to vertex 4 with weight 1
        [1, 3, 5],  # Edge from vertex 1 to vertex 3 with weight 5
        [3, 4, 3],  # Edge from vertex 3 to vertex 4 with weight 3
        [1, 4, 4],  # Edge from vertex 1 to vertex 4 with weight 4
    ]

    # Expected output
    # Distance from source (s) to vertex 1 is 0
    # Distance from source (s) to vertex 2 is 2 (1 -> 2)
    # Distance from source (s) to vertex 3 is 4 (1 -> 2 -> 3)
    # Distance from source (s) to vertex 4 is 3 (1 -> 2 -> 4)
    expected_distances = [0, 2, 4, 3]

    # Call the AI function to calculate the shortest distances
    actual_distances = vibekstra(n, s, edges)

    # Assert that the actual result matches the expected result
    assert actual_distances == expected_distances