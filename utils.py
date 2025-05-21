import os
import requests
from urllib.parse import urlparse
from pydub import AudioSegment
from html2image import Html2Image
from moviepy import ImageClip
import sys
import contextlib
import io
import sys
from quran_utils import Reciter
import pandas as pd
from IPython.display import HTML, display

# Check if the OS is macOS before adding Homebrew path
if sys.platform == 'darwin':  # 'darwin' is the platform name for macOS
    os.environ["PATH"] += os.pathsep + "/opt/homebrew/bin/"

@contextlib.contextmanager
def nostdout():
    save_stdout = sys.stdout
    sys.stdout = io.StringIO()
    yield
    sys.stdout = save_stdout
    

def download_file(url, directory='.', filename=None):
    """
    Downloads a file from a URL to a specified directory.
    
    Args:
        url (str): The URL of the file to download.
        directory (str): The directory to save the file to. Defaults to current directory.
        filename (str, optional): The name to save the file as. If None, extracts from URL.
    
    Returns:
        str: The path to the downloaded file, or None if download failed.
    """
    try:
        # Create the directory if it doesn't exist
        os.makedirs(directory, exist_ok=True)
        
        # Get the filename from the URL if not provided
        if not filename:
            filename = os.path.basename(urlparse(url).path)
            # If URL doesn't have a filename, use a default
            if not filename:
                filename = 'downloaded_file'
        
        # Full path to save the file
        filepath = os.path.join(directory, filename)
        
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        # Save the file
        with open(filepath, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    file.write(chunk)
        
        return filepath
    
    except requests.exceptions.RequestException as e:
        print(f"Error downloading file: {e}")
        return None
    except IOError as e:
        print(f"Error saving file: {e}")
        return None


def get_words_with_timestamps(surah_number, aya_start, aya_end, reciter=Reciter.MAHMOUD_KHALIL_AL_HUSARY):
    """
    Constructs an array of words and their start and end timestamps in an audio.
    
    Args:
        surah_number (int): The surah number.
        aya_start (int): The starting aya number.
        aya_end (int): The ending aya number.
    
    Returns:
        list: A list of dictionaries containing words and their timestamps.
    """
    import json
    
    # Load the Quran text data
    try:
        with open('data/quran/quran.json', 'r', encoding='utf-8') as f:
            quran_data = json.load(f)
    except Exception as e:
        print(f"Error loading Quran data: {e}")
        return []
    
    # Load the timestamp data
    try:
        with open(reciter.value, 'r', encoding='utf-8') as f:
            timestamp_data = json.load(f)
    except Exception as e:
        print(f"Error loading timestamp data: {e}")
        return []
    # load translation data
    try:
        with open("data/quran/English wbw translation.json", "r", encoding="utf-8") as f:
            translation_data = json.load(f)
    except Exception as e:
        print(f"Error loading translation data: {e}")
        return []
            
    result = []
    audio_urls = []
    
    # Convert surah_number to string for quran_data lookup
    surah_str = str(surah_number)
    offset = 0
    
    # Process each aya in the range
    for aya_number in range(aya_start, aya_end + 1):
        # Get the aya text
        try:
            aya_text = quran_data[surah_str][str(aya_number)]["displayText"]
            # Split the aya text into words
            words = aya_text.split()
        except KeyError:
            print(f"Aya {surah_number}:{aya_number} not found in Quran data")
            continue
        
        # Get the timestamps for this aya
        timestamp_key = f"{surah_number}:{aya_number}"
        
        try:
            segments = timestamp_data[timestamp_key]["segments"]
        except KeyError:
            print(f"Timestamps for {timestamp_key} not found")
            continue
        
        # Match words with their timestamps
        for i, segment in enumerate(segments):
            if i >= len(words):
                break
            word_key= f"{surah_number}:{aya_number}:{segment[0]}"
            word_index = segment[0]-1
            word_info = {
                "word": words[word_index],
                "surah": surah_number,
                "aya": aya_number,
                "word_position": segment[0],
                "start": segment[1] + offset,
                "end": segment[2] + offset,
                "translation": {"en":translation_data[word_key]}
            }
            result.append(word_info)
        audio_urls.append(timestamp_data[timestamp_key]["audio_url"])
        duration = timestamp_data[timestamp_key]["duration"]
        offset += duration if duration is not None else result[-1]["end"]
    
    # Download the audio files
    audio_files = get_audio_file_paths(audio_urls)
    
    #join the audio files
    audio_files.sort()
    audio_files = [f for f in audio_files]
    audio_files = ' '.join(audio_files)
    output_file = os.path.join('temp/audio', 'combined_audio.mp3')
  
    # Create an empty audio segment
    combined = AudioSegment.empty()
    
    # Add each audio file to the combined segment
    for audio_file in audio_files.split():
        sound = AudioSegment.from_mp3(audio_file)
        combined += sound
    
    # Export the combined audio
    out = combined.export(output_file, format="mp3")
    out.close()
    #TODO: delete the audio files
        
    
    return result
def get_audio_file_paths(urls):
    """
    Downloads audio files from a list of URLs and returns their paths.
    
    Args:
        urls (list): A list of URLs to download audio files from.
    
    Returns:
        list: A list of paths to the downloaded audio files.
    """
    audio_files = []
    for url in urls:
        # Extract the second to last segment from the URL path
        url_parts = url.split('/')
        directory_path = url_parts[-2] if len(url_parts) >= 2 else os.path.basename(url)
        directory_path = os.path.join('temp/audio', directory_path)
        file_name = url_parts[-1]
        file_path = os.path.join(directory_path, file_name)
        # Check if the file already exists before downloading
        if not os.path.exists(file_path):
            os.makedirs(directory_path, exist_ok=True)
            audio_files.append(download_file(url, directory_path))
        else:
            audio_files.append(file_path)
    return audio_files


def create_text_image(word,start,end, width, height, font_path, font_size, translation="",text_color=(255,255,255)):
    hti = Html2Image(size=(width, height), output_path="temp",disable_logging=True)
    hti.browser.use_new_headless = None
    html = f"""<div><p class="text">{word}</p><p class="translation">{translation}</p></div>"""
    css = f"""
    @font-face {{ 
        font-family: text;
        src: url({font_path});
    }}

    .text {{
        font-family: text;
        font-size: {font_size}px;
        color: RGB{text_color};
        margin:0;
    }}
    .translation {{

        font-size: {font_size*0.3}px;
        color: RGB{text_color};
        margin:1px;
    }}
    div {{
        display: flex;
        justify-content: center;
        align-items: center;
        height: {height}px;
        width: {width}px;
        flex-direction: column;
    }}
    """
    with nostdout():
        hti.screenshot(html_str=html, css_str=css, save_as='text.png',size=[(width, height)])
    
    
    img = ImageClip('temp/text.png', transparent=True)
    img.duration = end - start
    img.start = start
    img.end = end
    img = img.resized((width, height))
    return img

def display_words_table(words):
    """
    Create and display an HTML table of words with their timing information.
    
    Args:
        words (list): List of word dictionaries containing timing and translation data
    
    Returns:
        None: Displays the HTML table
    """
    # Create a DataFrame from the words list
    word_data = []
    for word in words:
        word_data.append({
            'Word': word['word'],
            'Translation': word['translation']['en'] if 'translation' in word and 'en' in word['translation'] else '',
            'Start Time (s)': word['start'],
            'End Time (s)': word['end'],
            'Duration (s)': round(word['end'] - word['start'], 2),
            "Aya": f"{word['aya']}",
            "Word Position": f"{word['word_position']}"
        })

    # Create a DataFrame and display it as an HTML table
    word_df = pd.DataFrame(word_data)
    display(HTML(word_df.to_html(index=False)))

