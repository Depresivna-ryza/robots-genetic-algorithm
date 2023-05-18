from genetic_project2.constants import LOAD_ROBOTS, MUTATION_STATISTICS
from genetic_project2.model import Model
from genetic_project2.ViewController import ViewController
import pickle



def main() -> None:
    if LOAD_ROBOTS:
        with open('data2.pkl', 'rb') as inp:
            model = pickle.load(inp)
    else:
        model = Model()
    vc = ViewController(model)

    vc.start_simulation()


def statistics_mutation():
    model = Model()
    vc = ViewController(model)
    vc.start_statistics_mutation()


if __name__ == "__main__":
    # statistics_mutation()
    main()