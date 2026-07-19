"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # "Late-Night Focus Listener" taste profile.
    # One target per feature that score_song weighs. tempo_bpm is raw BPM
    # (normalized inside scoring); the other numeric targets are on a 0-1 scale.
    user_prefs = {
        "genre": "lofi",          # for display/explanations; not weighted
        "mood": "focused",        # categorical match bonus
        "energy": 0.40,           # low-medium, not hyped up
        "valence": 0.55,          # neutral-calm
        "tempo_bpm": 82,          # slow-ish
        "danceability": 0.55,     # background, not a dance track
        "acousticness": 0.80,     # prefers acoustic/organic sound
        "likes_acoustic": True,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
