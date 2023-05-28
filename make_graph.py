from icecream import ic
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import statsmodels.api as sm

def main():
    filename = "mutation_statistics5"
    data = pd.read_csv(filename + ".csv") 
    print(data.head())

    X = data["mutation_probability"].tolist()
    # X = data["generation"].tolist()
    Y = data["final fitness"].tolist()
    # X = [i for i in range(len(Y))]
    
    # plt.figure().set_figwidth(12)
    ic(X, Y)
    plt.xlabel("mutation probability")
    plt.ylabel("total average fitness")
    plt.scatter(X, Y)

    coeficients = np.polyfit(X,Y, deg=1)
    mymodel = np.poly1d(coeficients)
    myline = np.linspace(min(X), max(X), 100)
    plt.plot(myline, mymodel(myline), color="green")

    plt.savefig(filename + ".png")

def main2():
    data1 = pd.read_csv("fitness_statistics_linear.csv")
    data2 = pd.read_csv("fitness_statistics_elitism.csv") 

    X = data1["generation"].tolist()
    Y1 = data1["final fitness"].tolist()
    Y2 = data2["final fitness"].tolist()
    plt.scatter(X, Y1, color="red", label="baseline")
    plt.scatter(X, Y2, color="green", label="elitism selection")

    coeficients = np.polyfit(X,Y1, deg=2)
    mymodel = np.poly1d(coeficients)
    myline = np.linspace(min(X), max(X), 100)
    plt.plot(myline, mymodel(myline), color="red")

    coeficients = np.polyfit(X,Y2, deg=2)
    mymodel = np.poly1d(coeficients)
    myline = np.linspace(min(X), max(X), 100)
    plt.plot(myline, mymodel(myline), color="green")


    plt.legend()

    plt.xlabel("generation")
    plt.ylabel("average fitness")

    plt.savefig("analysis_elitism_selection.png")



if __name__ == "__main__":
    main()