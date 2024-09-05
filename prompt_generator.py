import os
import json
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser


def generate_prompts_for_sentences(sentences):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")

    # Example prompts to guide the generation process
    prompt_examples = [{"input": "In the sprawling metropolis of Zenith Prime, neon lights pulsed against the backdrop of a star-studded void, illuminating the shadows of a city teetering on the edge of chaos.",
                        "output": "A cinematic 8K ultra-realistic image of a futuristic city at night, where neon lights pierce through the darkness, casting sharp reflections on wet streets. The cityscape is a blend of towering skyscrapers and narrow alleyways, with shadows lurking in every corner. The perspective is from street level, capturing the vibrant yet ominous atmosphere of a metropolis on the brink of collapse.",
                        },
                       {"input": "Detective Elara Quinn stood at the threshold of an enigma that stretched across the galaxies.",
                        "output": "A cinematic 8K ultra-realistic image of a lone figure standing at the edge of a vast, star-filled galaxy. The character is silhouetted against the shimmering backdrop of distant stars and swirling cosmic clouds. The perspective is from behind, emphasizing the enormity of the galaxy and the solitary figure poised to uncover its mysteries.",
                        },
                       {"input": "The air was thick with foreboding as she stepped onto the silent vessel, the ship a ghostly reminder of a forgotten past.",
                        "output": "A cinematic 8K ultra-realistic image of a deserted spaceship interior, dimly lit with flickering lights. The metallic walls are covered in rust and old markings, telling stories of a once-active crew. The perspective is from slightly above, showing the character entering the corridor, with shadows and eerie silence amplifying the sense of dread.",
                        },
                       ]

    # Create the few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    # Update the system prompt to be more descriptive
    prompt_few_shot_template = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=prompt_examples,
    )

    # Iterate through sentences and generate prompts
    for key, value in sentences.items():
        sentence = value.get("sentence", "").strip()
        if not sentence:
            continue  # Skip if the sentence is empty

        # Create the final prompt template for generating a prompt for the
        # sentence
        prompt_generation = ChatPromptTemplate.from_messages(
            [
                ("system",
                 "You are a visual storytelling expert with 30 years of experience in crafting perfect imagery based on written descriptions. Your task is to describe each sentence visually, focusing on creating a cinematic, ultra-realistic image in 8K resolution. Do not use the names from the sentence; instead, describe the qualities and details that can be visually seen. Start by describing the perspective, followed by 3-4 elements that stand out and can be visually captured. Finally, provide a brief description of the background to complete the scene. Return only the prompt, without any headings or additional text.",
                 ),
                prompt_few_shot_template,
                ("human",
                 f"Create a prompt for the sentence: {sentence}"),
            ])

        result = prompt_generation | model | StrOutputParser()
        generated_prompt = result.invoke({"input": sentence})
        # Add the generated prompt to the sentence
        sentences[key]["prompt"] = generated_prompt

    return sentences


# Main logic
if __name__ == "__main__":
    # High-level path provided
    base_folder = r"E:\Ember\Ember\ember\data\20240904192910"

    # Find the JSON file that starts with "codex" in the provided directory
    json_file = None
    for file in os.listdir(base_folder):
        if file.startswith("codex") and file.endswith(".json"):
            json_file = os.path.join(base_folder, file)
            break

    if not json_file:
        raise FileNotFoundError(
            "No codex JSON file found in the specified directory.")

    # Load the JSON file
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    # Generate prompts for the sentences
    sentences_with_prompts = generate_prompts_for_sentences(
        story_data.get("sentences", {})
    )

    # Update the story_data with the new prompts
    story_data["sentences"] = sentences_with_prompts

    # Save the updated JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"Updated JSON saved to {json_file}")
