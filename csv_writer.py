import json


class PlayerError(Exception):
    pass


def validate_player(player_id: int) -> bool:
    """
    Confirms if player at <player_id> has at least one pokemon
    """
    # Open JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Add players to JSON
    for player in data['players']:
        if player['id'] == player_id and len(player['party']) > 0:
            return True
    return False


def add_player(player_id: int) -> None:
    """
    Adds player to the JSON

    Precondition:
    - winner_id and loser_id exists
    """
    # Open JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Add players to JSON
    data['players'].append({"id": player_id, "stats": {}, "party": []})

    # Update the JSON file
    with open("data.json", "w") as file:
        json.dump(data, file)


def add_match(winner_id: int, loser_id: int) -> None:
    """
    Adds match to the JSON

    Precondition:
    - winner_id and loser_id exists
    """
    # Open JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Append match to match history
    if data['matches']:
        # If a match already exists append it to match history
        data['matches'].append({"id": data['matches'][-1]['id'] + 1, "winner": winner_id, "loser": loser_id})
    else:
        # First match, then append it to match history
        data['matches'].append({"id": 1, "winner": winner_id, "loser": loser_id})

    # Change number of games winners have won
    for player in data['players']:
        if player['id'] == winner_id:
            if player['stats']['won'] is None:
                player['stats']['won'] = 0
            player['stats']['won'] += 1
            break

    # Update the JSON file
    with open("data.json", "w") as file:
        json.dump(data, file)


def add_poke(player_id: int, poke_id: int, poke_moves: list[str] = None) -> None:
    """
    Add Pokemon with <poke_id> to a <player>'s party

    Precondition:
    - player and poke_id are both valid
    - player has greater than or equal to 0 pokemon and less than 6 pokemon
    """
    # Open JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Add pokemon to player's pokemon
    for player in data['players']:
        if player['id'] == player_id:
            player['party'].append({"id": poke_id, "moves": poke_moves})

    # Update the JSON file
    with open("data.json", "w") as file:
        json.dump(data, file)


def get_pokes(player_id: int) -> list[dict]:
    """
    Get pokemon in the party of a given <player_id>

    Preconditions:
    - player_id is valid
    """
    # Open JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Return player's party
    for player in data['players']:
        if player['id'] == player_id:
            return player['party']
    return None


def clear_pokes(player_id: int) -> None:
    """
    Clear the party for a given <player_id>

    Preconditions:
    - player_id is valid
    """
    # Open JSON file
    with open('data.json', 'r') as file:
        data = json.load(file)

    # Flag for if player is found
    found = False

    # Reset the party
    for player in data['players']:
        if player['id'] == player_id:
            player['party'] = []
            found = True
            break

    # If player is not found
    if not found:
        raise PlayerError

    # Update the JSON file
    with open("data.json", "w") as file:
        json.dump(data, file)

# add_match(1, 2)
# add_poke(1, 1, ["Return", "Return", "Return", "Return"])

