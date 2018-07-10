# EinStein-wurfelt-nicht-bot
A simple algorithm based on the Monte Carlo simulation playing *EinStein würfelt nicht!* game.

## Overview
### The game
*EinStein würfelt nicht!* is a strategy board game. Unlike most other games of this type, EWN gameplay is not deterministic; by rolling a dice, the random element is introduced. More about the game can be found for instance on [its Wikipedia page](https://en.wikipedia.org/wiki/EinStein_w%C3%BCrfelt_nicht!).

### Setting
Probably the largest *EinStein würfelt nicht!* online community might be found at the [Little Golem](https://littlegolem.net/jsp/main/) game server. This server allows only for correspondence gameplay, i.e., each player's turn may take up to several hours.

### Monte Carlo method
The Monte Carlo method is an approach to problem solving by multiply repeating the experiment; the problem - which itself might be deterministic or not - is tackled lots of times where each time includes some randomness. When the number of simulations is big enough then surprisingly accurate conclusions may be drawn. For more info please see its [Wiki page](https://en.wikipedia.org/wiki/Monte_Carlo_method).

### Solution

### Architecture

## Codes description

* **classes.py** - script with two classes definitions: Player and Board
* **functions.py** - auxiliary funtions used for games extracting, board parsing, determining the best move (here the Monte Carlo simulation takes place) and sending it to the server (i.e., playing it)
* **lambda_function.py** - a handler (function) for AWS Lambda service
* **main_ec2.py** - a script for Amazon EC2 *controlling* instance

One file (**credentials.py**, imported in the last two scripts) is missing, due to the obvious reasons.
