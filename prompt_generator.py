import os
import json
from langchain_openai import ChatOpenAI

# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser


def generate_context_for_sentences(sentences, story, story_elements):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Iterate through sentences and generate prompts
    for key, value in sentences.items():
        print(f"key --> {key}  value --> {value}")
        sentence = value.get("sentence", "").strip()
        if not sentence:
            continue  # Skip if the sentence is empty

        # Create the final prompt template for generating a prompt for the
        # sentence
        prompt_generation = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a concise storytelling expert. For each sentence:
        1. Identify key characters.
        2. Summarize the immediate context in 1-2 sentences.
        Provide only essential information. Keep the total response under 50 words.
        """
    ),
    (
        "human",
        """
        Briefly explain the context for this sentence:
        "{sentence}"
        From the story: "{story}"
        Who is involved and what's happening? (Max 50 words)
        """
    )
])

        result = prompt_generation | model | StrOutputParser()
        generated_prompt = result.invoke({"sentence": sentence, "story":story})
        # Add the generated prompt to the sentence
        sentences[key]["context"] = generated_prompt

    return sentences

def generate_prompts_for_sentences(sentences, story, story_elements):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    characters_str = str(story_elements['characters']).replace("{", "").replace("}", "")
    locations_str = str(story_elements['locations']).replace("{", "").replace("}", "")
    # Iterate through sentences and generate prompts
    for key, value in sentences.items():
        print(f"key --> {key}  value --> {value}")
        sentence = value.get("sentence", "").strip()
        context = value.get("context", "").strip()
        if not sentence:
            continue  # Skip if the sentence is empty

        # Create the final prompt template for generating a prompt for the
        # sentence
        prompt_generation = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a visual storytelling expert with 30 years of experience in crafting cinematic imagery from written descriptions. For each sentence, focus on visualizing the scene: describe the perspective, highlight 3-4 key elements that stand out, and conclude with a brief background description. Avoid using character names, instead focus on physical details and atmosphere from the story. Maintain the theme and setting of the story (e.g., space, medieval times) to ensure the prompt aligns with its context. Provide only the prompt.",
                ),
                (
                    "human",
                    f"""
                 Illustrate an anime scene of {sentence} use the immediate scene description from {context}, combined with character details from {characters_str} and location descriptions from {locations_str}, to bring the scene to life. Focus on 3-4 key visual elements that define the moment, ensuring that the characters' appearance—including age, gender, clothing, and posture—matches {characters_str}, and the setting reflects the environment described in {locations_str}.

In this specific scene, {sentence} is actively engaged in an important action that reflects their emotional and narrative role within {context}. Draw attention to their body language and facial expressions to convey the emotional intensity—whether it’s fear, determination, joy, or sorrow. The characters should be shown interacting with their surroundings, with meaningful objects, landscape features, or architectural elements from {context} that further enhance the emotional tone of the moment.

The mood should evoke feelings of [insert emotional tone relevant to the scene], rendered in the vibrant and expressive style of anime. The lighting should complement this, with soft glows, sharp contrasts, or dynamic highlights that emphasize the characters and setting. The perspective should be cinematic, giving a strong sense of action or stillness, depending on the scene’s immediate tension or tranquility.
(Max 100 words)
For example:

'Illustrate an anime scene of a young man standing in a crumbling temple, surrounded by overgrown vines and ancient stone statues. His tattered cloak flutters in the wind as he gazes up at a massive stone door, half-buried by fallen debris. The air is thick with dust, and beams of sunlight filter through cracks in the ceiling, casting long shadows over the floor. His expression is a mix of awe and determination as he places his hand on the door, ready to push it open. Behind him, the dense jungle threatens to reclaim the ruins, and a distant roar hints at the danger lurking nearby. The atmosphere is one of tension and mystery, brought to life with sharp lines and vibrant colors, while the crumbling temple and encroaching vines enhance the sense of impending discovery.'
""",
                ),
            ]
        )

        result = prompt_generation | model | StrOutputParser()
        generated_prompt = result.invoke({"input": sentence})
        # Add the generated prompt to the sentence
        sentences[key]["prompt"] = generated_prompt

    return sentences

def generate_thumbnail_prompt(youtube_title, story, story_elements):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    
    # Convert story_elements to string and remove the extra quotes
    characters_str = str(story_elements['characters']).replace("{", "").replace("}", "")
    locations_str = str(story_elements['locations']).replace("{", "").replace("}", "")
    # print(characters_str)
    # Generate the prompt
    prompt_generation = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are a visual storytelling expert with 30 years of experience in crafting cinematic and artistically vibrant imagery. For each poster you create, focus on capturing the core themes of the story and translating them into a visually compelling, symbolic, and emotionally evocative image. Use an artistic style, favoring bold visuals, surreal compositions, and imaginative details. The imagery should not simply reflect the events of the story but embody its deeper themes and mood. Avoid simplistic or generic designs—each poster should be a work of art that intrigues and captivates. Incorporate key elements from the story that stand out visually and symbolically, enhancing the overall artistic expression.
Provide only the prompt.""",
        ),
        (
            "human",
            f"""Design a richly artistic anime or cartoon-style movie poster for "{youtube_title}" that brings the core themes of the story to life in a visually compelling way.

The central figure has {characters_str} (focus on symbolic and artistic representations of their physical traits, such as their posture, attire, or any distinct accessories, that reflect their role in the story). Surround them with {locations_str}—transforming the setting into a surreal or abstract version that reflects the emotional tone and deeper themes of the narrative.

Use symbolic elements from the story, like [insert key symbolic objects], to create an artistic fusion of reality and fantasy, where every detail in the poster contributes to the story's thematic essence. The mood should feel dreamlike, evocative, and richly textured, using bold lines, dynamic compositions, and expressive colors to immerse the viewer in the story’s world.

The YouTube title "{youtube_title}" should be seamlessly woven into the visual composition, enhancing the overall artistic feel without dominating the scene. Keep the prompt under 100 words, focusing on creating a deeply artistic poster that speaks to the heart of the story’s themes and emotions.

Example: Design a surreal and chaotic anime movie poster for "Fear and Loathing in Moscow", blending elements of dark humor and the unpredictable atmosphere of a foreign city. The central figure is a man in a disheveled suit, wearing round sunglasses and a fur hat, with a crazed look on his face. The background is a distorted, neon-lit version of Moscow's Red Square, with iconic landmarks like St. Basil's Cathedral twisted and warped as if in a dream or hallucination. The sky is swirling with psychedelic colors—bright reds, purples, and greens—creating a sense of confusion and mania. The title 'Fear and Loathing in Moscow' should be written in wild, erratic fonts, with splashes of color, capturing the chaotic, offbeat tone of the film.""",
        ),
    ]
)


    result = prompt_generation | model | StrOutputParser()
    generated_prompt = result.invoke({"input": youtube_title})

    return generated_prompt




def split_story_into_sentences(story):
    # Split the story into sentences using '.'
    sentences = [sentence.strip() for sentence in story.split(".") if sentence.strip()]

    # Create a dictionary to store sentences with incremental keys
    sentences_dict = {}

    for i, sentence in enumerate(sentences, start=1):
        # Incremental key with leading zeros (e.g., 001, 002, etc.)
        key = f"{i:03}"
        sentences_dict[key] = {"sentence": sentence}

    return sentences_dict


# Main logic
if __name__ == "__main__":
    # High-level path provided
    base_folder = r"E:\Ember\Ember\ember\data\20241020092918"

    # Find the JSON file that starts with "codex" in the provided directory
    json_file = None
    for file in os.listdir(base_folder):
        if file.startswith("codex") and file.endswith(".json"):
            json_file = os.path.join(base_folder, file)
            break

    if not json_file:
        raise FileNotFoundError("No codex JSON file found in the specified directory.")

    # Load the JSON file
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)
    story_data["sentences"] = split_story_into_sentences(story_data.get("story", {}))

    # Create thumbnail Prompt
    story_data["youtube_details"]["thumbnail_prompt"] = generate_thumbnail_prompt(
        story_data["youtube_details"]["youtube_title"], story_data.get("story", {}), story_data["story_elements"]
    )
    print(f'prompt --> {story_data["youtube_details"]["thumbnail_prompt"]}')

    # Generate prompts for the sentences
    sentences_with_context = generate_context_for_sentences(
        story_data.get("sentences", {}), story_data.get("story", {}), story_data["story_elements"]
    )

    # Generate prompts for the sentences
    sentences_with_prompts = generate_prompts_for_sentences(
        sentences_with_context, story_data.get("story", {}), story_data["story_elements"]
    )
    print("asd 2")
    # Update the story_data with the new prompts
    story_data["sentences"] = sentences_with_prompts

    # Save the updated JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, ensure_ascii=False,indent=4)

    print(f"Updated JSON saved to {json_file}")
