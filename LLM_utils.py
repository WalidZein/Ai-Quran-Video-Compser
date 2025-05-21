import os
from typing import List, Dict
import openai
from dataclasses import dataclass
import xml.etree.ElementTree as ET
import prompts

@dataclass
class VideoSuggestion:
    keywords: str
    start_time: float
    end_time: float

def make_openai_request(api_key: str, prompt: str, model: str = "gpt-4.1") -> str:
    """
    Make a request to OpenAI API with the given prompt.
    
    Args:
        prompt (str): The prompt to send to the LLM
        model (str): The OpenAI model to use (default: gpt-4)
    
    Returns:
        str: The LLM's response
    """
    try:
        client = openai.OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
            ],
            temperature=0.55
        )
        return response.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error making OpenAI request: {str(e)}")

def parse_video_suggestions(llm_output: str) -> List[VideoSuggestion]:
    """
    Parse the LLM's XML output into a list of VideoSuggestion objects.
    
    Args:
        llm_output (str): The XML-formatted output from the LLM
    
    Returns:
        List[VideoSuggestion]: List of parsed video suggestions
    """
    try:
        # Wrap the output in a root element to make it valid XML
        xml_string = f"<root>{llm_output}</root>"
        root = ET.fromstring(xml_string)
        
        suggestions = []
        for video_elem in root.findall(".//video"):
            suggestion = VideoSuggestion(
                keywords=video_elem.find("query").text,
                start_time=float(video_elem.find("start").text),
                end_time=float(video_elem.find("end").text)
            )
            suggestions.append(suggestion)
        
        return suggestions
    except Exception as e:
        raise Exception(f"Error parsing video suggestions: {str(e)}")

def get_video_suggestions(verse_words: List[Dict[str, any]], api_key: str) -> List[VideoSuggestion]:
    """
    Get video suggestions from the LLM based on verse words and their timings.
    
    Args:
        verse_words (List[Dict]): List of dictionaries containing verse words and their timings
        api_key (str): OpenAI API key
    
    Returns:
        List[VideoSuggestion]: List of video suggestions
    """
    
    # Construct the prompt
    prompt = prompts.Background_video_prompt.format(quran_verse_data=verse_words)
    
    # Get response from LLM
    llm_output = make_openai_request(api_key, prompt)

    # Parse the response
    return parse_video_suggestions(llm_output)

if __name__ == "__main__":
    # Example usage
    example_verse_words = [{'word': 'بِسْمِ', 'start': 0.0, 'end': 0.48, 'aya': 1},
 {'word': 'اللَّهِ', 'start': 0.48, 'end': 1.0, 'aya': 1},
 {'word': 'الرَّحْمَنِ', 'start': 1.0, 'end': 2.16, 'aya': 1},
 {'word': 'الرَّحِيمِ', 'start': 2.16, 'end': 5.16, 'aya': 1},
 {'word': 'الْحَمْدُ', 'start': 5.16, 'end': 6.4, 'aya': 2},
 {'word': 'لِلَّهِ', 'start': 6.4, 'end': 6.83, 'aya': 2},
 {'word': 'رَبِّ', 'start': 6.83, 'end': 7.79, 'aya': 2}]
    
   
    api_key = ''#TODO: Add API key
    if not api_key:
        print("Please set the openai api key")
        exit(1)
    
    try:
        suggestions = get_video_suggestions(example_verse_words, api_key)
        print("\nVideo Suggestions:")
        print("-----------------")
        for suggestion in suggestions:
            print(f"\nKeywords: {suggestion.keywords}")
            print(f"Start: {suggestion.start_time:.2f}s")
            print(f"End: {suggestion.end_time:.2f}s")
    except Exception as e:
        print(f"Error: {str(e)}")
