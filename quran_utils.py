from enum import Enum
from typing import Dict, Optional


class Reciter(Enum):
    """
    Enum mapping reciters to their data file paths.
    
    Each enum value contains the path to the JSON file with timestamp data
    for the corresponding reciter's Quran recitation.
    """
    MAHMOUD_KHALIL_AL_HUSARY = 'data/audio/ayah-recitation-mahmoud-khalil-al-husary-murattal-hafs-957_updated.json'
    MUHAMMAD_AL_MINSHAWI = 'data/audio/ayah-recitation-muhammad-siddiq-al-minshawi-murattal-hafs-959_updated.json'
    
