
from pathlib import Path  # File paths
from time import sleep  # Pause between requests
from nba_api.stats.endpoints import (
    leaguedashplayerstats,
    leaguedashteamstats
)

DATA_DIR = Path("data/raw")  # Output directory
DATA_DIR.mkdir(parents=True, exist_ok=True)

# Dataset name -> (endpoint, game type, stat type)
DATASETS = {
    "player_stats": (
        leaguedashplayerstats.LeagueDashPlayerStats,
        "Regular Season", "Base"
    ),
    "player_advanced": (
        leaguedashplayerstats.LeagueDashPlayerStats,
        "Regular Season", "Advanced"
    ),
    "player_playoffs": (
        leaguedashplayerstats.LeagueDashPlayerStats,
        "Playoffs", "Base"
    ),
    "player_playoffs_advanced": (
        leaguedashplayerstats.LeagueDashPlayerStats,
        "Playoffs", "Advanced"
    ),
    "team_stats": (
        leaguedashteamstats.LeagueDashTeamStats,
        "Regular Season", "Base"
    ),
    "team_advanced": (
        leaguedashteamstats.LeagueDashTeamStats,
        "Regular Season", "Advanced"
    ),
    "team_playoffs": (
        leaguedashteamstats.LeagueDashTeamStats,
        "Playoffs", "Base"
    )
}



def collect_season(season):
    # Loop through every dataset configuration
    for name, (endpoint, season_type, measure) in DATASETS.items():

        # Create a unique filename for each dataset
        filename = DATA_DIR / f"{name}_{season}.csv"

        # Skip files that have already been downloaded
        if filename.exists():
            print(f"Skipping {filename.name}")
            continue

        # Request the relevant statistics
        print(f"Downloading {name} for {season}...", flush=True)
        response = endpoint(
            season=season,
            season_type_all_star=season_type,
            measure_type_detailed_defense=measure,
            per_mode_detailed="Totals",
            timeout=60
        )

        # Convert the API response to a table
        df = response.get_data_frames()[0]

        # Check that the response contains data
        if df.empty:
            raise ValueError(f"Empty data: {name}, {season}")

        # Save the table
        df.to_csv(filename, index=False)
        print(f"Saved {filename.name}: {len(df)} rows")

        # Avoid sending requests too quickly
        sleep(2)


# Process every completed NBA season
for year in range(1998, 2026):

    # Format the season, e.g. 2023-24
    season = f"{year}-{str(year + 1)[-2:]}"

    # Collect all seven datasets for this season
    collect_season(season)

print("Finished collecting NBA data!")
