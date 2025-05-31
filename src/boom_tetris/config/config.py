""" """

from ruamel.yaml import YAML

from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.polyomino.polyomino_generator import PolyominoGenerator
from src.boom_tetris.utils.dict_utils import DotDict, format_for_writing_to_yaml_file
from src.boom_tetris.constants import MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH, Position

yaml = YAML()
yaml.indent(mapping=2, sequence=4, offset=2)


class Config:
    """ """

    def __init__(self, config_path: str) -> None:
        self.config_path = config_path

    def load_config(
        file_path: str, validate: bool = True, file_type: str = "yaml"
    ) -> ConfigModel | DotDict:
        """ """
        if file_type == "yaml":
            with open(file_path) as file:
                config = yaml.load(file)

            if validate:
                config = ConfigModel(**config)
            else:
                config = DotDict(config)

        return config

    def _add_computational_parameters(self, config: DotDict) -> DotDict:
        """
        Computations:

        - Total number of rows on board, there are a couple of hidden
            rows to make sure pieces can rotate right at the spawn
            location.
        - Board size (left, top, width, height), based on the window
            size (width, height and margin).
        - Cell width and height, based on the board width and height and
            the number of cells the board consists of (default values
            are 20 rows and 10 columns).
        """

        # Computations.
        rows_total = config.BOARD.DIMENSIONS.ROWS + config.BOARD.DIMENSIONS.ROWS_HIDDEN

        window_horizontal_mid = config.WINDOW.WIDTH / 2
        board_height = config.WINDOW.HEIGHT - (2 * config.WINDOW.MARGIN)
        board_width = board_height * (config.BOARD.DIMENSIONS.COLS / rows_total)
        board_left = window_horizontal_mid - board_width / 2
        board_top = config.WINDOW.MARGIN

        cell_width = board_width / config.BOARD.DIMENSIONS.COLS
        cell_height = board_height / rows_total

        # Adding computed parameters back to config.
        config.BOARD.DIMENSIONS.ROWS_TOTAL = rows_total

        config.BOARD.RECT = {
            "LEFT": board_left,
            "TOP": board_top,
            "WIDTH": board_width,
            "HEIGHT": board_height,
        }

        config.BOARD.CELL = {"WIDTH": cell_width, "HEIGHT": cell_height}

        return config

    def _add_all_polyonomios(self, config: DotDict) -> DotDict:
        """ """
        # Exclude `rotations` from `directions`.
        directions = {
            key: value
            for key, value in config.DIRECTIONS.items()
            if isinstance(value, list)
        }

        polyomino_generator = PolyominoGenerator(
            number_of_polyomino_cells=config.POLYOMINO.SIZE, directions=directions
        )

        unique_coordinates = polyomino_generator.generate()

        config.POLYOMINO.ALL_SHAPES = [
            [[x, y] for (x, y) in shape] for shape in unique_coordinates
        ]

        return config

    def _change_data_types(self, config: ConfigModel) -> ConfigModel:
        """ """
        new_directions = config.DIRECTIONS.model_copy(
            update={
                "UP": Position(*config.DIRECTIONS.UP),
                "DOWN": Position(*config.DIRECTIONS.DOWN),
                "LEFT": Position(*config.DIRECTIONS.LEFT),
                "RIGHT": Position(*config.DIRECTIONS.RIGHT),
            }
        )

        config = config.model_copy(update={"DIRECTIONS": new_directions})

        return config

    def _write_config(self, file_path: str, config: DotDict) -> None:
        """ """
        config_dict = config.to_dict()
        config_dict_formatted = format_for_writing_to_yaml_file(obj=config_dict)

        with open(file_path, "w") as file:
            yaml.dump(config_dict_formatted, file)

    def augment_config(self, config) -> ConfigModel:
        """ """
        # Convert from Pydantic Basemodel to dictionary and then to DotDict
        # instance, to keep using dot notation for dictionary keys and values.
        config = DotDict(config.model_dump())

        augmented_config: DotDict = self._add_computational_parameters(config=config)
        augmented_config: DotDict = self._add_all_polyonomios(config=config)

        self._write_config(
            file_path=MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH, config=augmented_config
        )

        augmented_config: ConfigModel = Config.load_config(
            file_path=MAIN_CONFIG_AUGMENTED_RELATIVE_FILE_PATH
        )

        augmented_config: ConfigModel = self._change_data_types(config=augmented_config)

        return augmented_config
