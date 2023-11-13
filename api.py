from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
import pandas as pd
import time

def get_player_team(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_df = player_info.get_data_frames()[0]
    team_name = player_info_df.loc[0, 'TEAM_NAME'] if not player_info_df.empty else 'No team found'
    return team_name

# Fetch all NBA players
nba_players = players.get_players()

# Filter to include only active players
active_nba_players = [player for player in nba_players if player['is_active']]

# Initialize a DataFrame to hold all the data
all_players_data = pd.DataFrame()

# Iterate over active players and fetch their game logs and team names
for player in active_nba_players:
    print(f"Fetching game logs for {player['full_name']} (2023-2024 Season)...")

    # Get the player's current team
    team_name = get_player_team(player['id'])

    # Fetch player game logs for the 2023-2024 season
    gamelogs = playergamelog.PlayerGameLog(player_id=player['id'], season='2023-24')

    # Get the DataFrame from the game logs
    game_stats = gamelogs.get_data_frames()[0]

    # Remove 'VIDEO_AVAILABLE' column
    if not game_stats.empty:
        game_stats = game_stats.drop(columns=['VIDEO_AVAILABLE'], errors='ignore')
        game_stats['Player'] = player['full_name']
        game_stats['Team'] = team_name
        all_players_data = pd.concat([all_players_data, game_stats], ignore_index=True)

    time.sleep(1)  # Pause to avoid hitting the API rate limit

# Save the data to a CSV file
csv_file_path = 'nba_player_game_stats.csv'
all_players_data.to_csv(csv_file_path, index=False)
print(f"Data saved to {csv_file_path}")
