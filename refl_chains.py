# reflexion Agent

from typing import List, Sequence
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph import END, MessageGraph
from chains import generate_chain, reflect_chain
import datetime
from langchain_openai import ChatOpenAI


from langchain_core.output_parsers.openai_tools import(
    JsonOutputToolsParser,
    PydanticToolsParser
)



from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from schemas import AnswerQuestion, ReviseAnswer

llm = ChatOpenAI(model="gpt-4o-mini")

# llm = ChatOpenAI(model="gpt-4o")

parser = JsonOutputToolsParser(return_id=True)
parser_pydantic = PydanticToolsParser(tools=[AnswerQuestion])


actor_prompt_template = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert researcher.
            Current time : {time}
            1. {first_instruction}
            2. Reflect and critque your answer. Be severe to maximize improvement.
            3. Recommend search queries to research information and improve your answer.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
        (
            "system",
            "Answer the user's question above using the required format"
        )
    ]
).partial(
    time=lambda: datetime.datetime.now().isoformat(),
)



first_responder_prompt_template = actor_prompt_template.partial(
    first_instruction="Provide a detailed ~1000 word answer"
)


first_responder = first_responder_prompt_template | llm.bind_tools(
    tools=[AnswerQuestion], tool_choice="AnswerQuestion"
)


revise_instructions = """ Revise your previous answer using the new information.
- you should use the previous critique to add important information to your answer.
    - you must include numerical citations in your revised answer to ensure it can be verified.
    - Add a "References" section to the bottom of your answer (which does not count towards word limit)
        - [1] https://example1.com
        - [2] https://example2.com
    - you should use the previous critique to remove the superfluous information from your answer and make SURE it is not more than 1000 words
"""

revisor = actor_prompt_template.partial(
    first_instruction=revise_instructions
)  | llm.bind_tools(
    tools=[ReviseAnswer], tool_choice="ReviseAnswer"
)


if __name__ == "__main__":

    print("Hello Reflexion")

    # human_message=HumanMessage(
    #     content="Write about AI powered SOC/ Autonomous soc problem domain,"
    #     "list startups that do that and raised capital"
    # )

    human_message=HumanMessage(
        content="Write about save the cat all types of stories"
        "Briefly describe each story type and Give 2-3 movie examples for each story type"
    )


    chain=(
        first_responder_prompt_template
        | llm.bind_tools(tools=[AnswerQuestion], tool_choice="AnswerQuestion")
        | parser_pydantic
    )


    res = chain.invoke(input={"messages":[human_message]})
    print(res)

    print("Done")
