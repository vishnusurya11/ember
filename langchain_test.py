# Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/
# OpenAI Chat Model Documents: https://python.langchain.com/v0.2/docs/integrations/chat/openai/

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage


from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotChatMessagePromptTemplate,
)


# Setup environment variables and messages
load_dotenv()

# Create a ChatOpenAI model
model = ChatOpenAI(model="gpt-4o-mini")




examples = [
    {"input": "India", "output": """India, located in South Asia, is the 7th largest country by land area and the 2nd most populous nation, with over 1.4 billion people. 
    It spans diverse zones, from the Himalayas in the north to tropical coasts in the south. 
    India experiences a range of climates, from scorching summers to monsoon rains and snowy winters in the north. 
    As the world’s largest democracy, India gained independence in 1947 and operates as a federal parliamentary republic. 
    Known for its exports like textiles, IT services, and spices, India also imports crude oil, electronics, and machinery to fuel its growing economy. 
    Fun fact: India is the birthplace of yoga, a practice over 5,000 years old and a gift to the world!"""},
    {"input": "USA", "output": """Located in North America, the United States is the 3rd largest country by both land area and population, with over 331 million people. It spans diverse zones, from the Arctic cold of Alaska to the tropical warmth of Florida. The U.S. experiences a wide range of climates, from arid deserts to humid subtropics. As a federal republic, the U.S. has a significant global influence, having gained independence in 1776. Known for its exports like technology, machinery, and vehicles, the U.S. imports crude oil, electronics, and pharmaceuticals. Fun fact: The U.S. is home to the world’s largest economy and some of the most iconic landmarks, like the Statue of Liberty and the Grand Canyon!"""},
]



# This is a prompt template used to format each individual example.
example_prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}"),
        ("ai", "{output}"),
    ]
)
few_shot_prompt = FewShotChatMessagePromptTemplate(
    example_prompt=example_prompt,
    examples=examples,
)



final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "you are a youtube content writer who writes scripts for shorts that are under 60 seconds"),
        few_shot_prompt,
        ("human", "Tell me about {input}?"),
    ]
)


chain = final_prompt | model

result = chain.invoke({"input": "Iceland"})



# ---- LangChain OpenAI Chat Model Example ----


# Invoke the model with message
print(f"{result.content}")



# Print all loaded environment variables
# for key, value in os.environ.items():
#     print(f"{key}: {value}")
