# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.
In the real world, content platforms like Youtube and Spotify use a mixture of content-based filtering (which is what this recommendation project is using) and collabrative filitering (which ignores content and instead relies on pattern recognition for a large user base, for example: users who clicked on this video also enjoyed the following video - so the following video is recommended). So they take into account the users preference (what they watch) and show similar videos and also occasionally show content based on other users interests that the user might enjoy.

  -  My simulator is a content-based recommender. The scoring rule measures, feature by feature, how close each song's numeric attributes (energy, valence, danceability, acousticness, normalized tempo) are to the user's preferences, combined as a weighted sum where the weights encode how much each feature matters — producing one match score in [0,1] plus human-readable reasons. The ranking rule then sorts all scored songs and applies a variety penalty so the final top-K isn't five near-identical tracks. Variety is enforced at ranking, not by discarding features, so I keep full matching accuracy and a diverse list.
        ┌──────────────────┐        ┌──────────────────────┐
        │  Song catalog    │        │   User taste profile │
        │  (load_songs)    │        │   (UserProfile)      │
        │ energy, valence, │        │ target energy,       │
        │ tempo, dance...  │        │ mood, likes_acoustic │
        └────────┬─────────┘        └──────────┬───────────┘
                 │                             │
                 └──────────────┬──────────────┘
                                │
                                ▼
        ╔═══════════════════════════════════════════════╗
        ║   SCORING RULE   ·   score_song(user, song)    ║
        ║   "How well does THIS ONE song match?"         ║
        ╠═══════════════════════════════════════════════╣
        ║  1. Normalize features → all on 0–1 scale      ║
        ║       (tempo_bpm rescaled!)                    ║
        ║  2. Per-feature closeness = 1 - |user - song|  ║
        ║  3. Weighted sum  Σ (weight × closeness)       ║
        ║       energy .30  valence .25  dance .20 ...   ║
        ║       (weights sum to 1)                       ║
        ╚═══════════════════════════════════════════════╝
                                │
                                ▼
              one score in [0,1]  +  reasons
              (repeat for every song)
                                │
                                ▼
        ╔═══════════════════════════════════════════════╗
        ║   RANKING RULE   ·   recommend_songs(...)      ║
        ║   "What LIST do I actually show?"              ║
        ╠═══════════════════════════════════════════════╣
        ║  1. Sort all songs by score (descending)       ║
        ║  2. Variety re-rank: penalize a candidate      ║
        ║     too similar to ones already picked         ║
        ║       ← variety lives HERE, not by dropping    ║
        ║         features in scoring                    ║
        ╚═══════════════════════════════════════════════╝
                                │
                                ▼
                    ┌───────────────────────┐
                    │   Top-K recommendations│
                    │   (song, score, why)   │
                    └───────────────────────┘

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
# e.g.:
# User profile: genre=indie, mood=chill, energy=low
# Recommendations:
#   1. ...
#   2. ...
#   3. ...
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



