# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name   
**PathToMusic 1.0**

---

## 2. Intended Use  

My recommender is for people who want to look ofr similar song to the ones they already listen ton to. However they should expect the music to match the exact genre. Perhaps they'll be in for a surprise.

---

## 3. How the Model Works  

Think of the program as a matchmaker for songs. The listener describes the music they're in the mood for, and the program measures how closely each song fits — then returns the best matches with a reason for each.

What we look at in each song: measurable traits like energy (calm vs. hyped), tempo (fast vs. slow), valence (upbeat vs. moody), danceability, acousticness (unplugged vs. electronic), and a mood label like "chill" or "focused."

What the listener gives us: their ideal version of those same traits — how much energy, what tempo, what mood, and so on.

How we turn that into a score: for each trait we ask "how close is the song to what the listener wanted?" — a perfect match is 100%, further off scores lower. We blend all the traits into one score from 0 to 100%. The key twist: traits aren't weighted equally — energy and acousticness matter most for our focus listener, danceability barely matters — and a matching mood earns a small bonus. Each recommendation comes with plain-English reasons, like "closely matches your energy preference."

What we changed from the starter: the starter just returned the first few songs without looking at them. We made it actually compare each song's traits to the listener's wishes, added weights so important traits count more, made it explain itself, and left genre out of scoring (plus a step that avoids five near-identical picks) so results have some variety.


---

## 4. Data  


The datset holds 20 songs, seven genres: lofi (6), pop (3), synthwave (3), indie pop (2), rock (2), ambient (2), and jazz (2). No hip-hop, classical, country, metal, electronic/EDM, R&B, or world music.
I had Claude.ai add 10 additional songs.
The sample is too small and lofi-skewed to represent a realistic library, so some tastes (e.g. an intense-rock listener) have very few songs to match against.

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  
    Late-Night Focus — the two focused lofi tracks (Focus Flow, Deep Focus) top the list at 100%, exactly the calm, acoustic, low-energy songs a focus listener wants.
    High-Energy Pop and Deep Intense Rock — the loud, fast, danceable tracks rise to the top and the mellow ones sink, matching intuition.
    Chill Lofi — surfaces the quiet, acoustic, slow songs and pushes intense tracks to the bottom.
---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

The scorer only sees five numeric traits plus a mood label, so it's blind to lyrics, vocals, era, and cultural context — and it ignores genre by design, meaning a listener can be handed a song from a genre they dislike as long as the numbers match. The catalog is small and skewed toward lofi (6 of 20 songs), so listeners wanting under-represented styles like rock or jazz get thinner, lower-quality results purely because of what's in the data. Because the score blends weighted traits, a song that nails the two heaviest traits (energy and acousticness) can rank highly while missing everything else, and a sparse profile lets a single trait decide the whole ranking. The weights were tuned for a calm, focus-style listener, so users who care most about low-weighted traits like danceability — or who sit at a bland "all-neutral" middle — get less accurate or undifferentiated results. Finally, valid but extreme inputs (values outside 0–1) can produce negative trait scores and a broken "percent match," so the system silently misbehaves instead of warning the user.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  


Add more features — include era, vocals, and language, let users set their own weights, and validate inputs to 0–1.
Explain better — show each trait's contribution and score breakdown, not just which preferences matched.
Improve diversity — tune the variety penalty and spread genres/moods so one style doesn't dominate.
Handle complex tastes — support multiple moods, learn from skips/likes, and add a collaborative-filtering signal.

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

I learned about weights and how emphasizing one preference/metric can change the results.
I thought my application took into consideration everything necessary, but it turns out its not enough. I didn't bother adjusting my application to consider all those additional preferences/metrics because I don't want to burn through all my Claude.ai tokens.
I have a much deeper understanding of just how many considerations music apps make before recommending music to users. All that processing power for a few recommendations. I've only implemented a simple solution, there is so much more to consider when recommending something to someone.