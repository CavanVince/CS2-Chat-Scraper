# CS2-Chat-Scraper

## Installation
To install the CS2 bot:  
clone this repository to local  
`git clone https://github.com/CavanVince/CS2-Chat-Scraper.git`  
  
`cd ./CS2-Chat-Scraper`  
_(optional)_ `python -m venv .venv` -> _(windows)_ `source .\venv\Scripts\activate`  
`pip install -r requirements.txt`  

Create a `.env` file in the base project directory containing the following:
```
CONSOLE_FILE=C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\console.log
EXEC_FILE=C:\Program Files (x86)\Steam\steamapps\common\Counter-Strike Global Offensive\game\csgo\cfg\send_command.cfg
```
**NOTE**: Your path may differ, find where Counter-Strik Global Offensive is installed and copy the paths here.  


## Using the Bot  
#### Set CS2 Launch Configs
Right-click Counter-Strike 2 in your Steam Library -> _Properties..._ -> _General_ -> Launch Options  
Paste the following in the _Launch Options_ textbox:  
`-condebug -conclearlog +exec autoexec.cfg`  
  
Now we are ready to run the application:  
`python main.py`  

## Commands
```
!fortune | !fc | !fortune-cookie - Read out a player's fortune

!case  
      open <case name> - Open a case
      list - List possible cases to open
      balance - View the player's balance
      help - list help for the !case command

!roast <player> - Roast the player
```