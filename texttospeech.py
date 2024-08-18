from gtts import gTTS
import os

def text_to_speech(text, lang='en', filename='output.mp3'):
    """
    Converts the given text to speech and saves it as an audio file.
    
    Parameters:
        text (str): The text to convert to speech.
        lang (str): The language in which the text should be spoken (default is English).
        filename (str): The name of the output audio file (default is 'output.mp3').
    """
    # Create a gTTS object
    tts = gTTS(text=text, lang=lang, slow=False)
    
    # Save the audio file
    tts.save(filename)
    print(f"Saved audio to {filename}")

if __name__ == "__main__":
    # Example usage
    text = """India, located in South Asia, is the 7th largest country by land area and the 2nd most populous nation, with over 1.4 billion people. 
    It spans diverse zones, from the Himalayas in the north to tropical coasts in the south. 
    India experiences a range of climates, from scorching summers to monsoon rains and snowy winters in the north. 
    As the world’s largest democracy, India gained independence in 1947 and operates as a federal parliamentary republic. 
    Known for its exports like textiles, IT services, and spices, India also imports crude oil, electronics, and machinery to fuel its growing economy. 
    Fun fact: India is the birthplace of yoga, a practice over 5,000 years old and a gift to the world!"""
    
    text="""Located in North America, the United States is the 3rd largest country by both land area and population, with over 331 million people. It spans diverse zones, from the Arctic cold of Alaska to the tropical warmth of Florida. The U.S. experiences a wide range of climates, from arid deserts to humid subtropics. As a federal republic, the U.S. has a significant global influence, having gained independence in 1776. Known for its exports like technology, machinery, and vehicles, the U.S. imports crude oil, electronics, and pharmaceuticals. Fun fact: The U.S. is home to the world’s largest economy and some of the most iconic landmarks, like the Statue of Liberty and the Grand Canyon!"""
    text="""Located in Central Europe, Germany is the largest economy in Europe and the 4th largest in the world, with a population of over 83 million people. It spans diverse zones, from the coastal plains in the north to the mountainous regions in the south. Germany experiences a temperate seasonal climate, with cold winters and warm summers. As a federal parliamentary republic, Germany plays a key role in European and global politics, having reunified in 1990. Known for its exports like automobiles, machinery, and chemical products, Germany also imports crude oil, electronics, and agricultural goods. Fun fact: Germany is famous for its rich cultural history, including Oktoberfest and over 1,500 varieties of sausages!"""
    text_to_speech(text)
