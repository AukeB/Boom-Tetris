""" """

from src.boom_tetris.config.config import Config
from src.boom_tetris.constants import MAIN_CONFIG_RELATIVE_FILE_PATH


def main() -> None:
    """ """
    config_main = Config.load_config(file_path=MAIN_CONFIG_RELATIVE_FILE_PATH)

    config_instance = Config(config_path=MAIN_CONFIG_RELATIVE_FILE_PATH)
    config_augmented = config_instance.augment_config(config=config_main)

    # The 'Game' class can only be imported after the `augment_config` from
    # the 'Config' class has been executed, because it generates a .yaml
    # file that is immediatly loaded.
    from src.boom_tetris.game import Game

    game = Game(config=config_augmented)

    while game.update():
        pass


if __name__ == "__main__":
    main()


"""
Todo:

- Directions naar config (inclusief up, down, up, down)                     DONE
- Reverse all y,x coordinates back to x,y                                   DONE
- Replace yaml with more elaborate yaml package                             DONE
- Class van polyomino/utils.py maken genaamd PolynomioTransformer           DONE
    Bedoeld voor postprocessing de polyomino's na de generation             DONE
- Fix all rotaties voor tetromino's                                         DONE
    Inclusief geen rotatie voor O-piece                                     DONE
    En manually defined rotations voor I, Z and S-piece.                    DONE
- Fixen Pydantic parameters meegeven die niet in BaseModel staat            DONE
- Board size computen gebaseerd op window size                              DONE
- Implement grid_lines                                                      DONE
- rotate en shift functies zijn geschreven, nu implementeren voor alle
    tetrominos. Nog even kijken hoe te implementeren als de lineaire shift
    die ervoor zorgt dat een blok in het midden van het board spawnt, maar
    dan nog niet de rotatie goed gaat (voor 3 van de 7 pieces), hoe dit dan 
    op te lossen, waarschijnlijk door de spawn positie iets te verschuiven
    en dan alle andere coordinate van de blokken van de tetromino evenver
    naar de andere kant verschuiven.
- Nog ene keer PolyominoTranformer class doorlopen
    Coordinate, coordinates, all_coordinates betere namen geven
    Nog een keer tuple vs lists analyseren (misschien in readme zetten)
    Block namedtuple uit code halen                                         DONE
- Maak board 22 hoog ipv 20
    Hidden rows toevoegen                                                   DONE
    Nadenken over hoe dit precies in code te zetten                         
    Issue fixen met kleine ruimte over als board_size 30 rows heeft
- New line toevoegen met ruamel package na elke level1 dict item              


    
- MyPy toevoegen
    - Template repo updaten
- Fix spawn positities polyomino's
- Blok met tijd om laag laten vallen
- DAS implementeren

Backlog:

- Ook pentomino mapping maken op dezelfde manier is tetromino mapping       
"""