
from pathlib import Path  # Handles file and folder paths
from nba_api.stats.endpoints import leaguedashplayerstats  # NBA player stats endpoint
from time import sleep  # Lets us pause between API requests

DATA_DIR = Path("data/raw")  # Folder for downloaded data
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Create folder if needed


def collect_season(season):
    # Create the filename for this season
    filename = DATA_DIR / f"player_stats_{season}.csv"

    # Skip seasons we've already downloaded
    if filename.exists():
        print(f"Skipping {season}: already downloaded")
        return

    # Display which season we're downloading
    print(f"Downloading {season}...", flush=True)

    # Request regular-season player statistics
    response = leaguedashplayerstats.LeagueDashPlayerStats(
        season=season,  # NBA season
        season_type_all_star="Regular Season",  # Exclude playoffs
        measure_type_detailed_defense="Base",  # Basic statistics
        per_mode_detailed="Totals",  # Season totals
        timeout=60  # Maximum wait in seconds
    )

    # Convert API response into a pandas DataFrame
    df = response.get_data_frames()[0]

    # Stop if the API returned no data
    if df.empty:
        raise ValueError(f"No data returned for {season}")

    # Save this season's statistics as a CSV
    df.to_csv(filename, index=False)

    # Confirm successful download
    print(f"Saved {season}: {len(df)} players")


# Loop through NBA seasons from 1998-99 to 2025-26
for year in range(1998, 2026):

    # Convert year into NBA season format
    season = f"{year}-{str(year + 1)[-2:]}"

    # Download the season's player statistics
    collect_season(season)

    # Pause between requests to reduce server load
    sleep(2)

print("Finished downloading all seasons!")  # Completion message
