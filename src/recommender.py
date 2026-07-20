import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Fields that must be parsed from CSV strings into numbers.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py

    Numeric targets (one per weighted feature) let score_song compute
    per-feature closeness (1 - |user - song|). mood/genre are categorical;
    target_tempo_bpm is raw BPM (normalized inside scoring); the other
    numeric targets are on a 0-1 scale.
    """
    favorite_genre: str          # kept for display/explanations; NOT weighted (preserves variety)
    favorite_mood: str
    target_energy: float
    target_valence: float
    target_tempo_bpm: float
    target_danceability: float
    target_acousticness: float   # numeric target used by score_song
    likes_acoustic: bool = True  # friendly flag; score_song may fall back to this

    def to_prefs(self) -> Dict:
        """
        Adapt the profile into a user_prefs dict whose keys match the song
        dicts from load_songs (genre, mood, energy, tempo_bpm, ...), so a
        UserProfile can be fed to score_song exactly like the dict in main.py.
        """
        return {
            "genre": self.favorite_genre,
            "mood": self.favorite_mood,
            "energy": self.target_energy,
            "valence": self.target_valence,
            "tempo_bpm": self.target_tempo_bpm,
            "danceability": self.target_danceability,
            "acousticness": self.target_acousticness,
            "likes_acoustic": self.likes_acoustic,
        }

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file into a list of dictionaries.

    Numeric columns (id, energy, tempo_bpm, valence, danceability,
    acousticness) are converted from strings to int/float so score_song
    can do arithmetic on them; text columns are left as strings.
    Required by src/main.py
    """
    # Resolve relative paths against this file's project root, so the loader
    # works no matter which directory the program is launched from.
    if not os.path.isabs(csv_path):
        project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(project_root, csv_path)

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Skip fully blank rows (e.g. a trailing newline in the CSV).
            if row.get("title") is None or all(
                (v or "").strip() == "" for v in row.values()
            ):
                continue

            song: Dict = {}
            for key, value in row.items():
                value = (value or "").strip()
                if key in INT_FIELDS:
                    song[key] = int(value)
                elif key in FLOAT_FIELDS:
                    song[key] = float(value)
                else:
                    song[key] = value
            songs.append(song)

    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    # TODO: Implement scoring logic using your Algorithm Recipe from Phase 2.
    # Expected return format: (score, reasons)
    return []

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    return []
