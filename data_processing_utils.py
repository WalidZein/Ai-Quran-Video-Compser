def update_audio_durations(input_file_path, output_dir=None, max_workers=5):
    """
    Updates the duration field for each audio entry in the JSON file using multiple threads.
    
    Args:
        input_file_path (str): Path to the input JSON file
        output_file_path (str, optional): Path to save the updated JSON file. 
                                         If None, will use input_file_path with '_updated' suffix.
        max_workers (int): Maximum number of threads to use for processing
    
    Returns:
        str: Path to the updated JSON file
    """
    import json
    import requests
    from mutagen.mp3 import MP3
    import tempfile
    import os
    from concurrent.futures import ThreadPoolExecutor, as_completed
    import threading
    
    if output_dir is None:
        base_name, ext = os.path.splitext(input_file_path)
        output_file_path = f"{base_name}_updated{ext}"
    else:
        base_name = os.path.basename(input_file_path)
        name, ext = os.path.splitext(base_name)
        output_file_path = os.path.join(output_dir, f"{name}_updated{ext}")
    
    # Load the JSON data
    with open(input_file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # Thread-safe lock for updating data
    data_lock = threading.Lock()
    
    def process_audio_entry(key, entry):
        """Process a single audio entry to get its duration."""
        if entry["duration"] is None and "audio_url" in entry:
            audio_url = entry["audio_url"]
            try:
                # Create a temporary file to download the audio
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                # Download the audio file
                response = requests.get(audio_url, stream=True)
                response.raise_for_status()
                
                with open(temp_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                
                # Get the duration
                audio = MP3(temp_path)
                duration = audio.info.length
                
                # Thread-safe update of the JSON data
                with data_lock:
                    entry["duration"] = duration * 1000
                
                # Clean up
                os.unlink(temp_path)
                
                print(f"Updated duration for {key}: {duration} seconds")
                return key, True
            except Exception as e:
                print(f"Error processing {key}: {str(e)}")
                return key, False
        return key, None
    
    # Get entries that need processing
    entries_to_process = [(key, entry) for key, entry in data.items() 
                         if entry["duration"] is None and "audio_url" in entry]
    
    if not entries_to_process:
        print("No entries need duration updates")
        return input_file_path
    
    print(f"Processing {len(entries_to_process)} entries with {max_workers} threads...")
    
    # Process entries using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        # Submit all tasks
        future_to_key = {
            executor.submit(process_audio_entry, key, entry): key 
            for key, entry in entries_to_process
        }
        
        # Process completed tasks
        completed_count = 0
        for future in as_completed(future_to_key):
            key, result = future.result()
            completed_count += 1
            if result is True:
                print(f"Progress: {completed_count}/{len(entries_to_process)} completed")
    
    # Save the updated JSON data
    with open(output_file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    
    print(f"Updated JSON saved to {output_file_path}")
    return output_file_path