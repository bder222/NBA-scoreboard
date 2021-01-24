# NBA-scoreboard
## NBA LED Scoreboard
Displays NBA scores for the day on an LED board. Driven by a raspberry pi and currently only supports 32x64 boards.

### Current Functionality
Scrolls through all NBA games for the day. New days begin on the first update after 12pm ET.

### Game Data
Game data is pulled from the NBA's CDN link. This link provides live game data for all games of the current day. The link returns data in JSON format. During live games, game data is updated every 2 minutes. 

### Usage

`sudo crontab -e`
