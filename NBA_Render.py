from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys
from NBA_Standings import NBA_Standings
from dateutil import tz

class Render:
    def __init__(self):
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = 'adafruit-hat'
        self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False
        
        
        self.path = '/home/pi/NBA-scoreboard/'
        
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.team_colors = {'ATL': [[225, 58, 62], [100, 100, 100]], 'BOS': [[0, 131, 72], [187, 151, 83]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [142, 144, 144]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}
            
    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        date_range = []
        disp_live_odds = True
        try:
            for day in os.listdir(self.path):
                if day=='.DS_Store':
                    continue
                if day == 'DataToday.json':
                    with open(self.path + day) as file:
                        game_data = json.load(file)
                
        except:
            print('Error loading spreads data.')
            game_data = {}
        
        try:
            with open(self.path + 'NBASpreads.json', 'r') as file:
                spreads_data = json.load(file)
            with open(self.path + 'NBASpreadsLive.json', 'r') as file:
                spreads_data_live = json.load(file)
            with open(self.path + 'NBATopShot.json', 'r') as file:
                moments_value = json.load(file)
                
        except:
            print('Error loading spreads data.')
            spreads_data = {}
        
        canvas = matrix.CreateFrameCanvas()
        
        live_games = 0
        
        for game in game_data:
            if game['gameStatus'] == 2:
                live_games += 1
                
            hometeam = game['homeTeam']['teamTricode']
            awayteam = game['awayTeam']['teamTricode']
            
            home = (game['homeTeam']['teamCity'] + '-' + game['homeTeam']['teamName']).replace(' ', '-').lower()
            away = (game['awayTeam']['teamCity'] + '-' + game['awayTeam']['teamName']).replace(' ', '-').lower()
            if home == 'la-clippers':
                home = 'los-angeles-clippers'
            if away == 'la-clippers':
                away = 'los-angeles-clippers'
            
            gamelink = r'/basketball/nba/{0}-{1}-{2}'.format(away, home, game['gameCode'][0:game['gameCode'].find(r'/')])
            print(gamelink)

            try:
                if disp_live_odds == True and game['gameStatus'] == 2:
                    spread = spreads_data_live[gamelink]['spread']
                    over_under = spreads_data_live[gamelink]['over_under']
                else:
                    spread = spreads_data[gamelink]['spread']
                    over_under = spreads_data[gamelink]['over_under']
            except KeyError:
                #print('No spreads for this game.')
                spread = ''
                over_under = ''
            
            for line in range(0,32):
                graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(0, 0, 0))
            
            for line in range(10,19):
                graphics.DrawLine(canvas, 0, line, 18, line, graphics.Color(self.team_colors[hometeam][0][0], self.team_colors[hometeam][0][1], self.team_colors[hometeam][0][2]))
            for line in range(0,9):
                graphics.DrawLine(canvas, 0, line, 18, line, graphics.Color(self.team_colors[awayteam][0][0], self.team_colors[awayteam][0][1], self.team_colors[awayteam][0][2]))
            graphics.DrawText(canvas, self.font2, 64 - len(str(over_under))*4, 8, graphics.Color(0, 0, 200), over_under)
            graphics.DrawText(canvas, self.font2, 64 - len(str(spread))*4, 18, graphics.Color(0, 0, 200), spread)
            graphics.DrawText(canvas, self.font, 1, 18, graphics.Color(self.team_colors[hometeam][1][0], self.team_colors[hometeam][1][1], self.team_colors[hometeam][1][2]), hometeam)
            graphics.DrawText(canvas, self.font, 1, 8, graphics.Color(self.team_colors[awayteam][1][0], self.team_colors[awayteam][1][1], self.team_colors[awayteam][1][2]), awayteam)
            
            
            if game['gameStatus'] != 1: #run this if the game is live or is final
                homescore = game['homeTeam']['score']
                awayscore = game['awayTeam']['score']
                graphics.DrawText(canvas, self.font, 21, 8, graphics.Color(100, 100, 100), str(awayscore))
                graphics.DrawText(canvas, self.font, 21, 18, graphics.Color(100, 100, 100), str(homescore))
                graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), game['gameStatusText'])
            else:
                if game['gameStatusText'] != 'PPD':
                    from_zone = tz.tzutc()
                    to_zone = tz.tzlocal()
                    game_time_utc = dt.datetime.strptime(game['gameTimeUTC'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=from_zone)
                    game_time_local = game_time_utc.astimezone(to_zone).strftime('%I:%M %p')
                    #graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), game['gameStatusText'][0:game['gameStatusText'].find('ET')])
                    graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), game_time_local)
                if game['gameStatusText'] == 'PPD':
                    graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), 'Postponed')
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(6)
            
        return live_games
    def Render_Standings(self):
        try:
            with open(self.path + 'NBAStandings.json', 'r') as file:
                standings_data = json.load(file)
                
        except:
            print('Error loading standings data.')
            standings_data = {}
            
        matrix = RGBMatrix(options=self.options)
        
        canvas = matrix.CreateFrameCanvas()
        
        
            
        #Render teams from 1 to 15 in each conference
        for conf in ['eastern', 'western']:
            scroll_offset = 0
            for line in range(0,32):
                graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(0, 0, 0))
            while scroll_offset < 130:
                for line in range(0,32):
                    graphics.DrawLine(canvas, 0, line, 64, line, graphics.Color(0, 0, 0))
                for seed in range(1,16):
                    for team in standings_data[conf]:
                        if standings_data[conf][team]['seed'] == seed:
                            seed_team = team
                            for line in range((seed-1)*10 + 10 - scroll_offset,seed*10 - 1 + 10 - scroll_offset):
                                graphics.DrawLine(canvas, 13, line, 31, line, graphics.Color(self.team_colors[seed_team][0][0], self.team_colors[seed_team][0][1], self.team_colors[seed_team][0][2]))
                            graphics.DrawText(canvas, self.font, 14, seed*10 - 2 + 10 - scroll_offset, graphics.Color(self.team_colors[seed_team][1][0], self.team_colors[seed_team][1][1], self.team_colors[seed_team][1][2]), seed_team)
                            if seed < 10:
                                graphics.DrawText(canvas, self.font, 3, seed*10 - 2 + 10 - scroll_offset, graphics.Color(100, 100, 100), str(seed))
                            else:
                                graphics.DrawText(canvas, self.font, 0, seed*10 - 2 + 10 - scroll_offset, graphics.Color(100, 100, 100), str(seed))
                            graphics.DrawText(canvas, self.font, 34, seed*10 - 2 + 10 - scroll_offset, graphics.Color(100, 100, 100), str(standings_data[conf][seed_team]['wins']) + '-' + str(standings_data[conf][seed_team]['losses']))
                            graphics.DrawText(canvas, self.font, 21, 9 - scroll_offset, graphics.Color(100, 100, 100), conf[0:4].upper())
                canvas = matrix.SwapOnVSync(canvas)
                if scroll_offset == 0:
                    time.sleep(3.9)
                time.sleep(0.1)
                scroll_offset += 1
                
            time.sleep(4)
        return standings_data
                

        
if __name__=='__main__':
    live_prev = 0
    while True:
        live = Render().Render_Games()
        if live_prev - live > 0:
            NBA_Standings().Standings()
        if live == 0:
            Render().Render_Standings()
        live_prev = live + 0 
        
#/basketball/nba/new-orleans-pelicans-los-angeles-clippers-20210113

