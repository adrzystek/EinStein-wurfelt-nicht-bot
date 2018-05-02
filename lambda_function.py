from credentials import COOKIE, USERNAME
from functions import get_board_and_dice_and_color, select_best_move, parse_moves_coords, send_a_move
from classes import Player

def lambda_handler(event, context):
    game_id = event['gid']
    board, dice, color = get_board_and_dice_and_color(game_id, USERNAME)
    player1 = Player(color)
    player2 = Player('blue' if color == 'red' else 'red')
    piece, position, win_probability = select_best_move(board, dice, player1, player2)
    coords = parse_moves_coords(board, piece, position)
    send_a_move(game_id, coords, COOKIE, {'message': round(win_probability, 2)})
