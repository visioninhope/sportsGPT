from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
import pandas as pd
import time
from datetime import datetime

def get_player_team(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_df = player_info.get_data_frames()[0]
    return player_info_df.loc[0, 'TEAM_NAME'] if not player_info_df.empty else 'No team found'

# Fetch all NBA players
nba_players = players.get_players()

# Filter to include only active players
active_nba_players = [player for player in nba_players if player['is_active']]

# Initialize a DataFrame to hold all the data
all_players_data = pd.DataFrame()

# Mapping of original column names to new names
column_mapping = {
    'WL': 'Win/Loss', 'MIN': 'Minutes', 'FGM': '2PTMade', 'FGA': '2PTAttempted',
    'FG_PCT': '2PT_%', 'FG3M': '3PTMade', 'FG3A': '3PT_Attempted', 'FG3_PCT': '3PT_%',
    'FTM': 'FreeThrowsMade', 'FTA': 'FreeThrowsAttempted', 'FT_PCT': 'FreeThrow%',
    'OREB': 'OffensiveRebounds', 'DREB': 'DefensiveRebounds', 'REB': 'TotRebounds',
    'AST': 'Assists', 'STL': 'Steals', 'BLK': 'Blocks', 'TO': 'Turnovers',
    'PF': 'PersonalFouls', 'PTS': 'Points', 'PLUS_MINUS': '+/-'
}

# Iterate over active players and fetch their game logs and team names
for player in active_nba_players[:20]:  # Limiting to the first 20 for demonstration
    print(f"Fetching game logs for {player['full_name']} (2023-2024 Season)...")

    # Get the player's current team
    team_name = get_player_team(player['id'])

    # Fetch player game logs for the 2023-2024 season
    gamelogs = playergamelog.PlayerGameLog(player_id=player['id'], season='2023-24')
    game_stats = gamelogs.get_data_frames()[0]

    # Process and clean up data
    if not game_stats.empty:
        # Remove unwanted columns
        game_stats = game_stats.drop(columns=['SEASON_ID', 'PLAYER_ID', 'GAME_ID'], errors='ignore')

        # Rename columns
        game_stats.rename(columns=column_mapping, inplace=True)

        # Format percentage columns
        game_stats['2PT_%'] = (game_stats['2PT_%'] * 100).round(1).astype(str) + '%'
        game_stats['3PT_%'] = (game_stats['3PT_%'] * 100).round(1).astype(str) + '%'
        game_stats['FreeThrow%'] = (game_stats['FreeThrow%'] * 100).round(1).astype(str) + '%'

        # Add Player and Team columns
        game_stats['Player'] = player['full_name']
        game_stats['Team'] = team_name

        # Reorder columns
        columns_order = ['Player', 'Team', 'GAME_DATE', 'MATCHUP', 'Win/Loss', 'Minutes', '2PTMade', '2PTAttempted', '2PT_%', '3PTMade', '3PT_Attempted', '3PT_%', 'FreeThrowsMade', 'FreeThrowsAttempted', 'FreeThrow%', 'OffensiveRebounds', 'DefensiveRebounds', 'TotRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'PersonalFouls', 'Points', '+/-']
        game_stats = game_stats[columns_order]

        # Calculate and append averages
        averages = game_stats.mean(numeric_only=True)
        averages['Player'] = player['full_name'] + ' - Average'
        averages['Team'] = 'Average'
        game_stats = game_stats.append(averages, ignore_index=True)

        all_players_data = pd.concat([all_players_data, game_stats], ignore_index=True)

    time.sleep(1)  # Pause to avoid hitting the API rate limit

# Get current date
current_date = datetime.now().strftime("%Y%m%d")

# Save the data to a CSV file with current date appended
csv_file_path = f'nba_player_game_stats_{current_date}.csv'
all_players_data.to_csv(csv_file_path, index=False)
print(f"Data saved to {csv_file_path}")
