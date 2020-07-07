import pandas as pd
import numpy as np
import os

class InitData:

    def __init__(self):

        self.dataset = pd.read_csv("data-set.csv")

        # GW: Game Week         CLUB: Club Name
        # W: Wins               D: Draws
        # L: Loss               GS: Goals Scored
        # GC: Goals Conseded    FP: Final Position
        # CS: Clean Sheets
        # COULMNS = ["GW", "CLUB", "W", "D", "L", "GS", "GC", "CS", "FP"]

        SEASONS = list(np.unique(self.dataset["Season"]))
        SEASONS = SEASONS[SEASONS.index("2007-08"):]

        FRAMES = {}

        for season in SEASONS:
            FRAMES[season] = pd.DataFrame(self.table(season))


        for season in SEASONS:
            # Beacuase in Early Stages it isn't clear so I will take the secound round of the league
            FRAMES[season] = FRAMES[season][13:]

        
        # Creating new dir and save each dataframe in csv file

        MODIFIED_PATH = "./modified-data"
        if not os.path.exists(MODIFIED_PATH):
            os.mkdir(MODIFIED_PATH)
            
        with open(os.path.join(MODIFIED_PATH, "Seasons.txt"), "a") as f:
            for season in SEASONS:
                FRAMES[season].to_csv(os.path.join(MODIFIED_PATH, f"{season}.csv"))
                f.write(f"{season}\n")

            f.close()



    def table(self, season):
        s = self.dataset.loc[self.dataset["Season"] == season]
        CLUBS = s["HomeTeam"]
        CLUBS = np.unique(CLUBS)
        Rows = {}
        for c in CLUBS:
            club = pd.concat([s.loc[s["HomeTeam"] == c], s.loc[s["AwayTeam"] == c]], ignore_index=True)
            row = {}
            for i in club.index[:19]:
                if len(row) == 0:
                    if club["FTHG"][i] > club["FTAG"][i] and club["FTAG"][i] ==0:
                        row[f"{i+1}"] = [1, 0, 0, club["FTHG"][i], club["FTAG"][i], 1]
                    elif club["FTHG"][i] == club["FTAG"][i] == 0:
                        row[f"{i+1}"] = [0, 1, 0, club["FTHG"][i], club["FTAG"][i], 1]
                    else:
                        row[f"{i+1}"] = [0, 0, 1, club["FTHG"][i], club["FTAG"][i], 0]
                else:
                    if club["FTHG"][i] > club["FTAG"][i] and club["FTAG"][i] == 0:
                        row[f"{i+1}"] = [row[str(i)][0]+1, row[str(i)][1], row[str(i)][2], row[str(i)][3]+club["FTHG"][i], row[str(i)][4]+club["FTAG"][i], row[str(i)][5]+1]
                    elif club["FTHG"][i] == club["FTAG"][i] == 0:
                        row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1]+1, row[str(i)][2], row[str(i)][3]+club["FTHG"][i], row[str(i)][4]+club["FTAG"][i], row[str(i)][5]+1]
                    else:
                        row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1], row[str(i)][2]+1, row[str(i)][3]+club["FTHG"][i], row[str(i)][4]+club["FTAG"][i], row[str(i)][5]]
                        
            for i in club.index[19:]:

                if club["FTHG"][i] < club["FTAG"][i] and club["FTHG"][i] == 0:
                        row[f"{i+1}"] = [row[str(i)][0]+1, row[str(i)][1], row[str(i)][2], row[str(i)][4]+club["FTAG"][i], row[str(i)][3]+club["FTHG"][i], row[str(i)][5]+1]
                elif club["FTHG"][i] == club["FTAG"][i] == 0:
                    row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1]+1, row[str(i)][2], row[str(i)][4]+club["FTAG"][i], row[str(i)][3]+club["FTHG"][i], row[str(i)][5]+1]
                else:
                    row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1], row[str(i)][2]+1, row[str(i)][4]+club["FTAG"][i], row[str(i)][3]+club["FTHG"][i], row[str(i)][5]]
                        
            # Calculating the Total Points.
            tp = row["38"]
            tp = tp[0]*3 + tp[1]
            for gw in row:
                row[gw].append(tp)
                
            Rows[c] = row
            
        return Rows


    @staticmethod
    def add(path, season):
        '''For Appending New Dataset to the Mother Data'''
        s = pd.read_csv(path)
        CLUBS = s["HomeTeam"]
        CLUBS = np.unique(CLUBS)
        Rows = {}
        for c in CLUBS:
            club = pd.concat([s.loc[s["HomeTeam"] == c], s.loc[s["AwayTeam"] == c]], ignore_index=True)
            row = {}
            for i in club.index[:19]:
                if len(row) == 0:
                    if club["FTHG"][i] > club["FTAG"][i] and club["FTAG"][i] ==0:
                        row[f"{i+1}"] = [1, 0, 0, club["FTHG"][i], club["FTAG"][i], 1]
                    elif club["FTHG"][i] == club["FTAG"][i] == 0:
                        row[f"{i+1}"] = [0, 1, 0, club["FTHG"][i], club["FTAG"][i], 1]
                    else:
                        row[f"{i+1}"] = [0, 0, 1, club["FTHG"][i], club["FTAG"][i], 0]
                else:
                    if club["FTHG"][i] > club["FTAG"][i] and club["FTAG"][i] == 0:
                        row[f"{i+1}"] = [row[str(i)][0]+1, row[str(i)][1], row[str(i)][2], row[str(i)][3]+club["FTHG"][i], row[str(i)][4]+club["FTAG"][i], row[str(i)][5]+1]
                    elif club["FTHG"][i] == club["FTAG"][i] == 0:
                        row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1]+1, row[str(i)][2], row[str(i)][3]+club["FTHG"][i], row[str(i)][4]+club["FTAG"][i], row[str(i)][5]+1]
                    else:
                        row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1], row[str(i)][2]+1, row[str(i)][3]+club["FTHG"][i], row[str(i)][4]+club["FTAG"][i], row[str(i)][5]]
                        
            for i in club.index[19:]:

                if club["FTHG"][i] < club["FTAG"][i] and club["FTHG"][i] == 0:
                        row[f"{i+1}"] = [row[str(i)][0]+1, row[str(i)][1], row[str(i)][2], row[str(i)][4]+club["FTAG"][i], row[str(i)][3]+club["FTHG"][i], row[str(i)][5]+1]
                elif club["FTHG"][i] == club["FTAG"][i] == 0:
                    row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1]+1, row[str(i)][2], row[str(i)][4]+club["FTAG"][i], row[str(i)][3]+club["FTHG"][i], row[str(i)][5]+1]
                else:
                    row[f"{i+1}"] = [row[str(i)][0], row[str(i)][1], row[str(i)][2]+1, row[str(i)][4]+club["FTAG"][i], row[str(i)][3]+club["FTHG"][i], row[str(i)][5]]
                        
            # Calculating the Total Points.
            tp = row["38"]
            tp = tp[0]*3 + tp[1]
            for gw in row:
                row[gw].append(tp)
                
            Rows[c] = row
            for r in Rows[c]:
                Rows[r] = Rows[r][13:]

        frame = pd.DataFrame(Rows)
        # Creating new dir and save each dataframe in csv file
        import os

        MODIFIED_PATH = "./modified-data"
        if not os.path.exists(MODIFIED_PATH):
            os.mkdir(MODIFIED_PATH)
            
        with open(os.path.join(MODIFIED_PATH, "Seasons.txt"), "a") as f:
            frame.to_csv(os.path.join(MODIFIED_PATH, f"{season}.csv"))
            f.write(f"{season}.csv")

