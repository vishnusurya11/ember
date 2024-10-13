# chat_model.py

from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain.schema.runnable import RunnableBranch


def generate_short_script(input_dict):
    # Setup environment variables
    load_dotenv()

    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o-mini")

    # Create the few-shot prompt template
    example_prompt = ChatPromptTemplate.from_messages(
        [
            ("human", "{input}"),
            ("ai", "{output}"),
        ]
    )

    # Examples to use for few-shot learning
    country_examples = [
        {
            "input": "India",
            "output": """India, located in South Asia, is the 7th largest country by land area and the 2nd most populous nation, with over 1.4 billion people. It spans diverse zones, from the Himalayas in the north to tropical coasts in the south. India experiences a range of climates, from scorching summers to monsoon rains and snowy winters in the north. As the world’s largest democracy, India gained independence in 1947 and operates as a federal parliamentary republic. Known for its exports like textiles, IT services, and spices, India also imports crude oil, electronics, and machinery to fuel its growing economy. Fun fact: India is the birthplace of yoga, a practice over 5,000 years old and a gift to the world!""",
        },
        {
            "input": "USA",
            "output": """Located in North America, the United States is the 3rd largest country by both land area and population, with over 331 million people. It spans diverse zones, from the Arctic cold of Alaska to the tropical warmth of Florida. The U.S. experiences a wide range of climates, from arid deserts to humid subtropics. As a federal republic, the U.S. has a significant global influence, having gained independence in 1776. Known for its exports like technology, machinery, and vehicles, the U.S. imports crude oil, electronics, and pharmaceuticals. Fun fact: The U.S. is home to the world’s largest economy and some of the most iconic landmarks, like the Statue of Liberty and the Grand Canyon!""",
        },
        {
            "input": "Germany",
            "output": """Located in Central Europe, Germany is the largest economy in Europe and the 4th largest in the world, with a population of over 83 million people. It spans diverse zones, from the coastal plains in the north to the mountainous regions in the south. Germany experiences a temperate seasonal climate, with cold winters and warm summers. As a federal parliamentary republic, Germany plays a key role in European and global politics, having reunified in 1990. Known for its exports like automobiles, machinery, and chemical products, Germany also imports crude oil, electronics, and agricultural goods. Fun fact: Germany is famous for its rich cultural history, including Oktoberfest and over 1,500 varieties of sausages!""",
        },
    ]

    animal_examples = [
        {
            "input": "Lion",
            "output": """The lion, known as the king of the jungle, is found in sub-Saharan Africa and India’s Gir Forest. Lions live in prides and are carnivores, hunting large prey like zebras and buffalo. Male lions are famous for their majestic manes. Fun fact: A lion's roar can be heard up to 5 miles away, making it the loudest of any big cat!""",
        },
        {
            "input": "Elephant",
            "output": """Elephants, the largest land animals, are found in Africa and Asia. They live in various habitats like savannas and forests. Elephants are herbivores, eating up to 300 pounds of vegetation daily. Known for their intelligence and strong social bonds, they can recognize themselves in mirrors. Fun fact: Elephants sleep standing up and can mourn their dead!""",
        },
        {
            "input": "Dolphin",
            "output": """Dolphins are highly intelligent marine mammals found in oceans worldwide. They are carnivores, eating fish and squid, and are known for their playful behavior and acrobatic leaps. Dolphins live in social groups called pods. Fun fact: Dolphins sleep with one eye open and half their brain awake to stay alert!""",
        },
    ]

    bird_examples = [
        {
            "input": "Eagle",
            "output": """The eagle, a symbol of power and freedom, is found in various habitats across the globe, from mountains to coastal regions. Eagles are carnivores, primarily feeding on fish and small mammals. Known for their incredible eyesight, they can spot prey from miles away. Fun fact: The bald eagle, the national bird of the USA, can dive at speeds over 100 mph!""",
        },
        {
            "input": "Penguin",
            "output": """Penguins, the flightless birds, are primarily found in the Southern Hemisphere, with a large population in Antarctica. They are carnivores, feeding on fish, krill, and squid. Known for their unique waddling walk, penguins are also excellent swimmers, using their flippers to glide through water. Fun fact: Emperor penguins can dive over 1,800 feet deep, making them the deepest diving birds!""",
        },
        {
            "input": "Parrot",
            "output": """Parrots are vibrant and intelligent birds found in tropical and subtropical regions around the world, particularly in South America and Australia. They are omnivores, eating seeds, nuts, fruits, and occasionally insects. Known for their ability to mimic human speech, parrots are social and highly trainable. Fun fact: The African grey parrot is one of the most skilled talking birds, able to learn hundreds of words and phrases!""",
        },
    ]

    dinosaur_examples = [
        {
            "input": "Tyrannosaurus Rex",
            "output": """Tyrannosaurus Rex, or T-Rex, is one of the most famous dinosaurs, known for its massive size and fearsome appearance. It lived in North America around 68 to 66 million years ago. T-Rex was a carnivore, hunting large herbivorous dinosaurs. Fun fact: Despite its terrifying reputation, recent studies suggest that T-Rex might have had feathers in its youth!""",
        },
        {
            "input": "Triceratops",
            "output": """Triceratops, with its three distinct horns and large bony frill, is one of the most recognizable dinosaurs. It lived in North America around 68 million years ago. Triceratops was an herbivore, feeding on low-lying plants. Fun fact: Triceratops' frill was likely used for display during mating rituals and possibly as a defense mechanism!""",
        },
        {
            "input": "Velociraptor",
            "output": """Velociraptor, made famous by the Jurassic Park movies, was a small but agile predator. It lived in what is now Mongolia about 75 to 71 million years ago. Velociraptors were carnivores, hunting in packs to take down larger prey. Fun fact: Real Velociraptors were only about the size of a turkey, much smaller than their Hollywood portrayal!""",
        },
    ]

    space_object_examples = [
        {
            "input": "Mars",
            "output": """Mars, known as the Red Planet, is the fourth planet from the Sun in our solar system. It has a thin atmosphere composed mostly of carbon dioxide and is known for its red, dusty surface. Mars is a terrestrial planet with polar ice caps and the largest volcano in the solar system, Olympus Mons. Fun fact: Mars has seasons similar to Earth, but they last twice as long!""",
        },
        {
            "input": "Halley's Comet",
            "output": """Halley's Comet is the most famous comet, visible from Earth every 75-76 years. It has a highly elliptical orbit that takes it far beyond Neptune before swinging back toward the Sun. The comet is composed of ice, dust, and gas, creating a bright coma and tail when it approaches the Sun. Fun fact: Halley's Comet was last seen in 1986 and will return in 2061!""",
        },
        {
            "input": "Andromeda Galaxy",
            "output": """The Andromeda Galaxy is the closest spiral galaxy to the Milky Way, located about 2.5 million light-years from Earth. It is the largest galaxy in our local group, containing around one trillion stars. Andromeda is on a collision course with the Milky Way, expected to merge in about 4.5 billion years. Fun fact: Andromeda is visible to the naked eye from Earth in the Northern Hemisphere!""",
        },
    ]

    water_beings_examples = [
        {
            "input": "Great White Shark",
            "output": """The great white shark is one of the most feared predators in the ocean, found in coastal waters around the world. They are carnivores, primarily feeding on fish, seals, and other marine mammals. Great whites are known for their powerful jaws and sharp teeth. Fun fact: Great white sharks can detect a drop of blood in 25 gallons of water and can sense tiny electrical signals from living creatures!""",
        },
        {
            "input": "Blue Whale",
            "output": """The blue whale is the largest animal ever known to have existed, found in oceans worldwide. Despite their massive size, they feed primarily on tiny krill, consuming up to 4 tons of them daily. Blue whales communicate through low-frequency calls that can be heard for hundreds of miles. Fun fact: A blue whale’s heart is as large as a small car and can weigh up to 1,300 pounds!""",
        },
        {
            "input": "Jellyfish",
            "output": """Jellyfish are ancient marine creatures found in oceans all over the world. They are carnivores, feeding on small fish and plankton using their stinging tentacles. Jellyfish are known for their gelatinous bodies and lack of brains or bones. Fun fact: Some jellyfish are bioluminescent, meaning they can produce their own light in the dark depths of the ocean!""",
        },
    ]

    plant_examples = [
        {
            "input": "Rose",
            "output": """The rose, often called the queen of flowers, is known for its beauty and fragrance. Roses are found worldwide and are cultivated in a variety of colors and sizes. They thrive in well-drained soil with plenty of sunlight. Roses are not only symbols of love but also have culinary uses in teas and jams. Fun fact: The rose is the national flower of the United States, the United Kingdom, and several other countries!""",
        },
        {
            "input": "Bamboo",
            "output": """Bamboo is a fast-growing grass that can be found in Asia, Africa, and the Americas. Known for its strength and flexibility, bamboo is used in construction, furniture, and even clothing. It grows incredibly fast, with some species shooting up over 3 feet in a single day. Fun fact: Bamboo is a crucial food source for pandas, making up 99% of their diet!""",
        },
        {
            "input": "Sunflower",
            "output": """Sunflowers are tall, bright flowers native to North America, known for their large, sun-tracking blooms. They thrive in full sun and well-drained soil, often growing over 10 feet tall. Sunflowers are not just beautiful; their seeds are harvested for oil and snacks. Fun fact: A sunflower's head can contain up to 2,000 seeds, and the plant can follow the sun across the sky, a behavior called heliotropism!""",
        },
    ]

    country_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=country_examples,
    )

    animal_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=animal_examples,
    )

    bird_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=bird_examples,
    )

    plant_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=plant_examples,
    )

    water_beings__few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=water_beings_examples,
    )

    space_object_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=space_object_examples,
    )

    dinosaur_few_shot_prompt = FewShotChatMessagePromptTemplate(
        example_prompt=example_prompt,
        examples=dinosaur_examples,
    )

    # Create the final prompt template
    country_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            country_few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    animal_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            animal_few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    bird_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            bird_few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    plant_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            plant_few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    water_beings_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            water_beings__few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    space_object_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            space_object_few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    dinosaur_final_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                "you are a youtube content writer who writes scripts for shorts that are under 60 seconds",
            ),
            dinosaur_few_shot_prompt,
            ("human", f"Tell me about {input_dict['topic']}?"),
        ]
    )

    # Define the runnable branches for handling feedback
    branches = RunnableBranch(
        (
            lambda x: "countries" in input_dict["type"],
            country_final_prompt | model | StrOutputParser(),  # Positive feedback chain
        ),
        (
            lambda x: "animals" in input_dict["type"],
            animal_final_prompt | model | StrOutputParser(),  # Positive feedback chain
        ),
        (
            lambda x: "birds" in input_dict["type"],
            bird_final_prompt | model | StrOutputParser(),  # Positive feedback chain
        ),
        (
            lambda x: "plants" in input_dict["type"],
            plant_final_prompt | model | StrOutputParser(),  # Positive feedback chain
        ),
        (
            lambda x: "water_beings" in input_dict["type"],
            water_beings_final_prompt
            | model
            | StrOutputParser(),  # Positive feedback chain
        ),
        (
            lambda x: "space_objects" in input_dict["type"],
            space_object_final_prompt
            | model
            | StrOutputParser(),  # Positive feedback chain
        ),
        dinosaur_final_prompt | model | StrOutputParser(),
    )

    # Create the classification chain
    # classification_chain = classification_template | model | StrOutputParser()
    # Combine classification and response generation into one chain
    chain = branches | StrOutputParser()
    # Generate the YouTube short script
    # chain = country_final_prompt | model
    result = chain.invoke({"input_dict": input_dict})
    return result


# Optional: Print environment variables (for debugging)


def print_env_variables():
    load_dotenv()  # Ensure the environment variables are loaded
    for key, value in os.environ.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    # Example usage
    input_dict = {"topic": "Kenya", "type": "countries"}
    script = generate_short_script(input_dict)
    print(script)

    # Uncomment the following line if you want to print environment variables for debugging
    # print_env_variables()


#########
# TODO :
# - Update the examples for specific use cases
# - Update system prompt for better outcomes
