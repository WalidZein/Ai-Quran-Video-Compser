import os
import random
import requests
from typing import Optional, Dict, List, Union
from dataclasses import dataclass
from urllib.parse import urlparse
import utils

@dataclass
class VideoQuality:
    HD = "small"
    FHD = "medium"
    UHD = "large"

@dataclass
class VideoOrientation:
    LANDSCAPE = "landscape"
    PORTRAIT = "portrait"
    SQUARE = "square"

class PexelsVideoAPI:
    def __init__(self, api_key: str):
        """
        Initialize the Pexels Video API client.
        
        Args:
            api_key (str): Your Pexels API key
        """
        self.api_key = api_key
        self.base_url = "https://api.pexels.com/videos"
        self.headers = {
            "Authorization": api_key
        }
    
    def search_videos(
        self,
        query: str,
        orientation: Optional[VideoOrientation] = None,
        size: Optional[VideoQuality] = None,
        locale: Optional[str] = None,
        page: int = 1,
        per_page: int = 15,
    ) -> Dict:
        """
        Search for videos on Pexels.
        
        Args:
            query (str): Search query
            orientation (str, optional): Video orientation (landscape, portrait, square)
            size (str, optional): Minimum video size (sd, hd, full_hd, uhd)
            color (str, optional): Desired video color
            locale (str, optional): The locale of the search
            page (int, optional): Page number (default: 1)
            per_page (int, optional): Results per page (default: 15, max: 80)
            
        Returns:
            Dict: API response containing video results
        """
        params = {
            "query": query,
            "page": page,
            "per_page": per_page
        }
        
        if orientation:
            params["orientation"] = orientation
        if size:
            params["size"] = size
        if locale:
            params["locale"] = locale
            
        response = requests.get(
            f"{self.base_url}/search",
            headers=self.headers,
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    def get_video(self, video_id: int) -> Dict:
        """
        Get details for a specific video.
        
        Args:
            video_id (int): The ID of the video to retrieve
            
        Returns:
            Dict: Video details
        """
        response = requests.get(
            f"{self.base_url}/videos/{video_id}",
            headers=self.headers
        )
        response.raise_for_status()
        return response.json()
    
    def download_video(self, video_id: int, quality: str = "hd", output_dir: str = "temp/video") -> Optional[str]:
        """
        Download a video from Pexels by its ID.
        
        Args:
            video_id (int): The ID of the video to download
            quality (str): Desired video quality (sd, hd, full_hd, uhd)
            output_dir (str): Directory to save the video
            
        Returns:
            Optional[str]: Path to the downloaded video file, or None if download failed
        """
        try:
            # Get video details
            video_data = self.get_video(video_id)
            
            # Find the video file with the requested quality
            video_files = video_data.get("video_files", [])
            target_file = None
            
            for file in video_files:
                if file.get("quality") == quality:
                    target_file = file
                    break
            
            if not target_file:
                # If requested quality not found, use the highest quality available
                video_files.sort(key=lambda x: x.get("width", 0) * x.get("height", 0), reverse=True)
                target_file = video_files[0]
            
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Generate output filename
            video_url = target_file["link"]
            file_extension = os.path.splitext(urlparse(video_url).path)[1]
            if not file_extension:
                file_extension = ".mp4"  # Default to mp4 if no extension found
            
            output_filename = f"pexels_video_{video_id}{file_extension}"
            output_path = os.path.join(output_dir, output_filename)
            
            utils.download_file(video_url, output_dir, output_filename)
            
            return output_path
            
        except Exception as e:
            print(f"Error downloading video: {e}")
            return None

def download_video_by_id(
    api_key: str,
    video_id: int,
    quality: str = "hd",
    output_dir: str = "temp/video"
) -> Optional[str]:
    """
    Download a video from Pexels by its ID.
    
    Args:
        api_key (str): Your Pexels API key
        video_id (int): The ID of the video to download
        quality (str): Desired video quality (sd, hd, full_hd, uhd)
        output_dir (str): Directory to save the video
        
    Returns:
        Optional[str]: Path to the downloaded video file, or None if download failed
    """
    api = PexelsVideoAPI(api_key)
    return api.download_video(video_id, quality, output_dir)

def select_video(
    api_key: str,
    query: str,
    orientation: Optional[VideoOrientation] = None,
    size: Optional[VideoQuality] = None,
    selection_method: str = "best",
    offset: Optional[int] = None,
    duration: Optional[int] = None
) -> Optional[int]:
    """
    Search for videos and select one based on specified criteria.
    
    Args:
        api_key (str): Your Pexels API key
        query (str): Search query
        orientation (str, optional): Video orientation (landscape, portrait, square)
        size (str, optional): Minimum video size (sd, hd, full_hd, uhd)
        selection_method (str): How to select the video:
            - "best": Select the first result (usually highest quality)
            - "random": Select a random video from results
            - "offset": Select video at specific offset
        offset (int, optional): Offset for selection (required if selection_method is "offset")
        duration (int, optional): Minimum duration of the video
    Returns:
        Optional[int]: Selected video ID or None if no results found
    """
    api = PexelsVideoAPI(api_key)
    
    # Search for videos
    results = api.search_videos(
        query=query,
        orientation=orientation,
        size=size,
    )
    
    if not results.get("videos"):
        return None
    
    videos = results["videos"]
    if duration is not None:
        videos = [video for video in videos if video.get("duration") >= duration]
    if len(videos) == 0:
        raise ValueError("No videos found matching the criteria")
    match selection_method:
        case "best":
            return videos[0]["id"]
        case "random":
            return random.choice(videos)["id"]
        case "offset":
            if offset is None:
                raise ValueError("Offset must be provided when selection_method is 'offset'")
            if offset >= len(videos):
                    return None
            return videos[offset]["id"]
        case _:
            raise ValueError("Invalid selection_method. Must be one of: best, random, offset")
    
def select_and_download_video(
    api_key: str,
    query: str,
    orientation: Optional[str] = None,
    size: Optional[str] = None,
    selection_method: str = "best",
    output_dir: str = "temp/video",
    duration: Optional[int] = None,
    offset: Optional[int] = None
) -> Optional[str]:
    video_id = select_video(
        api_key=api_key,
        query=query,
        orientation=orientation,
        size=size,
        selection_method=selection_method,
        duration=duration,
        offset=offset
        )
    return download_video_by_id(api_key, video_id, size, output_dir)
    
# Example usage:
if __name__ == "__main__":
    # Replace with your actual API key
    API_KEY = "" #TODO: Add your API key
    
    # Example: Get a random landscape HD video of nature
    video_id = select_video(
        api_key=API_KEY,
        query="nature",
        orientation=VideoOrientation.LANDSCAPE,
        size=VideoQuality.HD,
        selection_method="random"
    )
    
    if video_id:
        print(f"Selected video ID: {video_id}")
        # Download the video
        video_path = download_video_by_id(
            api_key=API_KEY,
            video_id=video_id,
            quality=VideoQuality.HD
        )
        if video_path:
            print(f"Video downloaded to: {video_path}")
        else:
            print("Failed to download video")
    else:
        print("No videos found matching the criteria") 