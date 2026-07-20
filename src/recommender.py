import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

# Fields that must be parsed from CSV strings into numbers.
INT_FIELDS = ("id",)
FLOAT_FIELDS = ("energy", "tempo_bpm", "valence", "danceability", "acousticness")

# How much each numeric feature contributes to the match score.
# Weights sum to 1.0, so the weighted-sum score lands in [0, 1] ("percent match").
WEIGHTS = {
    "acousticness": 0.25,  # most disqualifying if wrong for this persona
    "energy": 0.25,        # must stay calm / low-arousal
    "tempo_bpm": 0.20,     # pace = intensity (trimmed; correlates with energy)
    "valence": 0.15,       # persona is tolerant on mood-positivity
    "danceability": 0.15,  # least relevant for background listening
}

# Small extra credit when the song's mood matches the user's (categorical,
# so it can't use the 1 - |a - b| closeness formula).
MOOD_BONUS = 0.10

# tempo_bpm is not on a 0-1 scale, so it must be normalized before it can be
# compared against the other features. Songs in the catalog run ~58-158 BPM.
TEMPO_MIN_BPM = 60.0
TEMPO_MAX_BPM = 200.0


def normalize_tempo(bpm: float) -> float:
    """Rescale a BPM value to 0-1, clamped, so it's comparable to other features."""
    scaled = (bpm - TEMPO_MIN_BPM) / (TEMPO_MAX_BPM - TEMPO_MIN_BPM)
    return max(0.0, min(1.0, scaled))

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
    # The remaining numeric targets default to neutral (0.5) / mid-tempo so a
    # profile can still be built with only the core fields (favorite_genre,
    # favorite_mood, target_energy) as the tests do.
    target_valence: float = 0.5
    target_tempo_bpm: float = 100.0
    target_danceability: float = 0.5
    target_acousticness: float = 0.5  # numeric target used by score_song
    likes_acoustic: bool = True       # friendly flag; folded into acousticness target below

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
        """Store the catalog of Song objects this recommender ranks over."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k Song objects for a user, highest score first."""
        # Score each Song (adapted to a dict) against the profile and return
        # the top-k Song objects, highest score first.
        prefs = user.to_prefs()
        scored = [(song, score_song(prefs, asdict(song))[0]) for song in self.songs]
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [song for song, _score in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a one-sentence explanation of why a song fits the user."""
        # Reuse the functional scorer: adapt the profile to prefs keys and the
        # Song dataclass to a dict, then turn its reasons into a sentence.
        _, reasons = score_song(user.to_prefs(), asdict(song))
        return build_explanation(song.title, reasons)

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

    print(f"Loaded {len(songs)} songs from {csv_path}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Score a single song against user preferences (content-based matching).

    For each weighted numeric feature we measure closeness = 1 - |user - song|
    (1.0 = perfect match, 0.0 = opposite), multiply by the feature's weight,
    and sum. A mood match adds a small bonus. The final score is in [0, 1].

    Returns (score, reasons) where reasons explains, in plain language, which
    preferences the song satisfied.
    """
    score = 0.0
    reasons: List[str] = []

    for feature, weight in WEIGHTS.items():
        user_value = user_prefs.get(feature)
        song_value = song.get(feature)
        if user_value is None or song_value is None:
            continue  # can't compare a feature the profile or song doesn't have

        # Put both values on the same 0-1 scale before comparing.
        if feature == "tempo_bpm":
            user_value = normalize_tempo(user_value)
            song_value = normalize_tempo(song_value)

        closeness = 1.0 - abs(user_value - song_value)
        score += weight * closeness

        # Call out features the song matched well as human-readable reasons.
        if closeness >= 0.85:
            reasons.append(f"closely matches your {feature} preference")
        elif closeness >= 0.70:
            reasons.append(f"is a good fit for your {feature} preference")

    # Categorical mood match: a bonus, not a closeness calculation.
    user_mood = user_prefs.get("mood")
    if user_mood is not None and song.get("mood") == user_mood:
        score += MOOD_BONUS
        reasons.append(f"has the mood you like ({user_mood})")

    # The mood bonus can push the total above 1.0; keep the score in [0, 1].
    score = min(1.0, score)

    if not reasons:
        reasons.append("is a general match for your profile")

    return score, reasons

def build_explanation(title: str, reasons: List[str]) -> str:
    """Turn a list of reason phrases into one readable sentence."""
    if not reasons:
        return f"'{title}' is a general match for your profile."
    if len(reasons) == 1:
        joined = reasons[0]
    else:
        joined = ", ".join(reasons[:-1]) + f", and {reasons[-1]}"
    return f"'{title}' {joined}."


# How strongly the ranking stage penalizes a candidate for resembling songs
# already chosen. 0 = ignore variety (pure score); higher = push harder for
# a diverse list, at the cost of demoting some closer matches.
VARIETY_PENALTY = 0.30


def _song_similarity(a: Dict, b: Dict) -> float:
    """
    How alike two songs are, in [0, 1]. Averages per-feature closeness over the
    weighted features (tempo normalized), then adds a bump for a shared artist.
    Used only by the variety re-rank, never by score_song.
    """
    closes = []
    for feature in WEIGHTS:
        av, bv = a.get(feature), b.get(feature)
        if av is None or bv is None:
            continue
        if feature == "tempo_bpm":
            av, bv = normalize_tempo(av), normalize_tempo(bv)
        closes.append(1.0 - abs(av - bv))
    similarity = sum(closes) / len(closes) if closes else 0.0
    if a.get("artist") and a.get("artist") == b.get("artist"):
        similarity = min(1.0, similarity + 0.15)  # same artist = extra similar
    return similarity


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Rank songs for a user and return the top-k as (song, score, explanation).

    Two stages, kept separate on purpose:
      1. SCORING  - score every song in isolation via score_song.
      2. RANKING  - greedily build the list, each time picking the highest
                    score MINUS a penalty for resembling already-picked songs.
                    Variety is enforced here, not by dropping features in
                    scoring, so match accuracy stays intact.
    """
    # Stage 1: score every song.
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, reasons))

    # Stage 2: greedy variety-aware selection.
    selected: List[Tuple[Dict, float, str]] = []
    remaining = list(scored)
    while remaining and len(selected) < k:
        best_idx, best_adjusted = 0, None
        for i, (song, score, _reasons) in enumerate(remaining):
            # Penalize by the most-similar song already chosen.
            penalty = 0.0
            if selected:
                penalty = VARIETY_PENALTY * max(
                    _song_similarity(song, chosen) for chosen, _s, _r in selected
                )
            adjusted = score - penalty
            if best_adjusted is None or adjusted > best_adjusted:
                best_idx, best_adjusted = i, adjusted

        song, score, reasons = remaining.pop(best_idx)
        selected.append((song, score, build_explanation(song["title"], reasons)))

    return selected
