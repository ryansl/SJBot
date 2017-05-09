# SJBot

This is an automated bot for StarJeweled (Bejeweled minigame in Starcraft) that can outperform the top players. Even the best human players can only achieve around 3000-3500 EPM, whereas this bot can consistently achieve 4500 EPM in an average game (as long as you don't lag too much and have decent framerate).

In order to build the project, you will need to `pip install autopy` and `pip install pyscreenshot` as the program relies on those two libraries. The bot works by periodically taking screenshots of the board and then using the average of the RGB values to accurately determine the color of each gem. It then looks for potential matches and calculates a score for each match based on the chain length, number of moves created, and several other metrics. It then determines the best subset of matches that do not conflict with each other and executes those.

If you want to use this, you will first have to re-calibrate the colors and screen positioning if you're not already on 1920x1080 screen resolution with texture quality set to high. That's what I calibrated everything to when running it on my computer. If you do need to do this, you can adjust the values accordingly in the configuration file.
