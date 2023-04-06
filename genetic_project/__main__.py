"""This specially named module makes the package runnable."""

from genetic_project import constants
from genetic_project.model import Model
from genetic_project.ViewController import ViewController


def main() -> None:
    """Entrypoint of simulation."""
    model = Model(constants.CELL_COUNT, constants.CELL_SPEED)
    vc = ViewController(model)
    vc.start_simulation()


if __name__ == "__main__":
    main()