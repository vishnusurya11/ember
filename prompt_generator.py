import os
import json
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser


def generate_prompts_for_sentences(sentences, story):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Example prompts to guide the generation process
    prompt_examples = [{"input": "In the context of the In a city once alive with alchemical marvels, a shadow lingered over the name Thoren, whispered among the populace like a dark omen. Once celebrated as a prodigy, Thoren had become a pariah, forever haunted by the specters of his past\u2014a catastrophic experiment that had claimed lives, including those of his dearest friends. The weight of his shame pressed heavily upon him, gnawing at his spirit like a relentless beast. Desperation surged within him, igniting a fierce determination to restore his tarnished legacy. Whispers of the fabled Philosopher's Stone\u2014a legendary artifact said to grant immense power\u2014pierced through his despair, sparking a glimmer of hope. It was rumored to be hidden within the towering fortress of Eldrin, an enigmatic wizard whose mastery of magic was both revered and feared.\n\nDriven by a singular purpose, Thoren set out to forge a team capable of breaching the ancient stronghold. His first ally was Mira, a nimble thief known for her cunning and unmatched agility in the city's underbelly. With raven-black hair framing her sharp features and eyes that sparkled with mischief, she embodied the stealth and cleverness he needed. Next came Jarek, a former knight whose unwavering loyalty and strength offered a bulwark against the dangers ahead. His imposing frame and the glint of his sword instilled a sense of security that Thoren found comforting. Lastly, they welcomed Lira, a spirited young sorceress whose flair for illusions could deceive even the most vigilant of guards. Her laughter echoed like a bright melody, infusing their grim mission with a sense of joy, while her wild auburn hair danced like flames in the wind.\n\nUnder the cover of night, they approached Eldrin's tower, its silhouette a foreboding monolith against the moonlit sky. The air shimmered with tension as they crossed the threshold, and a cascade of magical wards flared to life, casting an eerie glow over the dim corridors. Mira took the lead, her instincts sharp as she navigated them past perilous traps and concealed pitfalls. As Thoren whispered ancient incantations, he deftly dispelled minor enchantments that sought to ensnare them in their web of magic.\n\nDeeper into the tower they ventured, the atmosphere thickening with potent enchantments, the walls pulsating as if alive. Their first trial manifested in the form of a colossal stone golem, its eyes aflame with an otherworldly fire, a formidable guardian of Eldrin's secrets. Jarek stepped forward, sword gleaming ominously as he braced for battle. But Lira, ever quick-witted, raised her hands, weaving a complex illusion that conjured a phantom enemy behind the golem. For a heartbeat, confusion crossed the creature's stony face as it turned, allowing them to slip past unharmed, their hearts racing with the thrill of their narrow escape.\n\nThey ascended further, each chamber revealing mesmerizing illusions of the Philosopher's Stone, each more convincing than the last. Thoren's pulse quickened as he recognized the trap laid before them. With Lira's guidance, he focused his mind, calling upon the principles of alchemy that had once defined his greatness, discerning reality from illusion.\n\nAt last, they reached the inner sanctum, where Eldrin awaited, surrounded by swirling energies and arcane symbols. The air crackled with power as the wizard's piercing gaze landed on Thoren, a blend of disdain and curiosity flickering in his eyes. The confrontation unfolded like a deadly dance, their words cutting sharper than the finest blade, revealing the depths of Thoren's desperation and Eldrin's unyielding pride.\n\nAs tension reached its zenith, Mira seized the moment. She dashed toward the pedestal that held the real stone, but Eldrin's magic surged forth, unleashing a tempest of energy that threatened to engulf them. In that critical instant, Thoren\u2019s heart raced; he understood that brute strength would not win this day. Drawing upon his alchemical knowledge, he combined elements from the room to create a stunning flash of light that shattered Eldrin's concentration, granting them the diversion they desperately needed.\n\nLira conjured an illusion of a fearsome beast, a terrifying creature of fangs and claws that roared to life, distracting Eldrin long enough for Mira to claim the stone. With Jarek standing resolutely in front, sword drawn, he blocked the wizard's path, allowing the others to escape as the tower trembled under Eldrin's wrath.\n\nAs dawn broke, painting the horizon in hues of gold and crimson, they emerged from the forest, the Philosopher's Stone clutched tightly in their hands. Thoren's heart swelled with a mix of pride and redemption; they had faced down illusions and guardians, proving that friendship and courage could forge a new path. The city awaited, and with the stone, Thoren would not only reclaim his name but also ignite a renaissance of alchemical wonder. In the end, it was not merely the stone that mattered, but the bonds they had forged in the crucible of adversity. Together, they had rewritten the narrative of their lives, one filled with hope, bravery, and the promise of a brighter future. create a prompt for With raven-black hair framing her sharp features and eyes that sparkled with mischief, she embodied the stealth and cleverness he needed",
                        "output": "Close-up realistic photo of a lithe figure, captured from a slight angle, her raven-black hair framing her angular, sharp features. Her eyes, bright and full of mischief, reflect the subtle glimmer of street lamps or the faint moonlight overhead, hinting at her cleverness and agility. Her posture is poised, ready to move with swift precision. The background reveals the dimly lit, narrow alleyways of a bustling, medieval-style city, with towering stone buildings casting long shadows, adding to the atmosphere of secrecy and stealth.",
                        },
                       {"input": "In the context of story: In a bustling port city where the air was thick with the mingling scents of salt and spice, Kiran stood mesmerized by a shimmering compass that once belonged to his father. This was no ordinary navigational tool; it was said to guide not just the traveler\u2019s route, but the very desires of the heart. With dreams as wide as the ocean and a spirit that yearned for adventure, Kiran resolved to embark on a journey along the Silk Road\u2014a vibrant tapestry of cultures, colors, and untold stories waiting to be uncovered.\n\nAs he ventured into arid deserts and scaled towering mountains, Kiran encountered a vivid array of traders, each with wares as diverse as their tales. The sweet aroma of saffron mingled with the fiery scent of chili peppers, carrying stories that ignited Kiran\u2019s insatiable curiosity. Beneath the vast canvas of starlit skies, he shared meals with nomads, absorbing their wisdom as if it were the very water he craved. Their laughter and shared tales filled his heart, teaching him the profound value of connection and the beauty of communal experiences.\n\nYet, the journey was fraught with peril. Shadows cloaked the bandits who lurked nearby, their eyes glinting with greed, while the treacherous terrain tested Kiran\u2019s resolve. Each challenge he faced forged his character, sharpening his instincts and deepening his understanding of the world around him.\n\nOne fateful evening, Kiran arrived at a vibrant bazaar alive with the scent of incense and the sounds of jubilant laughter. Amid the colorful stalls, he encountered an enigmatic old woman whose eyes sparkled like the night sky. She claimed to read the stories written in the heavens and spoke of a great truth hidden within his journey. With a voice that felt both ancient and wise, she implored him to look beyond the allure of gold and silver, urging him to seek the richness found in the connections he formed with others.\n\nAs Kiran pressed on, his path led him to a village ravaged by war, where despair hung heavy in the air. The stark contrast to the bustling markets he had visited shook him to his core. Moved by the suffering he witnessed, Kiran drew upon his resources to bring aid, sharing food and supplies with those in need. In that moment, enlightenment dawned upon him: true wealth was not measured in coin but in compassion and unity.\n\nWith each mile he traveled, the compass transformed from a mere navigational tool into a powerful symbol of his evolving perspective. By the time Kiran returned home, he was no longer just the ambitious son of a renowned merchant. He had become a bridge between cultures, a storyteller whose experiences were woven into the very fabric of his existence. The compass now pointed true not only to the East but also to the heart of humanity, forever altering his worldview and the legacy he would carry forward\u2014a legacy of understanding, connection, and shared humanity that would resonate through the ages. create a prompt for Yet, the journey was fraught with peril",
                        "output": "Wide ultra realistic photo shot of a vast, barren desert stretching endlessly into the horizon, with jagged mountains rising in the distance. In the foreground, a lone figure trudges through the shifting sands, his form slightly hunched against the harsh wind, the fabric of his cloak billowing. Shadows loom from the rocky outcrops, hinting at hidden dangers, while the sun casts a golden yet unforgiving light over the treacherous terrain. Above, vultures circle ominously in the clear, blue sky. The atmosphere is tense, with the sense of peril lurking just beyond view, as the traveler braces for the unknown",
                        },
                       {"input": "In the context of story: In a city once alive with alchemical marvels, a shadow lingered over the name Thoren, whispered among the populace like a dark omen. Once celebrated as a prodigy, Thoren had become a pariah, forever haunted by the specters of his past\u2014a catastrophic experiment that had claimed lives, including those of his dearest friends. The weight of his shame pressed heavily upon him, gnawing at his spirit like a relentless beast. Desperation surged within him, igniting a fierce determination to restore his tarnished legacy. Whispers of the fabled Philosopher's Stone\u2014a legendary artifact said to grant immense power\u2014pierced through his despair, sparking a glimmer of hope. It was rumored to be hidden within the towering fortress of Eldrin, an enigmatic wizard whose mastery of magic was both revered and feared.\n\nDriven by a singular purpose, Thoren set out to forge a team capable of breaching the ancient stronghold. His first ally was Mira, a nimble thief known for her cunning and unmatched agility in the city's underbelly. With raven-black hair framing her sharp features and eyes that sparkled with mischief, she embodied the stealth and cleverness he needed. Next came Jarek, a former knight whose unwavering loyalty and strength offered a bulwark against the dangers ahead. His imposing frame and the glint of his sword instilled a sense of security that Thoren found comforting. Lastly, they welcomed Lira, a spirited young sorceress whose flair for illusions could deceive even the most vigilant of guards. Her laughter echoed like a bright melody, infusing their grim mission with a sense of joy, while her wild auburn hair danced like flames in the wind.\n\nUnder the cover of night, they approached Eldrin's tower, its silhouette a foreboding monolith against the moonlit sky. The air shimmered with tension as they crossed the threshold, and a cascade of magical wards flared to life, casting an eerie glow over the dim corridors. Mira took the lead, her instincts sharp as she navigated them past perilous traps and concealed pitfalls. As Thoren whispered ancient incantations, he deftly dispelled minor enchantments that sought to ensnare them in their web of magic.\n\nDeeper into the tower they ventured, the atmosphere thickening with potent enchantments, the walls pulsating as if alive. Their first trial manifested in the form of a colossal stone golem, its eyes aflame with an otherworldly fire, a formidable guardian of Eldrin's secrets. Jarek stepped forward, sword gleaming ominously as he braced for battle. But Lira, ever quick-witted, raised her hands, weaving a complex illusion that conjured a phantom enemy behind the golem. For a heartbeat, confusion crossed the creature's stony face as it turned, allowing them to slip past unharmed, their hearts racing with the thrill of their narrow escape.\n\nThey ascended further, each chamber revealing mesmerizing illusions of the Philosopher's Stone, each more convincing than the last. Thoren's pulse quickened as he recognized the trap laid before them. With Lira's guidance, he focused his mind, calling upon the principles of alchemy that had once defined his greatness, discerning reality from illusion.\n\nAt last, they reached the inner sanctum, where Eldrin awaited, surrounded by swirling energies and arcane symbols. The air crackled with power as the wizard's piercing gaze landed on Thoren, a blend of disdain and curiosity flickering in his eyes. The confrontation unfolded like a deadly dance, their words cutting sharper than the finest blade, revealing the depths of Thoren's desperation and Eldrin's unyielding pride.\n\nAs tension reached its zenith, Mira seized the moment. She dashed toward the pedestal that held the real stone, but Eldrin's magic surged forth, unleashing a tempest of energy that threatened to engulf them. In that critical instant, Thoren\u2019s heart raced; he understood that brute strength would not win this day. Drawing upon his alchemical knowledge, he combined elements from the room to create a stunning flash of light that shattered Eldrin's concentration, granting them the diversion they desperately needed.\n\nLira conjured an illusion of a fearsome beast, a terrifying creature of fangs and claws that roared to life, distracting Eldrin long enough for Mira to claim the stone. With Jarek standing resolutely in front, sword drawn, he blocked the wizard's path, allowing the others to escape as the tower trembled under Eldrin's wrath.\n\nAs dawn broke, painting the horizon in hues of gold and crimson, they emerged from the forest, the Philosopher's Stone clutched tightly in their hands. Thoren's heart swelled with a mix of pride and redemption; they had faced down illusions and guardians, proving that friendship and courage could forge a new path. The city awaited, and with the stone, Thoren would not only reclaim his name but also ignite a renaissance of alchemical wonder. In the end, it was not merely the stone that mattered, but the bonds they had forged in the crucible of adversity. Together, they had rewritten the narrative of their lives, one filled with hope, bravery, and the promise of a brighter future. create a prompt for Driven by a singular purpose, Thoren set out to forge a team capable of breaching the ancient stronghold",
                        "output": "Hyper realistic photo of a determined figure standing at the edge of a darkened alley, his silhouette cast against the faint glow of a distant city illuminated by the soft flicker of alchemical lanterns. His posture is firm, with an air of resolve as he looks ahead toward the towering fortress in the far distance, shrouded in mist and mystery. In the foreground, the bustling yet grim streets of the city are visible, filled with shadowy figures, a mix of merchants and thieves, as the atmosphere hums with tension. The towering stronghold looms in the background, its dark stone walls and spires reaching into the night sky, a place both feared and revered, symbolizing the daunting task ahead.",
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
                 "You are a visual storytelling expert with 30 years of experience in crafting cinematic imagery from written descriptions. For each sentence, focus on visualizing the scene: describe the perspective, highlight 3-4 key elements that stand out, and conclude with a brief background description. Avoid using character names, instead focus on physical details and atmosphere from the story. Maintain the theme and setting of the story (e.g., space, medieval times) to ensure the prompt aligns with its context. Provide only the prompt.",
                 ),
                prompt_few_shot_template,
                ("human",
                 f"In the context of story: {story} create a prompt for {sentence}"),
            ])

        result = prompt_generation | model | StrOutputParser()
        generated_prompt = result.invoke({"input": sentence})
        # Add the generated prompt to the sentence
        sentences[key]["prompt"] = generated_prompt

    return sentences

def split_story_into_sentences(story):
    # Split the story into sentences using '.'
    sentences = [sentence.strip()
                 for sentence in story.split(".") if sentence.strip()]

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
    story_data["sentences"]= split_story_into_sentences(story_data.get("story", {}))
    # Generate prompts for the sentences
    sentences_with_prompts = generate_prompts_for_sentences(
        story_data.get("sentences", {}), story_data.get("story", {})
    )

    # Update the story_data with the new prompts
    story_data["sentences"] = sentences_with_prompts

    # Save the updated JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"Updated JSON saved to {json_file}")
