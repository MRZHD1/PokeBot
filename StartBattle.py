import pokebase as pb
import time

TYPES = ['normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug',
         'ghost', 'fire', 'water', 'grass', 'electric', 'psychic', 'ice', 'dragon']


def type_multiplier(attack: str, defense) -> float:
    """ return multiplier based on attack type and defense pokemon type
    """
    # Get API data for the attacking type.
    atk_type = pb.move(attack).type

    # Check which damage_relation list the defense is in. Matches by name
    if defense in [t.name for t in atk_type.damage_relations.no_damage_to]:
        return 0.0
    elif defense in [t.name for t in atk_type.damage_relations.half_damage_to]:
        return 0.5
    elif defense in [t.name for t in atk_type.damage_relations.double_damage_to]:
        return 2.0
    else:
        return 1.0


def get_multiplier(atk: str, poke) -> float:
    """ return raw attack amount
    """
    multi = 1.0
    for i in poke.types:
        multi *= type_multiplier(atk, i.type.name)
    return pb.move(atk).power * multi


def attack_value(atk, poke_atk, poke_def, p_dict):
    """ returns health to be deducted from defending pokemon
    """
    atk_stat = p_dict[poke_atk].stats[1].base_stat
    def_stat = p_dict[poke_def].stats[2].base_stat
    poke_def = p_dict[poke_def]
    numer = 22 * get_multiplier(atk, poke_def) * (atk_stat / def_stat)
    return round((numer / 50) + 2)


def health_value(health: int, atk, poke_atk, poke_def, p_dict) -> int:
    return health - attack_value(atk, poke_atk, poke_def, p_dict)