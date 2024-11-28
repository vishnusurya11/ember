# from typing import List

# from pydantic import BaseModel, Field



# class Reflection(BaseModel):
#     missing: str = Field(description="Critique of what is missing.")
#     superfluous: str = Field(description="Critique of what is superfluous")


# class AnswerQuestion(BaseModel):
#     answer: str = Field(description="~1000 word detailed answer to the question")
#     reflection: str = Field(description="Your reflection on the initial answer")
#     search_queries: List[str] = Field(
#         description="1-3 search queries for researching improvements to address the critique of your current answer"
#     )





# if __name__ == "__main__":
#     print("Hey schema")

from typing import List

from langchain_core.pydantic_v1 import BaseModel, Field


class Reflection(BaseModel):
    missing: str = Field(description="Critique of what is missing.")
    superfluous: str = Field(description="Critique of what is superfluous")


class AnswerQuestion(BaseModel):
    """Answer the question."""

    answer: str = Field(description="~1000 word detailed answer to the question.")
    reflection: Reflection = Field(description="Your reflection on the initial answer.")
    search_queries: List[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )

class ReviseAnswer(AnswerQuestion):
    references: List[str] = Field(description="Citations motivating your updated answer")