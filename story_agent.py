from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from story_chains import( 
    story_generate_chain,
 story_prompt_reflect_chain,
 story_beat_generate_chain,
 story_beat_reflect_chain,

)
# Constants
MAX_ITERATIONS= 6
STORY_PROMPT_REFLECT = "story_prompt_reflect"
STORY_PROMPT_GENERATE = "story_prompt_generate"

STORY_BEAT_REFLECT = "story_beat_reflect"
STORY_BEAT_GENERATE = "story_beat_generate"


# Helper functions
def story_generation_node(state: Sequence[BaseMessage]):
    return story_generate_chain.invoke({"messages": state})

def story_reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = story_prompt_reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]



def story_beat_generation_node(state: Sequence[BaseMessage]):
    return story_beat_generate_chain.invoke({"messages": state})

def story_beat_reflection_node(messages: Sequence[BaseMessage]) -> List[BaseMessage]:
    res = story_beat_reflect_chain.invoke({"messages": messages})
    return [HumanMessage(content=res.content)]




# Function to process input content and return the final response
def story_prompt_generating_agent(input_content: str) -> str:
    # Initialize the graph builder
    builder = MessageGraph()
    builder.add_node(STORY_PROMPT_GENERATE, story_generation_node)
    builder.add_node(STORY_PROMPT_REFLECT, story_reflection_node)
    builder.set_entry_point(STORY_PROMPT_GENERATE)

    # Conditional edge function
    def should_continue(state: List[BaseMessage]):
        if len(state) > MAX_ITERATIONS:
            return END
        return STORY_PROMPT_REFLECT

    builder.add_conditional_edges(STORY_PROMPT_GENERATE, should_continue)
    builder.add_edge(STORY_PROMPT_REFLECT, STORY_PROMPT_GENERATE)
    graph = builder.compile()

    # Create input message
    inputs = HumanMessage(content=input_content)

    # Invoke the graph with the input message
    response = graph.invoke(inputs)

    print("#########################################")
    print(response)
    print("#########################################")

    # Return the final response content
    return response[-1].content


def story_beat_generating_agent(input_content: str) -> str:
    # Initialize the graph builder
    builder = MessageGraph()
    builder.add_node(STORY_BEAT_GENERATE, story_beat_generation_node)
    builder.add_node(STORY_BEAT_REFLECT, story_beat_reflection_node)
    builder.set_entry_point(STORY_BEAT_GENERATE)

    # Conditional edge function
    def should_continue(state: List[BaseMessage]):
        if len(state) > MAX_ITERATIONS:
            return END
        return STORY_BEAT_REFLECT

    builder.add_conditional_edges(STORY_BEAT_GENERATE, should_continue)
    builder.add_edge(STORY_BEAT_REFLECT, STORY_BEAT_GENERATE)
    graph = builder.compile()

    # Create input message
    inputs = HumanMessage(content=input_content)

    # Invoke the graph with the input message
    response = graph.invoke(inputs)

    print("#########################################")
    print(f"story beats: {response}")
    print("#########################################")

    # Return the final response content
    return response[-1].content


# Example usage
if __name__ == "__main__":

    input_dict = {
        "topic": "A man who won the lottery must break a deadly curse attached to the money before it claims his life in 48 hours."
    }

    input_text = f""" Using the topic provided generate beats
    TOPIC : {input_dict['topic']}
 
                """
    generated_beats = story_beat_generating_agent(input_text)

    print(f"generated beats ---> {generated_beats}")

    input_text = f""" Using the topic and beats provided generate a story 
    PLOT : {input_dict['topic']}

    BEATS : {generated_beats}
 
                """
    print("####################################################")
    generated_story = story_prompt_generating_agent(input_text)
    print(f"generated_story ---> {generated_story}")
