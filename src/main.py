"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, score_song


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

    header = f"Top {len(recommendations)} recommendations for a "
    header += f"{user_prefs['mood']} / {user_prefs['genre']} listener"
    print()
    print(header)
    print("=" * len(header))

    for rank, (song, score, _explanation) in enumerate(recommendations, start=1):
        # Pull the specific reason phrases straight from the scoring function.
        _score, reasons = score_song(user_prefs, song)

        print(f"\n{rank}. {song['title']} - {song['artist']}")
        print(f"   Match score: {score:.2f}  ({score * 100:.0f}%)")
        print("   Why this song:")
        for reason in reasons:
            print(f"     - it {reason}")

    print()


if __name__ == "__main__":
    main()
