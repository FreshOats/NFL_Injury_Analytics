# NFL_Injury_Cleaning_Functions
# This contains all of the functions for data cleaning for the 1st and Future Analytics data


# HOW TO USE: 
# 1. In dependencies, you will type: 
#     from NFL_Cleaning_Functions import *
# 2. To use this file, the only functions that need to be called will be the Vis_Data_Cleaner or 
# the ML_Data_Cleaner, which each call on the playlist.csv and injuryrecords.cvs, outputting a 
# cleaned and merged dataframe. All other functions are required to run those functions


########################## Primary Cleaning Functions ############################
# This function cleans the Concussion data from the Punt Analytics
def clean_punt(df, process):
    
    if process == 'vis':
        # Load and Clean the data
        df = column_capitalizer(df, 'punt')
        df = surface_normalizer(df)
        df = stadium_coder(df)
        df = position_coder(df, 'punt', 'vis')
        df = score_manager(df)
        df = game_adjuster(df)
        df = fake_id_maker(df)
        df = find_twist(df)
        df.drop(columns=['GameKey',
                        'PlayID',
                        'GSISID',
                        'Outdoor',
                        'season_year', 
                        'Turnover_Related'], inplace=True)
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    elif process == 'ml':
        df = column_capitalizer(df, 'punt')
        df = surface_normalizer(df)
        df = surface_coder(df)
        df = stadium_coder(df)
        df = position_coder(df, 'punt', 'ml')
        df = score_manager(df)
        df = game_adjuster(df)
        df = fake_id_maker(df)
        df = find_twist(df)
        df = play_maker(df)
        df = impact_maker(df)

        df.drop(columns=['GameKey',
                         'PlayID',
                         'GSISID',
                         'StadiumType',
                         'Turnover_Related',
                         'FieldType', 
                         'g_time',
                         'season_year'], inplace=True)
        df.drop_duplicates(inplace=True)
        df.reset_index(drop=True, inplace=True)
        return df

    return df






# This will clean and merge the injury data with an outer merge, containing all injury and 
# non-injury data from playlist.cvs and injuryrecord.csv, maintaining categorical data in the Vis_ 
# function and changing all to numeric data for the ML_ function. 
# PlayKey is the primary key to merge with the tracking dat

def clean_and_merge(playlist, injuries, process):
    import pandas as pd

    if process == 'vis':
        # Load and Clean the data
        playlist = column_capitalizer(playlist, 'playlist')
        playlist = surface_coder(playlist)
        playlist = stadium_coder(playlist)
        playlist = position_coder(playlist)
        playlist = play_coder(playlist)
        playlist = playerday_adjuster(playlist)
        playlist.drop(columns=['PlayerKey', 'GameID', 'Weather', 'Temperature', 'SyntheticField',
                               'Outdoor', 'RosterPosition_Num', 'Position_Num', 'PlayCode'], inplace=True)

        injuries = column_capitalizer(injuries, 'injuries')
        injuries = bodypart_coder(injuries)
        injuries = injury_duration_coder(injuries, process)

        injuries.PlayKey.dropna(inplace=True)

        #Drop redundant columns
        injuries.drop(columns=['GameID',
                               'PlayerKey',
                               'InjuryType',
                               'Surface',
                               'DM_M1',
                               'DM_M7',
                               'DM_M28',
                               'DM_M42'], inplace=True)

        # Merge the datasets
        merged = pd.merge(playlist, injuries, on='PlayKey', how='outer')

        # clean the datasets
        merged = clean_noninjured(merged, process)
        return merged

    elif process == 'ml':
        playlist = column_capitalizer(playlist, 'playlist')
        playlist = surface_coder(playlist)
        playlist = stadium_coder(playlist)
        playlist = position_coder(playlist)
        playlist = play_coder(playlist)
        playlist = playerday_adjuster(playlist)
        playlist.drop(columns=['PlayerKey', 'GameID', 'Weather', 'Temperature', 'StadiumType',
                               'FieldType', 'RosterPosition', 'Position', 'PlayType'], inplace=True)

        injuries = column_capitalizer(injuries, 'injuries')
        injuries = bodypart_coder(injuries)
        injuries = injury_duration_coder(injuries, process)

        injuries = injuries.loc[injuries.PlayKey.isna() == False]

        injuries.drop(columns=['GameID',
                               'PlayerKey',
                               'Surface',
                               'BodyPart',
                               'DM_M1',
                               'DM_M7',
                               'DM_M28',
                               'DM_M42'], inplace=True)

        merged = pd.merge(playlist, injuries, on='PlayKey', how='outer')
        merged = clean_noninjured(merged, process)
        return merged

    return merged







############################## Functions for ALL ANALYSES #############################
# This Codes the Stadium Stype as either Indoor or Outdoor, necessary for ALL analysis

# This function capitalizes all of the headers in the dataframes
def column_capitalizer(df, df_name):

    if df_name == 'playlist':
        columns = {
            'playerkey': 'PlayerKey',
            'gameid': 'GameID',
            'playkey': 'PlayKey',
            'rosterposition': 'RosterPosition',
            'playerday': 'PlayerDay',
            'playergame': 'PlayerGame',
            'stadiumtype': 'StadiumType',
            'fieldtype': 'FieldType',
            'temperature': 'Temperature',
            'weather': 'Weather',
            'playtype': 'PlayType',
            'playergameplay': 'PlayerGamePlay',
            'position': 'Position',
            'postiongroup': 'PositionGroup',
        }

    elif df_name == 'injuries':
        columns = {
            'playerkey': 'PlayerKey',
            'gameid': 'GameID',
            'playkey': 'PlayKey',
            'bodypart': 'BodyPart',
            'fieldtype': 'Surface',
            'dm_m1': 'DM_M1',
            'dm_m7': 'DM_M7',
            'dm_m28': 'DM_M28',
            'dm_m42': 'DM_M42'
        }

    elif df_name == 'punt':
        columns = {
            'gamekey': 'GameKey',
            'playid': 'PlayID',
            'gsisid': 'GSISID',
            'p_position': 'Position',
            'prole': 'Role',
            'season_type': 'Season_Type',
            'quarter': 'Quarter',
            'week': 'Week',
            'stadiumtype': 'StadiumType',
            'turf': 'Turf',
            'gameweather': 'Weather',
            'temperature': 'Temperature',
            'score_home_visiting': 'Score_Home_Visiting', 
            'player_activity': 'Player_Activity',
            'turnover_related': 'Turnover_Related',
            'impact_type': 'Impact_Type'
        }

    df = df.rename(columns=columns)

    return df



# stadium_coder: This function changes the stadium type to either Outdoor or Indoor, maintaining the categorical label
def stadium_coder(df):
    df.StadiumType.fillna('Outdoor', inplace=True)
    
    stadiums = {'Outdoor': 'Outdoor',
               'outdoor': 'Outdoor',
               'Indoors': 'Indoor',
               'Indoors (Domed)': 'Indoor',
               'Oudoor': 'Outdoor',
               'Outdoors': 'Outdoor',
               'Outdoors ': 'Outdoor',
               'Open': 'Outdoor',
               'Closed Dome': 'Indoor',
               'Domed, closed': 'Indoor',
               'Dome': 'Indoor',
               'Indoor': 'Indoor',
               'Domed': 'Indoor',
               'Retr. Roof-Closed': 'Indoor',
               'Outdoor Retr Roof-Open': 'Outdoor',
               'Retractable Roof': 'Indoor',
               'Ourdoor': 'Outdoor',
               'Indoor, Roof Closed': 'Indoor',
               'Retr. Roof - Closed': 'Indoor',
               'Bowl': 'Outdoor',
               'Outddors': 'Outdoor',
               'Retr. Roof-Open': 'Outdoor',
               'Dome, closed': 'Indoor',
               'Indoor, Open Roof': 'Outdoor',
               'Domed, Open': 'Outdoor',
               'Domed, open': 'Outdoor',
               'Heinz Field': 'Outdoor',
               'Cloudy': 'Outdoor',
               'Retr. Roof - Open': 'Outdoor',
               'Retr. Roof Closed': 'Indoor',
               'Outdor': 'Outdoor',
               'Outside': 'Outdoor',
               'Indoor, non-retractable roof': 'Indoor',
               'Retr. roof - closed': 'Indoor',
               'Indoor, fixed roof ': 'Indoor',
               'Indoor, Non-Retractable Dome': 'Indoor',
               'Indoor, Fixed Roof': 'Indoor',
               'Indoor, fixed roof': 'Indoor'}
    

    df.StadiumType.replace(stadiums, inplace=True)

    # Create a new column with stadiums coded numerically
    stadium = {
        'Outdoor': 1, 
        'Indoor': 0
    }
    
    # Map the stadiumtype for outdoor as 1 = True and 0 = false
    df['Outdoor'] = df.StadiumType.map(stadium)
    return df






# playerday_adjuster: This function adjusts the player day to remove the negative values
def playerday_adjuster(df):
    df['DaysPlayed'] = df['PlayerDay'].apply(lambda x: x + 63 if x < 200 else x - 273)

    df.drop(columns='PlayerDay', inplace=True)

    return df


# play_coder: This function creates a categorical grouping for the different types of plays, grouping into passing, rushing, or kicking plays
def play_coder(df):    
    play_type = {
        'Pass': 'Pass',
        'Rush': 'Rush',
        'Extra Point': 'Kick',
        'Kickoff': 'Kick',
        'Punt': 'Punt',
        'Field Goal': 'Kick',
        'Kickoff Not Returned': 'Kick',
        'Punt Not Returned': 'Punt',
        'Kickoff Returned': 'Kick',
        'Punt Returned': 'Punt'
    }

    play_map = {
        'Pass': 0, 
        'Rush': 1, 
        'Punt': 2,
        'Kick': 3
    }

    df.PlayType.replace(play_type, inplace=True)
    df['PlayCode'] = df.PlayType.map(play_map)
    
    df = df.loc[df.PlayType.isna() == False]

    return df


# bodypart_coder: This function codifies the injury types, adding this as a new column called "InjuryType"
def bodypart_coder(df):
    injury_map = {
        'NoInjury': 0,
        'Foot': 1,
        'Ankle': 2,
        'Knee': 3
    }

    df['InjuryType'] = df.BodyPart.map(injury_map)

    # Remove any injuries not associated with a play
    df = df.loc[df.PlayKey.isna() == False]
    return df

# Injury_Duration_Classifier: This creates a new list of numerical values as the shortest number of days of injury
def injury_duration_classifier(row):
    injury_duration = 0
    if row["DM_M42"] == 1:
        injury_duration = 42
    else:
        if row["DM_M28"] == 1:
            injury_duration = 28
        else:
            if row["DM_M7"] == 1:
                injury_duration = 7
            else: 
                injury_duration = 1
    
    return injury_duration

# injury duration coder supplies either a string or numeric for the severity of an injury if the df is for ml or vis
def injury_duration_coder(df, process): 
    # Injury_Duration_Coder: Apply the Injury Duration Classifier to the dataframe

    df['InjuryDuration'] = df.apply(injury_duration_classifier, axis=1)
    df.InjuryDuration.astype(int)
    
    if process == 'ml':
        severity_map = {
            42: 1, 
            28: 1,
            7: 0, 
            1: 0 
        }
        df['SevereInjury'] = df.InjuryDuration.map(severity_map)
        df.SevereInjury.astype(int)
        return df
    
    elif process == 'vis':
        severity_map = {
            42: 'Severe',
            28: 'Severe',
            7: 'Mild',
            0: 'Mild'
        }
        df['SevereInjury'] = df.InjuryDuration.map(severity_map)
        return df

    return df

        
# This function returns all positions as 
# the 1-2 letter abbreviations for all position, and supplies a numerical version for ml, 
# the unneccessary columns will be removed before merging the tables
def position_coder(df, dataset='injury', process='vis'):
    import numpy as np

    position = {
        'Quarterback': 'QB',
        'Running Back': 'RB',
        'Wide Receiver': 'WR',
        'Tight End': 'TE',
        'Offensive Lineman': 'OL',
        'Kicker': 'K',
        'Defensive Lineman': 'DL',
        'Linebacker': 'LB',
        'Cornerback': 'CB',
        'Safety': 'S'
    }

    numerical = {
        'Quarterback': 0,
        'QB': 0,
        'Running Back': 1,
        'RB': 1,
        'FB': 2,
        'Wide Receiver': 3,
        'WR': 3,
        'Tight End': 4,
        'TE': 4,
        'Offensive Lineman': 5,
        'OL': 5,
        'C': 6,
        'G': 7,
        'LG': 8,
        'RG': 9,
        'T': 10,
        'LT': 11,
        'RT': 12,
        'Kicker': 13,
        'K': 13,
        'KR': 14,
        'Defensive Lineman': 15,
        'DL': 15,
        'DE': 16,
        'DT': 17,
        'NT': 18,
        'Linebacker': 19,
        'LB': 19,
        'OLB': 20,
        'ILB': 21,
        'MLB': 22,
        'DB': 23,
        'Cornerback': 24,
        'CB': 24,
        'Safety': 25,
        'S': 25,
        'SS': 26,
        'FS': 27,
        'P': 28,
        'PR': 29,
        'HB': 30, 
        'LS': 31
    }

    if dataset == 'injury':
        df['Position'] = np.where(
            df['Position'] == 'Missing Data', df['RosterPosition'], df['Position'])

        df.RosterPosition.replace(position, inplace=True)
        df.Position.replace(position, inplace=True)

        df['RosterPosition_Num'] = df.RosterPosition.map(numerical)
        df.RosterPosition_Num.astype(int)

        df['Position_Num']= df.Position.map(numerical)
        df.Position_Num.astype(int)

        df.drop(columns='PositionGroup', inplace=True)
        return df

    elif dataset == 'punt':
        df.dropna(subset=['Position'], inplace=True)
        if process == 'ml':
            df.Position.replace(numerical, inplace=True)
            df.Position.astype(int)
            return df
        else: 
            return df

    return df


# This codes the Surface from Categorical to Numerical
def surface_coder(df):
    # surface_coder: Function that encodes the Field Surface to identify natural or synthetic
    surface_map = {
        'Natural': 0,
        'Synthetic': 1
    }

    
    df['SyntheticField'] = df.FieldType.map(surface_map)
    return df

# This function changes the different types of turfs listed in the punt group to either Natural or Synthetic
def surface_normalizer(df):
    turfs = {
        'Grass': 'Natural',
        'Field Turf': 'Synthetic',
        'Natural Grass': 'Natural',
        'grass': 'Natural',
        'Artificial': 'Synthetic',
        'FieldTurf': 'Synthetic',
        'DD GrassMaster': 'Synthetic',
        'A-Turf Titan': 'Synthetic',
        'UBU Sports Speed S5-M': 'Synthetic',
        'UBU Speed Series S5-M': 'Synthetic',
        'Artifical': 'Synthetic',
        'UBU Speed Series-S5-M': 'Synthetic',
        'FieldTurf 360': 'Synthetic',
        'Natural grass': 'Natural',
        'Field turf': 'Synthetic',
        'Natural': 'Natural',
        'Natrual Grass': 'Natural',
        'Synthetic': 'Synthetic',
        'Natural Grass ': 'Natural',
        'Naturall Grass': 'Natural',
        'FieldTurf360': 'Synthetic'}

    df['FieldType'] = df.Turf.map(turfs)
    df.drop(columns='Turf', inplace=True)
    return df

# This function fills the NaN values after performing an outer merge 
def clean_noninjured(df, process):
    if process == 'vis':
        df.BodyPart.fillna('NoInjury', inplace=True)
        df.InjuryDuration.fillna(0, inplace=True)
        df.SevereInjury.fillna('NoInjury', inplace=True)
        df['IsInjured'] = df.BodyPart.apply(
            lambda x: "NoInjury" if x == 'NoInjury' else "Injured")
        return df

    elif process == 'ml':
        df.InjuryType.fillna(0, inplace=True)
        df.InjuryDuration.fillna(0, inplace=True)
        df.SevereInjury.fillna(0, inplace=True)
        df['IsInjured'] = df.InjuryType.apply(
            lambda x: 0 if x == 0 else 1)
        return df

    return df


# The find_twist function determines the difference between the
#  direction the player is running vs facing, adjusting for the differences in direction of play
def find_twist(df):
    df['new_o'] = abs(df.o - 180)
    df['new_dir'] = abs(df.dir - 180)
    df['Twist'] = abs(df.new_o - df.new_dir)
    df.drop(columns=['dir', 'o', 'new_o', 'new_dir'], inplace=True)

    return df


# The Score Manager function takes the Home_Away scores from the Punt_Analytics dataset and creates a new column with the home score, 
# and it also creates a column with the home-away difference, since there is a potential that the score difference correlates with the injuries 
def score_manager(df): 
    df['HomeScore'] = df.Score_Home_Visiting.apply(lambda row: [int(score) for score in row.split() if score.isdigit()][0])
    df['Score_Difference'] = df.Score_Home_Visiting.apply(lambda row: [int(score) for score in row.split(
    ) if score.isdigit()][0] - [int(score) for score in row.split() if score.isdigit()][1])

    df.drop(columns='Score_Home_Visiting', inplace=True)
    
    return df


# Game Adjuster - the games in the Punt datasets reset at 1 for each subseason, so preseason is always game 1, 
# then reg season starts at game 1, and post at game 1. Since it's likely that the concussions will increase as the 
# year progresses, we need to fix this so that preseason starts at 1, then the first game of reg is 5, and post at 23
def game_adjuster(df): 
    import numpy as np
    df.Week = np.where(df.Season_Type == 'Reg', df.Week + 5, df.Week)
    df.Week = np.where(df.Season_Type == 'Post', df.Week + 22, df.Week)
    df.drop(columns='Season_Type', inplace=True)

    return df

# The Punt tables don't have a unique identifier, so we will need to create unique identifiers for them
def fake_id_maker(df):
    cols = ['GameKey', 'PlayID']
    player_cols = ['GameKey', 'PlayID', 'GSISID']

    df['GamePlay'] = df[cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)
    df['GamePlay_ID'] = df[player_cols].apply(lambda row: '-'.join(row.values.astype(str)), axis=1)

    return df


# The Punt tables have 4 unique types of plays associated with concussions: Blocked, Blocking, Tackled, Tackling, which need to be coded for ML 
def play_maker(df):
    activities = {
        'None': 0,
        'Blocking': 1, 
        'Blocked': 2, 
        'Tackling': 3, 
        'Tackled': 4
    }
    df.Player_Activity.replace(activities, inplace=True)

    return df

def impact_maker(df):
    impacts = {
        'None': 0,
        'Helmet-to-body': 1, 
        'Helmet-to-helmet': 2, 
        'Helmet-to-ground': 3,
        'Unclear': 4
    }
    df.Impact_Type.replace(impacts, inplace=True)
    return df