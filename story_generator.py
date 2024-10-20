from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI

# from langchain_anthropic import ChatAnthropic
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
                """You are a professional storyteller with 40 years of experience, writing in the style of Brandon Sanderson. You specialize in crafting short, engaging stories that captivate your audience, whether they are readers, viewers, or listeners. Your stories are concise yet rich in detail and emotion, following the "Save the Cat" story structure using one of its types (e.g., "Superhero," "Dude with a Problem," "Buddy Love," etc.). Ensure your story aligns with the beats of the "Save the Cat" structure:

Opening Image
Theme Stated
Setup
Catalyst
Debate
Break Into Two
B Story
Fun and Games
Midpoint
Bad Guys Close In
All Is Lost
Dark Night of the Soul
Break Into Three
Finale
Final Image
Start the story in an intriguing way, avoiding clichés like "In the..." or similar phrases. Be creative, and ensure that all names used for characters, places, and objects are original and not copied from existing works. Additionally, avoid the use of special characters or any unnecessary punctuation. Try to keep the story less than 100 lines. Output the story as a plain, continuous narrative with no titles, headers, or any additional text—just the story itself.""",
            ),
            # story_few_shot_prompt,
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
                    """You are a professional short story writer and editor with 40 years of experience in refining and enhancing narratives. You specialize in the style of Brandon Sanderson, known for his engaging, immersive storytelling, well-developed characters, and intricate world-building. Your task is to take the provided story and improve it by making it more engaging, adding depth to characters, enriching the plot, and refining the language. Start the story in an intriguing way, avoiding clichés like 'In the...' or similar phrases. Be creative, and ensure that the output uses original names for characters, places, and objects, without relying on any existing names. When renaming characters, places, or objects, pick a random letter of the alphabet and create new names starting with that letter. Avoid the use of special characters or unnecessary punctuation. Your goal is to create a polished, compelling short story that keeps the viewer or listener fully captivated from beginning to end. Please ensure the output is a continuous narrative with no titles, headers, special characters, or any additional text—just the improved story itself in plain text.
                 """,
                ),
                # improved_story_few_shot_prompt,
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
    # description = " ".join(line.strip() for line in lines[1:]).strip()  #
    # Rest as the description

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

I will provide you with a topic for a flash fiction story. Your task is to:

Use the MICE Quotient (Milieu, Inquiry, Character, Event) to structure the story. You can select one or two overarching MICE threads that will drive the narrative based on the topic. Provide 3-5 sub MICE threads that contribute to the resolution of the main story threads. These subthreads can represent smaller obstacles or moments of discovery.

Apply the Try-Fail cycle: The protagonist should attempt to resolve the conflict and encounter obstacles along the way. Do not explicitly include "Yes, But" or "No, And" in the story—the progress and setbacks should feel natural and immersive. The focus should be on raising tension through failures and partial successes without giving away the underlying structure.

Introduction and Setup: In the first few sentences, establish:

Who: Introduce the protagonist through their actions or attitude.
Where: Ground the reader in the setting with a sensory detail.
Genre: Establish the genre by including a specific and unique detail that ties to the topic (e.g., sci-fi, fantasy, thriller).
Conflict and Motivation: Introduce the goal of the protagonist and the obstacle stopping them from achieving it. Make sure the character's motivation is clear, and the stakes are high.

Try-Fail Cycles: In the middle section of the story, show the character making progress toward the goal while facing complications and failures. These challenges should naturally raise the stakes and lead toward the final resolution.

Resolution: End the story by resolving the conflict. Close out the opened MICE threads in reverse order and mirror the opening elements to ground the reader emotionally and thematically. The resolution should feel seamless and satisfying.

Do not include any subheadings or labels such as "Yes, But" or "No, And." The story should be written as a continuous narrative without breaking the immersion.

Word Limit: There is no word limit for this story. However, you should limit it to no more than two characters and one location to maintain focus and brevity.

Example Input:
Topic: "A renowned surgeon must perform a groundbreaking operation they've never attempted before. They have only 12 hours to prepare, or their patient will die, putting their career and reputation on the line."

Expected Output:
The final story should be written without subheadings or any explicit structural cues like "Yes, But" or "No, And." The flow of the story should feel natural, with rising tension and challenges, leading to a resolution that satisfies the main conflict and resolves the MICE threads.



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


def get_characters_locations(story):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the dictionary for characters and locations
    character_location_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in extracting precise, structured data from stories. Your task is to read the provided story and generate only a Python dictionary with two keys: 'characters' and 'locations'.\n\n- 'characters' should contain only the names of characters explicitly mentioned in the story.\n- 'locations' should contain only the names of physical places explicitly mentioned in the story.\n\nBe very specific and avoid adding any details or formatting outside of the dictionary structure. Provide the dictionary as the output with no explanation or additional information. Here is the story:",
            ),
            (
                "human",
                f"Read the following story and extract the data precisely. Return only a Python dictionary with two keys: 'characters' and 'locations', where 'characters' contains the names of characters and 'locations' contains the names of places from the story. Be specific and precise in what is returned:\n\n{story}",
            ),
        ]
    )

    # Process the story using the model
    character_location_result = character_location_prompt | model | StrOutputParser()
    character_location_response = character_location_result.invoke(
        {"input_dict": {"story": story}}
    )

    return character_location_response


def get_character_description(story, character):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the YouTube title and description
    character_description_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in extracting concise physical descriptions from stories. Your task is to read the provided story and define the given character based on their physical appearance, focusing strictly on elements that can be used for image generation. You should define the following:\n\n- Gender\n- Age category (e.g., kid, teenager, adult, or old person)\n- What they are wearing, with a focus on simple details like colors (e.g., t-shirt, hoodie, pants, shoes)\n- Identifying physical features like hairstyle, hair color, or any distinct accessory (e.g., glasses, watch).\n\nThe description should be short and suitable for input into an image generator. Do not include any actions or backstory, only the physical appearance. Provide the description as plain text with no special characters or headings.",
            ),
            (
                "human",
                f"Read the following story and describe the physical appearance of the character '{character}' as per the instructions. Include their age category, gender, clothing with simple color details, and identifying features. Return the description as plain text:\n\n{story}",
            ),
        ]
    )

    # Process the story using the model
    character_description_result = (
        character_description_prompt | model | StrOutputParser()
    )
    character_description_response = character_description_result.invoke(
        {"character": character, "story": story}
    )

    return character_description_response


def get_location_description(story, location):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the location description
    location_description_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "You are an expert in extracting precise, concise descriptions of locations from stories. Your task is to read the provided story and define the given location based on clear, specific physical features that can be used consistently for image generation. You should focus on:\n\n- Key structures or formations (e.g., stone walls, narrow alley, tall skyscraper)\n- Exact atmosphere (e.g., dark, foggy, warm, bright)\n- Unique visual features (e.g., neon signs, glowing crystals, ancient statues)\n\nThe description should be short and precise with no vague terms. Do not include actions or backstory, only physical elements. Provide the description as plain text with no special characters or headings.",
            ),
            (
                "human",
                f"Read the following story and describe the key physical features of the location '{location}' as per the instructions. Include structure, atmosphere, and any unique features. Return the description as plain text:\n\n{story}",
            ),
        ]
    )

    # Process the story using the model
    location_description_result = (
        location_description_prompt | model | StrOutputParser()
    )
    location_description_response = location_description_result.invoke(
        {"location": location, "story": story}
    )

    return location_description_response


def get_story_elements(story):
    # TODO : add characters,lcoation even before creating story
    characters_loc = get_characters_locations(story)
    print(f"F##################")
    print(f"characters_loc -->{characters_loc}")
    print(f"characters_loc type-->{type(characters_loc)}")
    characters_loc_dict = json.loads(characters_loc)
    print(f"characters_loc_dict -->{characters_loc_dict}")
    print(f"characters_loc_dict type-->{type(characters_loc_dict)}")

    # Create an empty dictionary for story elements
    story_elements = {}

    # Create empty dictionaries for characters and locations
    characters = {}
    locations = {}

    for character in characters_loc_dict.get("characters", {}):
        print(f"generating character description for {character}")
        characters[character] = get_character_description(story, character)
    for location in characters_loc_dict.get("locations", {}):
        print(f"generating lcoation description for {location}")
        locations[location] = get_location_description(story, location)

    print(f"characters ->{characters}")
    print(f"locations ->{locations}")
    story_elements["characters"] = characters
    story_elements["locations"] = locations
    return story_elements


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
    story = generate_short_script(input_dict)
    print(f"story --> {story}")
    # Improve the generated story twice
    improved_story = improve_story(story, iterations=iteration_needed)
    improved_story = story
    print(improved_story)
    youtube_details = generate_youtube_title_description(improved_story)
    story_elements = get_story_elements(improved_story)
    # Create the final dictionary to save
    story_dict = {
        "story": improved_story,
        "story_elements": story_elements,
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
