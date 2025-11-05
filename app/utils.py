import pandas as pd

def load_games_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in ["title","genres","platforms","playtime","rating","summary","tags"]:
        if col not in df.columns:
            df[col] = None

    def split_list(s):
        s = "" if pd.isna(s) else str(s)
        return [x.strip() for x in s.split(",") if x.strip()]

    df["genres_list"] = df["genres"].apply(split_list)
    df["platforms_list"] = df["platforms"].apply(split_list)
    df["tags_list"] = df["tags"].apply(split_list)

    for col in ["playtime","rating"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df["bow"] = (
        df["genres_list"].apply(lambda xs: " ".join(xs)) + " " +
        df["platforms_list"].apply(lambda xs: " ".join(xs)) + " " +
        df["tags_list"].apply(lambda xs: " ".join(xs)) + " " +
        df["summary"].fillna("")
    )
    return df.drop_duplicates(subset=["title"]).reset_index(drop=True)

def filter_df(df: pd.DataFrame, genre=None, platform=None, max_playtime=None, min_rating=None):
    mask = pd.Series(True, index=df.index)
    if genre:
        mask &= df["genres_list"].apply(lambda xs: genre.lower() in [g.lower() for g in xs])
    if platform:
        mask &= df["platforms_list"].apply(lambda xs: platform.lower() in [p.lower() for p in xs])
    if max_playtime is not None:
        mask &= (df["playtime"].fillna(0) <= float(max_playtime))
    if min_rating is not None:
        mask &= (df["rating"].fillna(0) >= float(min_rating))
    return df[mask]
