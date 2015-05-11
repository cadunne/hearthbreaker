import json
import logging
from hearthbreaker.agents.basic_agents import RandomAgent
from hearthbreaker.agents.aggressive_agent import AggressiveAgent
from hearthbreaker.agents.control_agent import ControlAgent
from hearthbreaker.agents.tempo_agent import TempoAgent
from hearthbreaker.cards.heroes import hero_for_class
from hearthbreaker.constants import CHARACTER_CLASS
from hearthbreaker.engine import Game, Deck, card_lookup
from hearthbreaker.cards import *
import timeit


def load_deck(filename):
    cards = []
    character_class = CHARACTER_CLASS.MAGE

    with open(filename, "r") as deck_file:
        contents = deck_file.read()
        items = contents.splitlines()
        for line in items[0:]:
            parts = line.split(" ", 1)
            count = int(parts[0])
            for i in range(0, count):
                card = card_lookup(parts[1])
                if card.character_class != CHARACTER_CLASS.ALL:
                    character_class = card.character_class
                cards.append(card)

    if len(cards) > 30:
        pass

    return Deck(cards, hero_for_class(character_class))


def do_stuff(agent1, agent2, d1, d2):
    _count = 0
    lwins = 0
    rwins = 0
    

    def play_game():
        nonlocal _count
        nonlocal lwins
        nonlocal rwins
        _count += 1
        
        new_game = game.copy()
        try:

            new_game.start()

            lwins += (new_game.players[0].hero.health != 0)
            rwins += (new_game.players[1].hero.health != 0)

        except Exception as e:
            print(json.dumps(new_game.__to_json__(), default=lambda o: o.__to_json__()))
            print(new_game._all_cards_played)
            raise e

        del new_game

        if _count % 50 == 0:
            print("---- game #{} ----".format(_count))
            print("lwins: " + str(lwins) + ", rwins: "+ str(rwins))


    
    deck1 = load_deck(d1)
    deck2 = load_deck(d2)
    game = Game([deck1, deck2], [agent1, agent2])

    print(timeit.timeit(play_game, 'gc.enable()', number=5))

    returnString = str(type(game.players[0].agent)) + " with deck " + d1 + ": " + str(lwins) + " wins"
    returnString += '\n\t' + str(type(game.players[1].agent)) + " with deck " + d2 + ": " + str(rwins) + " wins"
    if rwins != 0:
        returnString += '\n\t ratio: ' + str(lwins/rwins)
    
    return returnString

if __name__ == "__main__":
    rd = "rampDruid.hsdeck"
    vm = "valueMage.hsdeck"
    bh = "beastHunter.hsdeck"


    logstring = do_stuff(TempoAgent(), ControlAgent(), rd, rd)


    ra = RandomAgent()
    ta = TempoAgent()
    ca = ControlAgent()
    aa = AggressiveAgent()

    agentList = [ra, ta, ca, aa]

    LOG_FILENAME = 'match_results.log'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG, filemode = 'w')

    for x in range(0, 4):

        ra = RandomAgent()
        ta = TempoAgent()
        ca = ControlAgent()
        aa = AggressiveAgent()

        agentList = [ra, ta, ca, aa]

        a1 = agentList[x]
        a2 = agentList[0]

        logstring = do_stuff(a1, a2, rd, rd)
        logging.debug(logstring)

        logstring = do_stuff(a1, a2, rd, vm)
        logging.debug(logstring)

        logstring = do_stuff(a1, a2, vm, rd)
        logging.debug(logstring)

        logstring = do_stuff(a1, a2, vm, vm)
        logging.debug(logstring)














