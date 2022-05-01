import pokebase as pb
import asyncio


def create_lists() -> list:
    # Fetch all pokemon information for generation 1
    gen_resource = pb.generation(1)

    poke_list = []

    # builds list from gen_resource
    for pokemon in gen_resource.pokemon_species:
        poke_list.append(pokemon)

    return poke_list


def check_pokemon(name: str, poke_list: list) -> int:
    # Initializes int for id
    poke_id = 0

    # Sets poke_id to the id of the desired pokemon
    for poke in poke_list:
        if poke.name == name.lower():
            poke_id = poke.id

    return poke_id


def add_move(p_id: int, move_str: str) -> bool:
    # Grabs pokemon via id
    poke, move = str(pb.pokemon(p_id)), pb.move(move_str.lower())

    # check if move exists
    try:
        move.pp
    except:
        return False

    # Checks if move is in generation 1
    if str(move.generation) != 'generation-i':
        return False
        # check if pokemon can learn move
    elif poke not in [mon.name for mon in move.learned_by_pokemon]:
        return False
    return True
