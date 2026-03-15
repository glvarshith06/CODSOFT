# ============================================================
# TASK 4 - RECOMMENDATION SYSTEM
# CodSoft AI Internship
# Techniques: Collaborative Filtering + Content-Based Filtering
# ============================================================

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

# ── Sample Dataset ───────────────────────────────────────────

# Movie metadata for Content-Based Filtering
movies = pd.DataFrame({
    "movie_id": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "title": [
        "The Matrix", "John Wick", "Inception", "Interstellar",
        "The Notebook", "Titanic", "Avengers: Endgame", "Iron Man",
        "The Dark Knight", "Forrest Gump"
    ],
    "genres": [
        "Action Sci-Fi",
        "Action Thriller",
        "Action Sci-Fi Thriller",
        "Sci-Fi Drama",
        "Romance Drama",
        "Romance Drama",
        "Action Adventure Sci-Fi",
        "Action Sci-Fi",
        "Action Crime Drama",
        "Drama Romance"
    ]
})

# User-Movie ratings for Collaborative Filtering (0 = not rated)
ratings_data = {
    "Alice":   [5, 4, 0, 0, 1, 2, 5, 4, 5, 0],
    "Bob":     [4, 5, 4, 3, 0, 0, 4, 5, 4, 0],
    "Carol":   [0, 0, 0, 0, 5, 5, 0, 0, 0, 5],
    "Dave":    [4, 3, 5, 5, 0, 0, 3, 4, 5, 0],
    "Eve":     [0, 0, 0, 5, 0, 0, 0, 0, 4, 0],
    "Frank":   [0, 0, 4, 5, 0, 0, 5, 3, 4, 0],
}

ratings_df = pd.DataFrame(ratings_data, index=movies["title"])


# ── 1. CONTENT-BASED FILTERING ───────────────────────────────

def content_based_recommend(movie_title: str, top_n: int = 5):
    """
    Recommend movies similar to the given title based on genre similarity.
    Uses TF-IDF + Cosine Similarity on genre tags.
    """
    tfidf = TfidfVectorizer(stop_words="english")
    tfidf_matrix = tfidf.fit_transform(movies["genres"])
    sim_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Find index of the given movie
    indices = pd.Series(movies.index, index=movies["title"])
    if movie_title not in indices:
        print(f"  ⚠️  '{movie_title}' not found in the dataset.")
        return []

    idx = indices[movie_title]
    sim_scores = list(enumerate(sim_matrix[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = [s for s in sim_scores if s[0] != idx][:top_n]

    recommended = movies["title"].iloc[[s[0] for s in sim_scores]].tolist()
    return recommended


# ── 2. COLLABORATIVE FILTERING (User-Based) ──────────────────

def collaborative_recommend(user_name: str, top_n: int = 5):
    """
    Recommend movies for a user based on ratings of similar users.
    Uses User-Based Cosine Similarity.
    """
    if user_name not in ratings_df.columns:
        print(f"  ⚠️  User '{user_name}' not found.")
        return []

    # Compute user-user cosine similarity
    user_matrix = ratings_df.T  # shape: (users x movies)
    sim_matrix = cosine_similarity(user_matrix)
    sim_df = pd.DataFrame(sim_matrix, index=ratings_df.columns, columns=ratings_df.columns)

    # Get similarity scores of all other users to the target user
    user_sim = sim_df[user_name].drop(user_name).sort_values(ascending=False)

    # Weighted average of ratings from similar users
    weighted_scores = {}
    sim_sum = {}

    for other_user, sim_score in user_sim.items():
        if sim_score <= 0:
            continue
        for movie in ratings_df.index:
            # Only consider movies the target user hasn't rated
            if ratings_df.loc[movie, user_name] == 0:
                rating = ratings_df.loc[movie, other_user]
                if rating > 0:
                    weighted_scores[movie] = weighted_scores.get(movie, 0) + sim_score * rating
                    sim_sum[movie] = sim_sum.get(movie, 0) + sim_score

    if not weighted_scores:
        return []

    # Normalize
    predicted = {m: weighted_scores[m] / sim_sum[m] for m in weighted_scores}
    predicted_series = pd.Series(predicted).sort_values(ascending=False)

    return predicted_series.head(top_n).index.tolist()


# ── 3. HYBRID: combine both methods ──────────────────────────

def hybrid_recommend(user_name: str, liked_movie: str, top_n: int = 5):
    """
    Combine content-based and collaborative filtering results.
    """
    cb = set(content_based_recommend(liked_movie, top_n))
    cf = set(collaborative_recommend(user_name, top_n))

    # Movies in both = highest confidence
    both = cb & cf
    only_cb = cb - cf
    only_cf = cf - cb

    combined = list(both) + list(only_cb) + list(only_cf)
    return combined[:top_n]


# ── Main Demo ────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("      🎬  Movie Recommendation System  🎬")
    print("=" * 55)

    # ── Content-Based ──────────────────────────────────────
    print("\n📌 Content-Based Filtering")
    print("   'If you liked X, you might also like...'")
    test_movie = "The Matrix"
    recs = content_based_recommend(test_movie, top_n=4)
    print(f"\n   Because you liked: {test_movie}")
    for i, r in enumerate(recs, 1):
        print(f"   {i}. {r}")

    # ── Collaborative ──────────────────────────────────────
    print("\n📌 Collaborative Filtering (User-Based)")
    print("   'Users like you also enjoyed...'")
    test_user = "Alice"
    recs = collaborative_recommend(test_user, top_n=4)
    print(f"\n   Recommendations for {test_user}:")
    for i, r in enumerate(recs, 1):
        print(f"   {i}. {r}")

    # ── Hybrid ─────────────────────────────────────────────
    print("\n📌 Hybrid Recommendation")
    print("   'Combining your taste + similar users'")
    recs = hybrid_recommend("Alice", "Inception", top_n=4)
    print(f"\n   Hybrid recommendations for Alice (liked Inception):")
    for i, r in enumerate(recs, 1):
        print(f"   {i}. {r}")

    # ── Interactive ────────────────────────────────────────
    print("\n" + "=" * 55)
    print("  🔍 Try it yourself!")
    print("=" * 55)
    print("\nAvailable movies:")
    for _, row in movies.iterrows():
        print(f"  - {row['title']}  [{row['genres']}]")

    print("\nAvailable users:", ", ".join(ratings_df.columns))

    print("\n--- Content-Based ---")
    movie_input = input("Enter a movie you like: ").strip()
    recs = content_based_recommend(movie_input, top_n=5)
    if recs:
        print("Recommended movies:")
        for i, r in enumerate(recs, 1):
            print(f"  {i}. {r}")

    print("\n--- Collaborative ---")
    user_input = input("Enter your name (from list above): ").strip()
    recs = collaborative_recommend(user_input, top_n=5)
    if recs:
        print(f"Recommended for {user_input}:")
        for i, r in enumerate(recs, 1):
            print(f"  {i}. {r}")


if __name__ == "__main__":
    main()
