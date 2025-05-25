""" """

import yaml

from src.boom_tetris.config.model import ConfigModel


class Config:
    """ """

    def __init__(self, config_path: str) -> None:
        """ """
        self.config_path = config_path
        self.config = self.load_config(file_path=self.config_path)

    def load_config(self, file_path: str, file_type: str = "yaml") -> dict:
        """ """
        if file_type == "yaml":
            with open(file_path) as file:
                config = yaml.load(file, Loader=yaml.FullLoader)

            config = ConfigModel(**config)

        return config

    def _add_parameters(self, config: ConfigModel) -> dict:
        """ """
        cell_width = config.BOARD.RECT.WIDTH // config.BOARD.DIMENSIONS.COLS
        cell_height = config.BOARD.RECT.HEIGHT // config.BOARD.DIMENSIONS.ROWS

        config_dict = config.model_dump()

        config_dict["BOARD"]["CELL"] = {"WIDTH": cell_width, "HEIGHT": cell_height}

        return config_dict

    def _construct_augmented_config_path(
        self, file_path: str, infix: str = "_augmented"
    ) -> str:
        """ """
        augmented_file_path = file_path.with_name(
            f"{file_path.stem}{infix}{self.config_path.suffix}"
        )

        return augmented_file_path

    def _save_config(self, file_path: str, config: dict) -> None:
        """ """
        with open(file_path, "w") as file:
            yaml.dump(config, file)

    def augment_config(self) -> ConfigModel:
        """ """
        augmented_config: dict = self._add_parameters(config=self.config)
        augmented_config_path = self._construct_augmented_config_path(
            file_path=self.config_path
        )

        self._save_config(file_path=augmented_config_path, config=augmented_config)
        augmented_config: ConfigModel = self.load_config(
            file_path=augmented_config_path
        )

        return augmented_config
