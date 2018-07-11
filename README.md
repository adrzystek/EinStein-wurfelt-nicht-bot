# EinStein-wurfelt-nicht-bot
A simple algorithm based on the Monte Carlo simulation playing *EinStein würfelt nicht!* game.

## Overview

### The game
*EinStein würfelt nicht!* is a strategy board game. Unlike most other games of this type, EWN gameplay is not deterministic; by rolling a dice, the random element is introduced. More about the game can be found for instance on [its Wikipedia page](https://en.wikipedia.org/wiki/EinStein_w%C3%BCrfelt_nicht!).

### Setting
Probably the largest *EinStein würfelt nicht!* online community might be found at the [Little Golem](https://littlegolem.net/jsp/main/) game server. This server allows only for a correspondence gameplay, i.e., each player's turn may take up to several hours.

### Goal
The aim of this project was to create a fully automatized bot capable of playing the EWN game at a decent level.

### Monte Carlo method
The Monte Carlo method is an approach to problem solving by multiply repeating the experiment; the problem - which itself might be deterministic or not - is tackled lots of times where each time includes some randomness. When the number of simulations is big enough then surprisingly accurate conclusions may be drawn. For more info please see its [Wiki page](https://en.wikipedia.org/wiki/Monte_Carlo_method).

### Solution architecture
The Amazon Web Services cloud was used, namely two its components - Amazon EC2 and AWS Lambda. One EC2 instance was rented where every 10 minutes it is checked whether there is a game to make a move. If it is found, then the EC2 instance triggers Lambda function (with game id as an argument) which renders the board, makes the simulations (i.e., plays 10k games with more or less random moves from the given point of the game and checks which move leads to the greatest numbers of wins) and finally plays the best move.

### Results
After three months of playing (without any human intervention, apart from initial tournaments registration), having played over 100 games, with 50% win ratio, the bot managed to get into top 20% of players at the LG server (much higher than its creator ;) ). His profile and played games may be seen [here](https://littlegolem.net/jsp/info/player.jsp?plid=70514).

## Codes description
* **classes.py** - script with two classes definitions: Player and Board
* **functions.py** - auxiliary funtions used for games extracting, board parsing, determining the best move (here the Monte Carlo simulation takes place) and sending it to the server (i.e., playing it)
* **lambda_function.py** - a handler (function) for AWS Lambda service
* **main_ec2.py** - a script for Amazon EC2 *controlling* instance

One file (**credentials.py**, imported in the last two scripts) is missing, for obvious reasons.
