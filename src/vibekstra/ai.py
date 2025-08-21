import os
from typing_extensions import Literal
import openai
from pydantic import BaseModel, Field
from typing import TypeVar, List

# Define a class to represent a weighted directed edge in a graph
class Edge(BaseModel):
    """Represents a weighted directed edge in a graph."""
    u: int = Field(..., description="The starting vertex of the edge")
    v: int = Field(..., description="The ending vertex of the edge")
    w: int = Field(..., description="The weight of the edge")

# Define a request model for solving the single-source shortest path problem
class VibekstraRequest(BaseModel):
    """Request model for the single-source shortest path problem."""
    prompt: str = Field(
        "You are an algorithm expert. Please solve the following single-source shortest path problem for a graph with non-negative weights (similar to Dijkstra's algorithm)."
        "Calculate the shortest distance from the specified source vertex to every other vertex."
        "The vertices are numbered starting from 1. If a vertex is unreachable, set the distance to -1 (though this problem guarantees all vertices are reachable)."
        "Return a list where the i-1th element represents the shortest distance from the source vertex to vertex i.",
        description="Instruction for the AI"
    )
    n: int = Field(..., description="The number of vertices in the graph")
    source: int = Field(..., description="The source (starting) vertex")
    edges: List[Edge] = Field(..., description="The list of edges in the graph")

# Define a response model for the single-source shortest path problem
class VibekstraResponse(BaseModel):
    """Response model for the single-source shortest path problem."""
    distances: List[int] = Field(..., description="A list of shortest distances from the source vertex to each vertex, in order of vertex numbering")

# Function to calculate single-source shortest paths using AI
def vibekstra(n: int, source: int, edges: List[List[int]]) -> List[int]:
    """
    Calculate single-source shortest paths using AI.

    Args:
        n: The number of vertices in the graph
        source: The source vertex
        edges: A list of edges, e.g., [[u1, v1, w1], [u2, v2, w2], ...]

    Returns:
        A list of shortest distances from the source vertex to each vertex.
    """
    # Convert the input edge list into a list of Pydantic Edge models
    edge_models = [Edge(u=u, v=v, w=w) for u, v, w in edges]

    # Construct the request data
    request_data = VibekstraRequest(
        n=n,
        source=source,
        edges=edge_models
    )

    # Call the AI and get structured output
    response_model = structured_output(
        content=request_data.model_dump_json(indent=2),
        response_format=VibekstraResponse,
    )
    
    return response_model.distances

# --- General OpenAI API call function (no modification needed) ---

T = TypeVar("T", bound=BaseModel)

# Function to send a request to the OpenAI API and get a structured Pydantic model output
def structured_output(
    content: str,
    response_format: T,
    model: str = "gpt-4.1-mini",
) -> T:
    """
    Send a request to the OpenAI API and get a structured Pydantic model output.

    Args:
        content: The input content to send to the API
        response_format: The expected response format as a Pydantic model
        model: The OpenAI model to use (default: "gpt-4.1-mini")

    Returns:
        A Pydantic model instance containing the structured response.
    """
    # Retrieve the OpenAI API key from the environment variables
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("The OPENAI_API_KEY environment variable is not set!")
        
    # Initialize the OpenAI client with the API key
    client = openai.OpenAI(api_key=api_key)

    # Send the request to the OpenAI API
    response = client.beta.chat.completions.parse(
        model=model,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": content,
                    },
                ],
            }
        ],
        response_format=response_format,
    )
    # Parse the response into the expected Pydantic model
    response_model = response.choices[0].message.parsed
    return response_model