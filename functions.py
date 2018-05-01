import re
import urllib.request

from bs4 import BeautifulSoup
import numpy as np
import requests

from classes import Board


def get_games_list(cookie, game='einstein'):
    
    r = requests.get('https://littlegolem.net/jsp/game/index.jsp', cookies=cookie)
    
    soup = BeautifulSoup(r.text, 'lxml')
    
    div_tag = soup.find_all('div', class_ = 'portlet box blue-madison')
    
    tr_tags = div_tag[0].find_all('tr')
    
    games = []
    for tr_tag in tr_tags:
        if re.findall(game, str(tr_tag), flags=re.I):
            games.append(re.findall('gid=(.*)"', str(tr_tag))[0])
            
    return games
    

def get_board_and_dice_and_color(gid, my_username):

    url = 'https://littlegolem.net/jsp/game/game.jsp?gid={}'.format(gid)
    
    html = urllib.request.urlopen(url).read()
    
    soup = BeautifulSoup(html, 'lxml')
    
    dice = int(re.findall('src="/ng/images/source/soccer/die(.?).gif"', str(soup.find_all('img')))[0])
    
    fields = re.findall('src="/ng/images/source/(.*?)"', str(soup.find_all('td')))
    
    board = np.zeros((5, 5))
    
    for i, field in enumerate(fields):
        _field = field.replace('.png', '').replace('.gif', '').replace('einstein/', '')
        if _field[0] == 'r':
            _field = int(_field[-1]) * (-1)
        elif _field[0] == 'b':
            _field = int(_field[-1])
        row = i // 5
        col = i % 5
        board[(row, col)] = _field
    
    div_tags = soup.find_all('div', class_ = 'portlet box yellow')
    
    for div_tag in div_tags:
        if re.findall(my_username, str(div_tag)):
            color = re.findall('Player -\s*(.*?)</div>', str(div_tag))[0].lower()
    
    return board, dice, color


def parse_moves_coords(board, piece, coords_new):
    _, pieces_position = Board(given_board=board).initialize()
    coords_until_now = pieces_position[piece]
    _str = ''
    _str += chr(-coords_until_now[1] + 101)
    _str += chr(-coords_until_now[0] + 101)
    _str += chr(-coords_new[1] + 101)
    _str += chr(-coords_new[0] + 101)
    return _str
    
    
def send_a_move(gid, coords, cookie, payload={'message': ''}):
    r = requests.post('https://littlegolem.net/jsp/game/game.jsp?sendgame={}&sendmove={}'.format(gid, coords), cookies=cookie, data=payload)
    return r
    

def select_best_move(board, dice, player_main, player_opponent, n_iter=10000):
    _moves_and_games_cnt, _moves_and_wins_cnt = {}, {}
    for i in range(n_iter):
        _board, pieces_position = Board(given_board=board).initialize()
        piece, new_position = player_main.choose_piece_and_position(pieces_position, _board, given_dice=dice)
        _moves_and_games_cnt[(piece, new_position)] = _moves_and_games_cnt.get((piece, new_position), 0) + 1
        player_main.play(_board, pieces_position, given_piece_and_position=(piece, new_position))
        while True:
            if player_main.won:
                _moves_and_wins_cnt[(piece, new_position)] = _moves_and_wins_cnt.get((piece, new_position), 0) + 1
                break
            player_opponent.play(_board, pieces_position)
            if player_opponent.won:
                break
            player_main.play(_board, pieces_position)
        player_main.won, player_opponent.won = False, False
    try:
        _moves_and_probabilities_of_win = {}
        for k, v in _moves_and_wins_cnt.items():
            probability = v / _moves_and_games_cnt[k]
            _moves_and_probabilities_of_win[k] = probability
        (best_piece, best_position), win_probability = sorted(_moves_and_probabilities_of_win.items(), key = lambda x: x[1], reverse=True)[0]
    except:
        best_piece, best_position, win_probability = piece, new_position, 0
    return (best_piece, best_position, win_probability)