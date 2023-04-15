
from genetic_project import constants
from genetic_project.model import Model
from genetic_project.ViewController import ViewController


def main() -> None:
    model = Model()
    vc = ViewController(model)

    vc.start_simulation()


if __name__ == "__main__":
    main()