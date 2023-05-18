from icecream import ic
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd 
import statsmodels.api as sm
from sklearn.preprocessing import PolynomialFeatures

def main():
    data = pd.read_csv('mutation_statistics5.csv') 
    print(data.head())

    X = data["mutation_probability"].tolist()
    Y = data["final fitness"].tolist()
    ic(X, Y)
    plt.scatter(X, Y)

    polynomial_features = PolynomialFeatures(degree=2, include_bias = True)
    XP = polynomial_features.fit_transform(data["mutation_probability"].values.reshape((-1, 1)))

    model = sm.OLS(Y,XP).fit()

    # print(model.summary(alpha=0.05))

    X_plot = np.arange(min(X),max(X),1)
    X_plotP = polynomial_features.fit_transform(X_plot.reshape((-1, 1)))
    pred_ols = model.get_prediction(X_plotP)
    iv_l = pred_ols.summary_frame(alpha=0.1)["obs_ci_lower"]
    iv_u = pred_ols.summary_frame(alpha=0.1)["obs_ci_upper"]
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot(X, Y, "o", label="data")
    ax.plot(X_plot, pred_ols.predicted_mean, label="OLS")
    ax.plot(X_plot, iv_u, "r--")
    ax.plot(X_plot, iv_l, "r--")
    plt.savefig("mutation_statistics6_graph.png")

if __name__ == "__main__":
    main()