# PUBG-API-Wrapper-Python
Small wrapper written in Python, which simplifies querying the PUBG API. 

# Pre-Requisites and Usage of CLI version of the application:
1. Make sure to fill out:
   - A valid PUBG Developer `API_TOKEN` - Located in `config/APISettings.py`
   - A valid PUBG Username for `PLAYER_NAME` - Located in `user_settings.py`
   - A valid platform for `PLAYER_PLATFORM` - Located in `user_settings.py`
   - A valid game-mode for `PLAYER_GAME_MODE` - Located in `user_settings.py`
   - A valid integer for `MATCH_INTEGER` - Located in `user_settings.py
   - A valid season per respective platform for `SEASON_VAL` - Located in `user_settings.py`

2. Executing user_input.py will give you a simple menu in the console, and will ask you to choose out of three different options.
   - 1: Lifetime Stats
   - 2: Season Stats
   - 3: Stats over a number of matches.

Other than the Pre-Requisites mentioned above, the user has to do nothing else,
as all the nitty-gritty API calls etc. are abstracted away, for simplicty.

## Usage of CLI version of the application without user_input.py
Include the following in your script
```Python
from api_interface import API_INTERFACE
from helper.helperFunctions import regionCheck
from config.APIConfig import APIConfig
from config.APISettings import APISetting
from config import user_settings
```

Having done that, it's pretty simple from here on out.
```Python
## Sets up authentication header
 _HEADER = APIConfig(APISettings.API_TOKEN.value).setupAuth()

## Pulls lifetime stats for a user.
API_INTERFACE.lifetimeStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, _HEADER, user_settings.PLAYER_GAME_MODE)

## Checks the season you chose doesn't need a Region shard, then retrieves user-stats for that season
regionCheck(user_settings.SEASON_VAL) ## Check if the season needs a Region shard or not
API_INTERFACE.seasonStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, _HEADER, user_settings.PLAYER_GAME_MODE, user_settings.SEASON_VAL)

## Pulls defined amount of matchges from the API for a specific user.
API_INTERFACE.matchStats(user_settings.PLAYER_NAME, user_settings.PLAYER_PLATFORM, _HEADER, user_settings.MATCH_INTEGER)
```
 
# Using GUI version of the application:
1. Make sure `GUI` is set to `True` within `config/user_settings.py` 
   [optional] If you want to pre-load settings, fill out the following:
      - A valid PUBG Developer `API_TOKEN` - Located in `config/APISettings.py`
      - A valid PUBG Username for `PLAYER_NAME` - Located in `user_settings.py`
      - A valid integer for `MATCH_INTEGER` - Located in `user_settings.py`
2. Executing `api_interface` will launch the GUI, which looks like below:

![GUI](https://i.imgur.com/2I2aXUR.png)

3. Play around with the settings
4. Any data this produces will be dumped to `DATA/`, and will be named appropriately.
