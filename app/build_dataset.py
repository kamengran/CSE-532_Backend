import requests
import csv
import time
import os

# === STEP 1: Insert your RAWG API key here ===
API_KEY = "49b57452637744359a3ba7021f7f6454"

# === STEP 2: Config ===
BASE_URL = "https://api.rawg.io/api/games"
TOTAL_GAMES = 10000   
PAGE_SIZE = 40
OUT_PATH = "data/games.csv"

def fetch_page(page: int):
    """Fetch one page of games from RAWG."""
    params = {
        "key": API_KEY,
        "page": page,
        "page_size": PAGE_SIZE,
        "ordering": "-added"
    }
    r = requests.get(BASE_URL, params=params, timeout=15)
    r.raise_for_status()
    return r.json().get("results", [])

def game_to_row(game: dict):
    """Convert a RAWG game entry to a row matching your backend schema (with release date)."""
    title = game.get("name", "").strip()
    genres = ", ".join(g["name"] for g in game.get("genres", []))
    platforms = ", ".join(
        p["platform"]["name"] for p in game.get("platforms", []) if p.get("platform")
    )
    playtime = game.get("playtime") or ""
    rating = int((game.get("rating") or 0) * 20)  # convert 0–5 → 0–100
    released = game.get("released") or ""         # <-- new column
    summary_parts = [
        game.get("slug", "").replace("-", " "),
        f"Genres: {genres}" if genres else "",
        f"Available on: {platforms}" if platforms else "",
        f"Released: {released}" if released else ""
    ]
    summary = ". ".join(p for p in summary_parts if p)
    tags_data = game.get("tags") or []
    tags = ", ".join(t["name"] for t in tags_data[:8]) or genres
    return {
        "title": title,
        "genres": genres,
        "platforms": platforms,
        "playtime": playtime,
        "rating": rating,
        "released": released,    # <-- new column added
        "summary": summary,
        "tags": tags
    }

def main():
    all_rows = []
    page = 1
    while len(all_rows) < TOTAL_GAMES:
        print(f"Fetching page {page}...")
        results = fetch_page(page)
        if not results:
            break
        for g in results:
            row = game_to_row(g)
            if row["title"]:
                all_rows.append(row)
                if len(all_rows) >= TOTAL_GAMES:
                    break
        page += 1
        time.sleep(0.3)  # polite delay

    # Ensure directory exists
    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)

    print(f"Writing {len(all_rows)} games to {OUT_PATH} ...")
    fieldnames = ["title", "genres", "platforms", "playtime", "rating", "released", "summary", "tags"]
    with open(OUT_PATH, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(all_rows)
    print("✅ Done! File saved successfully.")

if __name__ == "__main__":
    main()
