from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import os
import json
import datetime as dt
import time
import sys

class Render:
    def __init__(self):
        #self.options = RGBMatrixOptions()
        #self.options.hardware_mapping = 'adafruit-hat'
        #self.options.gpio_slowdown = 3
        self.options.rows = 32
        self.options.cols = 64
        self.options.drop_privileges = False
        
        
        self.path = '/home/pi/NBA-scoreboard/'
        
        self.font = graphics.Font()
        self.font.LoadFont("/home/pi/NBA-scoreboard/rpi-rgb-led-matrix/fonts/6x12.bdf")
        self.font2 = graphics.Font()
        self.font2.LoadFont("/home/pi/NBA-scoreboard/rpi-rgb-led-matrix/fonts/4x6.bdf")
        self.team_colors = {'ATL': [[225, 58, 62], [100, 100, 100]], 'BOS': [[0, 131, 72], [187, 151, 83]], 'BKN': [[100, 100, 100], [0, 0, 0]], 'CHA': [[29, 17, 96], [0, 140, 168]], 'CHI': [[206, 17, 65], [0, 0, 0]], 'CLE': [[134, 0, 56], [253, 187, 48]], 'DAL': [[0, 125, 197], [196, 206, 211]], 'DEN': [[77, 144, 205], [253, 185, 39]], 'DET': [[237, 23, 76], [0, 107, 182]], 'GSW': [[253, 185, 39], [0, 107, 182]], 'HOU': [[206, 17, 65], [196, 206, 211]], 'LAL': [[253, 185, 39], [85, 37, 130]], 'MEM': [[15, 88, 108], [190, 212, 233]], 'MIA': [[152, 0, 46], [0, 0, 0]], 'MIL': [[0, 71, 27], [240, 235, 210]], 'MIN': [[0, 80, 131], [0, 169, 79]], 'NOP': [[0, 43, 92], [227, 24, 55]], 'NYK': [[0, 107, 182], [245, 132, 38]], 'OKC': [[0, 125, 195], [240, 81, 51]], 'ORL': [[0, 125, 197], [0, 0, 0]], 'PHI': [[237, 23, 76], [0, 107, 182]], 'PHX': [[229, 96, 32], [29, 17, 96]], 'POR': [[224, 58, 62], [186, 195, 201]], 'SAC': [[114, 76, 159], [142, 144, 144]], 'SAS': [[186, 195, 201], [0, 0, 0]], 'TOR': [[206, 17, 65], [0, 0, 0]], 'UTA': [[0, 43, 92], [249, 160, 27]], 'WAS': [[0, 43, 92], [227, 24, 55]], 'IND': [[255, 198, 51], [0, 39, 93]], 'LAC': [[237, 23, 76], [0, 107, 182]]}
            
    def Render_Games(self, printer=False):
        matrix = RGBMatrix(options=self.options)
        date_range = []
        
        for day in os.listdir(self.path):
            if day=='.DS_Store':
                continue
            if day == 'DataToday.json':
                with open(self.path + day) as file:
                    game_data = json.load(file)
        try:
            with open(self.path + 'NBASpreads.json', 'r') as file:
                spreads_data = json.load(file)
                
        except:
            print('Error loading spreads data.')
            spreads_data = {}
        
        canvas = matrix.CreateFrameCanvas()
        
        for game in game_data:
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
            
            
            if game['gameStatus'] != 1:
                homescore = game['homeTeam']['score']
                awayscore = game['awayTeam']['score']
                graphics.DrawText(canvas, self.font, 21, 8, graphics.Color(100, 100, 100), str(awayscore))
                graphics.DrawText(canvas, self.font, 21, 18, graphics.Color(100, 100, 100), str(homescore))
                graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), game['gameStatusText'])
            else:
                if game['gameStatusText'] != 'PPD':
                    graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), game['gameStatusText'][0:len(game['gameStatusText']) - 3])
                if game['gameStatusText'] == 'PPD':
                    graphics.DrawText(canvas, self.font, 1, 27, graphics.Color(100, 100, 100), 'Postponed')
            canvas = matrix.SwapOnVSync(canvas)
            time.sleep(6)
            
if __name__=='__main__':
    while True:
        Render().Render_Games()
        
#/basketball/nba/new-orleans-pelicans-los-angeles-clippers-20210113
