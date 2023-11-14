from nba_api.stats.static import players
from nba_api.stats.endpoints import playergamelog, commonplayerinfo
import pandas as pd
import time
from datetime import datetime

def get_player_team(player_id):
    player_info = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    player_info_df = player_info.get_data_frames()[0]
    return player_info_df.loc[0, 'TEAM_NAME'] if not player_info_df.empty else 'No team found'

def format_percentage(value):
    """Formats a decimal percentage value to a string with one decimal place."""
    return "{:.1f}%".format(value * 100)

def format_one_decimal(value):
    """Formats a numeric value to a string with one decimal place."""
    return "{:.1f}".format(value)

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
    'AST': 'Assists', 'STL': 'Steals', 'BLK': 'Blocks', 'TOV': 'Turnovers',
    'PF': 'PersonalFouls', 'PTS': 'Points', 'PLUS_MINUS': '+/-'
}

# Columns that need to be formatted to one decimal place
numeric_cols = ['Minutes', '2PTMade', '2PTAttempted', '3PTMade', '3PT_Attempted', 'FreeThrowsMade',
                'FreeThrowsAttempted', 'OffensiveRebounds', 'DefensiveRebounds',
                'TotRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers',
                'PersonalFouls', 'Points', '+/-']

# Iterate over active players and fetch their game logs and team names
for player in active_nba_players:  # Limiting to the first 20 for demonstration
    print(f"Fetching game logs for {player['full_name']} (2023-2024 Season)...")

    # Get the player's current team
    team_name = get_player_team(player['id'])

    # Fetch player game logs for the 2023-2024 season
    gamelogs = playergamelog.PlayerGameLog(player_id=player['id'], season='2023-24')
    if gamelogs.get_data_frames():
        game_stats = gamelogs.get_data_frames()[0]

        # Process and clean up data
        if not game_stats.empty:
            # Remove unwanted columns and rename
            game_stats = game_stats.drop(columns=['SEASON_ID', 'PLAYER_ID', 'GAME_ID'], errors='ignore')
            game_stats.rename(columns=column_mapping, inplace=True)

            # Add Player and Team columns, format percentages
            game_stats['Player'] = player['full_name']
            game_stats['Team'] = team_name
            for col in ['2PT_%', '3PT_%', 'FreeThrow%']:
                game_stats[col] = game_stats[col].apply(format_percentage)

            # Reorder columns
            columns_order = ['Player', 'Team', 'GAME_DATE', 'MATCHUP', 'Win/Loss', 'Minutes', '2PTMade', '2PTAttempted', '2PT_%', '3PTMade', '3PT_Attempted', '3PT_%', 'FreeThrowsMade', 'FreeThrowsAttempted', 'FreeThrow%', 'OffensiveRebounds', 'DefensiveRebounds', 'TotRebounds', 'Assists', 'Steals', 'Blocks', 'Turnovers', 'PersonalFouls', 'Points', '+/-']
            game_stats = game_stats[columns_order]

            # Calculate averages for numeric columns
            averages = game_stats[numeric_cols].mean()

            # Format numeric columns with one decimal
            for col in numeric_cols:
                averages[col] = format_one_decimal(averages[col])

            # Calculate and format averages for percentage columns
            averages_percentage = game_stats[['2PT_%', '3PT_%', 'FreeThrow%']].replace('%', '', regex=True).astype(float).mean()
            for col in ['2PT_%', '3PT_%', 'FreeThrow%']:
                averages[col] = format_percentage(averages_percentage[col] / 100)

            # Add Player and Team for the averages row
            averages['Player'] = player['full_name'] + ' - Average'
            averages['Team'] = 'Average'

            # Append the averages row
            averages_df = pd.DataFrame([averages])
            game_stats = pd.concat([game_stats, averages_df], ignore_index=True)

            # Concatenate with the main DataFrame
            all_players_data = pd.concat([all_players_data, game_stats], ignore_index=True)

        time.sleep(2)  # Pause to avoid hitting the API rate limit

# Get current date
current_date = datetime.now().strftime("%Y%m%d")

# Save the data to a CSV file with current date appended
csv_file_path = f'nba_player_game_stats_{current_date}.csv'
all_players_data.to_csv(csv_file_path, index=False)
print(f"Data saved to {csv_file_path}")
