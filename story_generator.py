from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
from datetime import datetime
import json


def generate_short_script(input_dict):
    # Load environment variables
    # load_dotenv()

    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Create the few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    # Examples to use for few-shot learning
    story_examples = [
        {
            "input": "A heroic journey in a dystopian future",
            "output": """War and ecological collapse have reduced the world to ruins, where one man dares to rise against all odds to restore hope. Relying solely on his wits and an ancient map, he braves treacherous wastelands to infiltrate the enemy's stronghold. Along the way, unexpected allies join him, and together they uncover a secret that holds the power to either save humanity or doom it forever.""",
        },
        {
            "input": "A tale of friendship between a boy and a dragon",
            "output": """In a secluded mountain village, a young boy stumbles upon a wounded dragon hidden away in a cave. Ignoring the warnings of his elders, he cares for the dragon, forming a bond that transcends their differences. As the dragon heals, the boy learns of a prophecy that entwines their fates. Together, they embark on a journey to confront the forces threatening their world, proving that friendship can conquer even the darkest evils.""",
        },
        {
            "input": "A detective solving a mystery in a haunted mansion",
            "output": """Shrouded in mist, the forest conceals an old mansion long abandoned and whispered to be haunted. When a series of mysterious deaths rattles the nearby town, a seasoned detective is summoned to unravel the truth. As he delves deeper into the mansion’s dark history, he uncovers secrets that refuse to stay buried and realizes that the past may still have a deadly grip on the present.""",
        },
    ]

    # Create a few-shot prompt template for storytelling
    story_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=story_examples,
    )

    # Create the final prompt template for the story
    story_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a professional storyteller with 40 years of experience. You specialize in crafting short, engaging stories that captivate your audience, whether they are readers, viewers, or listeners. Your stories are concise, yet rich in detail and emotion, making them perfect for capturing attention in a brief format. Start the story in an intriguing way, avoiding clichés like 'In the...' or similar phrases. Be creative, and ensure that all names used for characters, places, and objects are original and not copied from existing works. Additionally, avoid the use of special characters or any unnecessary punctuation. Output the story as a plain, continuous narrative with no titles, headers, or any additional text—just the story itself.",
            ),
            story_few_shot_prompt,
            ("human", f"Create a story about {input_dict['topic']}"),
        ]
    )

    result = story_final_prompt | model | StrOutputParser()
    return result.invoke({"input_dict": input_dict})


def improve_story(story, iterations=1):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Create the few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )
    improved_story_examples = [
        {
            "input": "War and ecological collapse have left the world in ruins, and one man rises against all odds to restore hope. Armed with nothing but his wits and an ancient map, he ventures across treacherous wastelands and into the heart of the enemy's domain. Along the way, he encounters unexpected allies and discovers a secret that could save humanity—or doom it forever.",
            "output": """A barren wasteland stretches endlessly under a perpetually darkened sky, where hope is a distant memory. Yet one man, driven by a fire that refuses to die, embarks on a perilous journey to reclaim it. Armed only with his instincts and an ancient map passed down through generations, he crosses shifting sands and abandoned cities, each step bringing him closer to the enemy's stronghold. Along the way, unexpected allies—survivors clinging to the possibility of a better future—join him. Together, they brave deadly storms, outwit enemy forces, and uncover a forgotten secret that holds the power to breathe life back into their dying world. In the end, it’s not just survival at stake, but the rekindling of hope in a broken world.""",
        },
        {
            "input": "A young boy from a remote mountain village discovers a wounded dragon hiding in a cave. Despite his elders' warnings, he tends to the creature, forming an unbreakable bond. As the dragon regains strength, the boy learns of a prophecy that links their fates. Together, they set out to confront the forces threatening their world, proving that friendship can overcome even the greatest of evils.",
            "output": """High in mist-covered mountains where ancient legends whisper through the trees, a young boy stumbles upon a wounded dragon, its emerald scales dulled with pain. Ignoring the elders' warnings of danger, the boy is guided by his heart to care for the beast. As the dragon heals, a bond stronger than blood forms between them—a bond destined to be tested by a prophecy long forgotten. Together, they soar through treacherous skies, confront sinister forces, and uncover hidden truths. Their unyielding friendship turns the tide, showing that even the smallest acts of kindness can alter the course of destiny.""",
        },
        {
            "input": "A fog-covered forest conceals an old mansion, long abandoned and rumored to be haunted. A series of mysterious deaths in the nearby town prompts a seasoned detective to investigate. As he delves into the case, he uncovers dark secrets about the mansion's past and realizes that the ghosts of the past may still be very much alive.",
            "output": """Thick fog hangs over the forest, shrouding an old mansion in mystery, its decaying walls whispering of secrets long buried. When the first body is discovered in the nearby town, the locals avoid mentioning the mansion. But as deaths continue, they turn to the one man who might solve the mystery. The detective, known for his unflinching resolve, arrives with nothing but his intuition and a burning curiosity. As he navigates the mansion's shadowed halls, he feels the weight of the past pressing in. Every creak of the floorboards and flicker of candlelight hints at something not entirely of this world. Unraveling the mansion’s dark history—betrayal, murder, and a curse that still lingers—he soon realizes that some spirits refuse to rest. But understanding human nature, not the supernatural, ultimately allows him to escape the mansion's deadly grasp and bring peace to the restless dead.""",
        },
    ]

    # Create a few-shot prompt template for improving stories
    improved_story_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=improved_story_examples,
    )

    # Improvement process
    improved_story = story
    for _ in range(iterations):
        # Create the final prompt template for improving a story
        improvement_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a professional short story writer and editor with 40 years of experience in refining and enhancing narratives. You specialize in the style of Brandon Sanderson, known for his engaging, immersive storytelling, well-developed characters, and intricate world-building. Your task is to take the provided story and improve it by making it more engaging, adding depth to characters, enriching the plot, and refining the language. Start the story in an intriguing way, avoiding clichés like 'In the...' or similar phrases. Be creative, and ensure that the output uses original names for characters, places, and objects, without relying on any existing names. Avoid the use of special characters or unnecessary punctuation. Your goal is to create a polished, compelling short story that keeps the viewer or listener fully captivated from beginning to end. Please ensure the output is a continuous narrative with no titles, headers, special characters, or any additional text—just the improved story itself in plain text.",
                ),
                improved_story_few_shot_prompt,
                ("human", f"Here is a story that needs improvement: {improved_story}"),
                ("ai", "Improve the story and return it."),
            ]
        )

        result = improvement_prompt | model | StrOutputParser()
        improved_story = result.invoke({"input_dict": {"story": improved_story}})

    return improved_story


def generate_youtube_title_description(story):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the YouTube title and description
    title_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in creating concise, captivating YouTube titles that reflect the core essence of a story. \
            Your task is to generate only the YouTube title, no additional text or special characters, ensuring it is engaging, short, and to the point. \
            Do not use quotation marks or any unnecessary punctuation in the title.",
            ),
            (
                "human",
                f"Generate a compelling YouTube title for the following story:\n\n{story}",
            ),
        ]
    )

    description_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in creating captivating YouTube descriptions that reflect the core essence of a story. \
         Your task is to generate only the YouTube description, which should be engaging and informative, summarizing the key elements of the story to entice viewers to watch. \
         Keep it concise, avoid spoilers, and ensure it highlights the main themes and intrigue.",
            ),
            (
                "human",
                f"Generate a compelling YouTube description for the following story:\n\n{story}",
            ),
        ]
    )

    # Process the story using the model
    title_result = title_prompt | model | StrOutputParser()
    title_response = title_result.invoke({"input_dict": {"story": story}})

    description_result = description_prompt | model | StrOutputParser()
    description_response = description_result.invoke({"input_dict": {"story": story}})

    # Split the response into title and description (assuming the response is well-structured)
    # lines = response.split("\n")
    # title = lines[0].strip()  # First line as the title
    # description = " ".join(line.strip() for line in lines[1:]).strip()  # Rest as the description

    return {
        "youtube_title": title_response,
        "youtube_description": description_response,
    }


def generate_story(model, input_dict):

    # Create the final prompt template for the story
    story_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are a professional storyteller with 40 years of experience. You specialize in crafting short, engaging stories that captivate your audience, whether they are readers, viewers, or listeners. Your stories are concise, yet rich in detail and emotion, making them perfect for capturing attention in a brief format. Start the story in an intriguing way, avoiding clichés like 'In the...' or similar phrases. Be creative, and ensure that all names used for characters, places, and objects are original and not copied from existing works. Additionally, avoid the use of special characters or any unnecessary punctuation. Output the story as a plain, continuous narrative with no titles, headers, or any additional text—just the story itself.",
            ),
            (
                "human",
                f"""
             You are a writer with 40 years of experience in writing short stories and have won many awards like Mary Robinette.

Story Structure: Utilize the MICE Quotient (Milieu, Inquiry, Character, Event) to structure your story. You may combine multiple elements and nest them appropriately by opening and closing threads in sequence (e.g., open Milieu <M>, then Inquiry <I>, and close in reverse </I></M>).

Opening: In the first three sentences, establish:

Who: Introduce the main character through action, highlighting their attitude or a defining trait.
Where: Set the scene using a sensory detail to ground the reader.
Genre: Include a genre-specific detail to orient the reader.
Conflict Introduction:

Goal: Clearly state what the character is trying to achieve and why it matters to them.
Obstacle: Introduce what is preventing them from reaching their goal.
Try-Fail Cycles:

Incorporate at least one try-fail cycle where the character attempts to overcome the obstacle and fails, making the situation worse.
Use "Yes, but" or "No, and" structures to escalate tension and complicate the character's efforts.
Resolution:

Transition to a try-succeed cycle where the character finally overcomes the obstacle.
Use "Yes, and" or "No, but" structures to move toward resolution and show progress.
Ending:

Close out the MICE elements you opened, mirroring the opening.
Re-establish the Who, Where, and Genre/Mood, showing how things have changed.
Provide a satisfying conclusion that delivers a specific emotional impact.
Character and Setting Limitations:

Limit the story to no more than two characters and one location to maintain focus and brevity.
Instructions:

Use the topic provided ({input_dict['topic']}) to craft your story.
Ensure that your story follows the MICE Quotient structure, opening and closing threads appropriately.
Incorporate sensory details and character actions to engage the reader.
Focus on delivering a specific emotional experience through the story.
             """,
            ),
        ]
    )

    result = story_final_prompt | model | StrOutputParser()
    return result.invoke({"input_dict": input_dict})


if __name__ == "__main__":
    # Initial story generation
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    iteration_needed = 2
    input_dict = {
        "topic": "'The Hereditary Hack': A second-generation cybercriminal discovers her legendary parents' last heist is still running in the background of the internet. What world-changing secret is lurking in the code, and why did they hide it from her?"
    }
    story = generate_story(model, input_dict)
    print(f"story ---> {story}")
    # story = generate_short_script(input_dict)
    # print(f"story --> {story}")
    # # Improve the generated story twice
    # improved_story = improve_story(story, iterations=iteration_needed)
    improved_story = story
    print(improved_story)
    youtube_details = generate_youtube_title_description(improved_story)

    # Create the final dictionary to save
    story_dict = {
        "story": improved_story,
        "youtube_details": youtube_details,
    }

    # Generate the filename and folder based on the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f"data/{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    filename = os.path.join(folder_name, f"codex_{timestamp}.json")

    # Save the dictionary to a JSON file
    with open(filename, "w") as f:
        json.dump(story_dict, f, indent=4)

    # Print the location of the saved file
    print(f"\nStory saved to {filename}")
