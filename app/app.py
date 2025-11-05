import pandas as pd

def load_games_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # --- Normalize column names (edit if your CSV is different) ---
    rename_map = {
        'name': 'title',
        'app_name': 'title',
        'platform': 'platforms',
        'metacritic': 'rating',
        'metascore': 'rating',
        'avg_playtime': 'playtime',
        'play_time': 'playtime',
        'about': 'summary',
        'desc': 'summary',
        'description': 'summary'
    }
    for k,v in rename_map.items():
        if k in df.columns and v not in df.columns:
            df.rename(columns={k:v}, inplace=True)

    # Ensure needed columns exist
    for col in ['title','genres','platforms','playtime','rating','summary','tags']:
        if col not in df.columns:
            df[col] = None

    # Coerce to strings for text columns
    for col in ['genres','platforms','tags','summary','title']:
        df[col] = df[col].fillna('').astype(str)

    # Split comma-separated to lists (store also raw text for vectorizer)
    def split_or_empty(s):
        return [x.strip() for x in s.split(',') if x.strip()]

    df['genres_list']    = df['genres'].apply(split_or_empty)
    df['platforms_list'] = df['platforms'].apply(split_or_empty)
    df['tags_list']      = df['tags'].apply(split_or_empty)

    # Numeric clean
    for col in ['playtime','rating']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')

    # Build a “bag of words” column for content-based sim
    df['bow'] = (
        df['genres_list'].apply(lambda xs: " ".join(xs)) + " " +
        df['platforms_list'].apply(lambda xs: " ".join(xs)) + " " +
        df['tags_list'].apply(lambda xs: " ".join(xs)) + " " +
        df['summary'].fillna('')
    )

    # Drop exact duplicate titles
    df = df.drop_duplicates(subset=['title']).reset_index(drop=True)
    return df

def filter_df(df: pd.DataFrame, genre=None, platform=None, max_playtime=None, min_rating=None):
    mask = pd.Series([True]*len(df), index=df.index)
    if genre:
        mask &= df['genres_list'].apply(lambda xs: genre.lower() in [g.lower() for g in xs])
    if platform:
        mask &= df['platforms_list'].apply(lambda xs: platform.lower() in [p.lower() for p in xs])
    if max_playtime is not None:
        mask &= (df['playtime'].fillna(0) <= float(max_playtime))
    if min_rating is not None:
        mask &= (df['rating'].fillna(0) >= float(min_rating))
    return df[mask]
