""" """

import yaml


from src.boom_tetris.config.model import ConfigModel
from src.boom_tetris.polyomino.polyomino_generator import PolyominoGenerator
from src.boom_tetris.utils.dot_dict import DotDict
from src.boom_tetris.utils.yaml_dumper import FlowListDumper
from src.boom_tetris.constants import CONFIG_POLYOMINOS_RELATIVE_FILE_PATH


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
                config = yaml.load(file, Loader=yaml.FullLoader)

            if validate:
                config = ConfigModel(**config)
            else:
                config = DotDict(config)

        return config

    def _add_computational_parameters(self, config: ConfigModel) -> dict:
        """ """
        cell_width = config.BOARD.RECT.WIDTH // config.BOARD.DIMENSIONS.COLS
        cell_height = config.BOARD.RECT.HEIGHT // config.BOARD.DIMENSIONS.ROWS

        config.BOARD.CELL = {"WIDTH": cell_width, "HEIGHT": cell_height}

        return config

    def _add_all_polyonomios(self, config: ConfigModel) -> dict:
        """ """
        polyomino_generator = PolyominoGenerator(
            number_of_polyomino_cells=config.POLYOMINO.SIZE
        )

        unique_coordinates = polyomino_generator.generate()

        config.POLYOMINO.ALL_SHAPES = [
            [[y, x] for (y, x) in shape] for shape in unique_coordinates
        ]

        return config

    def _construct_augmented_config_path(
        self, file_path: str, infix: str = "_augmented"
    ) -> str:
        """ """
        augmented_file_path = file_path.with_name(
            f"{file_path.stem}{infix}{self.config_path.suffix}"
        )

        return augmented_file_path

    def _write_config(self, file_path: str, config: dict) -> None:
        """ """
        with open(file_path, "w") as file:
            yaml.dump(config, file, Dumper=FlowListDumper, default_flow_style=False)

    def augment_config(self, config) -> ConfigModel:
        """ """
        augmented_config_path = self._construct_augmented_config_path(
            file_path=self.config_path
        )

        # Convert from Pydantic Basemodel to dictionary and then to DotDict
        # instance, to keep using dot notation for dictionary keys and values.
        config = DotDict(config.model_dump())

        augmented_config = self._add_computational_parameters(config=config)
        augmented_config = self._add_all_polyonomios(config=config)

        self._write_config(
            file_path=augmented_config_path, config=augmented_config.to_dict()
        )

        # Also write all the polyomino shapes to a separate .yaml file.
        config_all_polyominos = {
            "ALL_POLYOMINOS": augmented_config.POLYOMINO.ALL_SHAPES
        }
        self._write_config(
            file_path=CONFIG_POLYOMINOS_RELATIVE_FILE_PATH, config=config_all_polyominos
        )

        augmented_config: ConfigModel = Config.load_config(
            file_path=augmented_config_path
        )

        return augmented_config
