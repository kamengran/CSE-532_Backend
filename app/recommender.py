import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class ContentRecommender:
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=5000
        )
        self.matrix = self.vectorizer.fit_transform(self.df['bow'])

    def recommend(self, query_text: str, top_k: int = 10) -> pd.DataFrame:
        if not query_text.strip():
            # If no keywords, just return popular/top rated
            return self.df.sort_values('rating', ascending=False).head(top_k)

        qvec = self.vectorizer.transform([query_text])
        sims = cosine_similarity(qvec, self.matrix).ravel()
        self.df['score'] = sims
        return self.df.sort_values('score', ascending=False).head(top_k)
