import json

import boto3

from credentials import COOKIE
from functions import get_games_list


client = boto3.client('lambda')

game_ids = get_games_list(COOKIE)

for game_id in game_ids:
    _payload = {'gid': game_id}
    client.invoke(FunctionName='EinSteinPlayer',
                  InvocationType='Event',
                  Payload=json.dumps(_payload))