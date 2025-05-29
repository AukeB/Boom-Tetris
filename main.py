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
- O-piece detection -> Create mapping after tetris piece creation           
    with an integer mapping to the ALL_POLYOMINOS variable. Afterwards,
    implement no ration with the O-piece.


    Hiermee beginnnen, lineair tranformatie op de coordinates van 
    de tetris blocks toepassen werkt, maar vergeten dat de longbar, squiggly
    en reverse squiggly maar twee verschillende rotatie posities hebben, mijn methode
    zal er altijd 4 genereren. Het is wel valid, maar niet volgens het juiste rotatie
    systeem. Waarschijnlijk beste om rotatie posities handmatig te definieren.

    Class van polyomino/utils.py maken
- Blok met tijd om laag laten vallen
- DAS implementeren
"""