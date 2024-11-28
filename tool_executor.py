from typing import List
from refl_chains import parser
from collections import defaultdict
import json

from langchain_core.messages import BaseMessage, ToolMessage, HumanMessage, AIMessage

from schemas import AnswerQuestion, ReviseAnswer, Reflection
from langchain_core.output_parsers.openai_tools import(
    JsonOutputToolsParser,
    PydanticToolsParser
)

from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import ToolInvocation, ToolExecutor


search = TavilySearchAPIWrapper()
tavily_tool = TavilySearchResults(api_wrapper=search, max_results=5)
tool_executor = ToolExecutor([tavily_tool])


def execute_tools(state:List[BaseMessage]) -> List[ToolMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)
    

    ids = []
    tool_invocations = []

    for parsed_call in parsed_tool_calls:
        for query in parsed_call["args"]["search_queries"]:
            print(f"searching query : {query}")
            tool_invocations.append(ToolInvocation(
                tool="tavily_search_results_json",
                tool_input=query,
            )            )
            ids.append(parsed_call["id"])
    
    outputs=tool_executor.batch(tool_invocations)

    outputs_map= defaultdict(dict)
    for id_, output, invocation in zip(ids,outputs,tool_invocations):
        outputs_map[id_][invocation.tool_input]=output

    tool_messages = []
    for id_,mapped_output in outputs_map.items():
        print(f"mapped output -> {mapped_output}")
        tool_messages.append(ToolMessage(content=json.dumps(mapped_output), tool_call_id = id_))
    
    
    return tool_messages


if __name__ == "__main__":
    print("Hello")

    human_message=HumanMessage(
        content="Write about save the cat all types of stories"
        "Give 2-3 movie examples for each story type"
    )

    answer=AnswerQuestion(
        answer="",
        reflection=Reflection(missing="", superfluous=""),
        search_queries=[
            'Save the Cat story types',
            'examples of Save the Cat movies',
            'Blake Snyder Save the Cat analysis'
        ],
        id="call_hjasgdfgsdjfK629",
    )

    raw_res=execute_tools(
        state=[
            human_message,
            AIMessage(
                content="",
                tool_calls=[
                    {
                        "name":AnswerQuestion.__name__,
                        "args":answer.dict(),
                        "id":"call_hjasgdfgsdjfK629",
                    }
                ]
            )
        ]
    )

    print(raw_res)