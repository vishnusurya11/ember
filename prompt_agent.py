from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from prompt_chains import( image_generate_chain,
 image_prompt_reflect_chain,
 youtube_thumbnail_generate_chain,
 youtube_thumbnail_prompt_reflect_chain,
)
# Constants
MAX_ITERATIONS= 3
IMAGE_PROMPT_REFLECT = "image_prompt_reflect"
IMAGE_PROMPT_GENERATE = "image_prompt_generate"

YOUTUBE_THUMBNAIL_PROMPT_REFLECT = "youtube_thumbnail_prompt_reflect"
YOUTUBE_THUMBNAIL_GENERATE = "YOUTUBE_THUMBNAIL_GENERATE"


# Helper functions
def image_generation_node(state: Sequence[BaseMessage]):
    return image_generate_chain.invoke({"messages": state})

def image_reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = image_prompt_reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

def youtube_thumbnail_generation_node(state: Sequence[BaseMessage]):
    return youtube_thumbnail_generate_chain.invoke({"messages": state})

def youtube_thumbnail_reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = youtube_thumbnail_prompt_reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]

# Function to process input content and return the final response
def image_prompt_generating_agent(input_content: str) -> str:
    # Initialize the graph builder
    builder = MessageGraph()
    builder.add_node(IMAGE_PROMPT_GENERATE, image_generation_node)
    builder.add_node(IMAGE_PROMPT_REFLECT, image_reflection_node)
    builder.set_entry_point(IMAGE_PROMPT_GENERATE)

    # Conditional edge function
    def should_continue(state: List[BaseMessage]):
        if len(state) > MAX_ITERATIONS:
            return END
        return IMAGE_PROMPT_REFLECT

    builder.add_conditional_edges(IMAGE_PROMPT_GENERATE, should_continue)
    builder.add_edge(IMAGE_PROMPT_REFLECT, IMAGE_PROMPT_GENERATE)
    graph = builder.compile()

    # Create input message
    inputs = HumanMessage(content=input_content)

    # Invoke the graph with the input message
    response = graph.invoke(inputs)

    # Return the final response content
    return response[-1].content

def youtube_thumbnail_prompt_generating_agent(input_content: str) -> str:
    # Initialize the graph builder
    builder = MessageGraph()
    builder.add_node(YOUTUBE_THUMBNAIL_GENERATE, youtube_thumbnail_generation_node)
    builder.add_node(YOUTUBE_THUMBNAIL_PROMPT_REFLECT, youtube_thumbnail_reflection_node)
    builder.set_entry_point(YOUTUBE_THUMBNAIL_GENERATE)

    # Conditional edge function
    def should_continue(state: List[BaseMessage]):
        if len(state) > MAX_ITERATIONS:
            return END
        return YOUTUBE_THUMBNAIL_PROMPT_REFLECT

    builder.add_conditional_edges(YOUTUBE_THUMBNAIL_GENERATE, should_continue)
    builder.add_edge(YOUTUBE_THUMBNAIL_PROMPT_REFLECT, YOUTUBE_THUMBNAIL_GENERATE)
    graph = builder.compile()

    # Create input message
    inputs = HumanMessage(content=input_content)

    # Invoke the graph with the input message
    response = graph.invoke(inputs)

    # Return the final response content
    return response[-1].content

# Example usage
if __name__ == "__main__":
    input_text = """Make this tweet better:
    @langchainAI
    - newly Tool calling feature is seriously underrated.
    After a long wait, it's here making the implementation of agent across different models with function calling super easy.
    Made a video covering their newest blog post."""
    
    result = image_prompt_generating_agent(input_text)
    print(result)
