import os
from typing_extensions import Literal
import json
import requests
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

# Function to send a request to the Claude API and get a structured Pydantic model output
def structured_output(
    content: str,
    response_format: T,
    model: str = "claude-3-sonnet-20240229",
) -> T:
    """
    Send a request to the Claude API and get a structured Pydantic model output.

    Args:
        content: The input content to send to the API
        response_format: The expected response format as a Pydantic model
        model: The Claude model to use (default: "claude-3-sonnet-20240229")

    Returns:
        A Pydantic model instance containing the structured response.
    """
    # Retrieve the Claude API key from the environment variables
    api_key = os.environ.get("CLAUDE_API_KEY")
    if not api_key:
        raise ValueError("The CLAUDE_API_KEY environment variable is not set!")
        
    # Get the JSON schema for the response format
    schema = response_format.model_json_schema()
    
    # Create the prompt with schema information
    prompt = f"""
{content}

Please respond with a JSON object that matches this exact schema:
{json.dumps(schema, indent=2)}

Return only the JSON object, no other text.
"""

    # Send the request to the Claude API
    headers = {
        "Content-Type": "application/json",
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01"
    }
    
    data = {
        "model": model,
        "max_tokens": 1000,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = requests.post(
        "https://api.anthropic.com/v1/messages",
        headers=headers,
        json=data
    )
    
    if response.status_code != 200:
        raise ValueError(f"Claude API request failed: {response.status_code} - {response.text}")
    
    response_data = response.json()
    content_text = response_data["content"][0]["text"]
    
    # Parse the JSON response
    try:
        json_response = json.loads(content_text)
        return response_format(**json_response)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON response: {e}\nResponse: {content_text}")
    except Exception as e:
        raise ValueError(f"Failed to create response model: {e}\nResponse: {content_text}")