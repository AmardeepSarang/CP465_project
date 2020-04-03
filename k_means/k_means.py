import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import copy
import random as rd
pd.options.mode.chained_assignment = None  # To stop warnings from pandas for cleaner output

# Function to calculate and store euclidean distances of each tuple to the cluster centers
def calcDistances(math_read, centers):
    for i in centers.keys():
        math_read["Distance to cluster {}".format(i)] = (
            np.sqrt(
                (math_read['math score'] - centers[i][0]) ** 2
                + (math_read['reading score'] - centers[i][1]) ** 2
            )
        )

    # Create array of columns to add to the dataframe
    center_distances = ["Distance to cluster {}".format(i) for i in centers.keys()]

    # Get the index of the cluster center with the shortest distance for each tuple 
    math_read["closest"] = math_read.loc[:,center_distances].idxmin(axis=1)

    # Map the cluster centers, also map colors to the cluster centers
    math_read["closest"] = math_read["closest"].map(lambda x: int(x.lstrip("Distance to cluster ")))
    math_read["color"] = math_read["closest"].map(lambda x: colors[x])

    return math_read

# Function to recompute new cluster centers using the means
def updateCenters(c):
    for i in centers.keys():
        centers[i][0] = np.mean(math_read[math_read["closest"] == i]["math score"])
        centers[i][1] = np.mean(math_read[math_read["closest"] == i]["reading score"])
    return c

# Read in StudentPerformance CSV as a data frame
data = pd.read_csv("StudentsPerformance.csv")

# Get dataframes of continuous variables in dataset (exam scores)
math_read = data[["math score", "reading score"]]

# Initialize k value (Please pick from 1 to 6 since limited by colors offered in matplotlib)
k = int(input("Enter k value (1 to 6): "))

# Choose random points to be the cluster centers
centers = {
    i+1: [rd.choice(math_read["math score"]), rd.choice(math_read["reading score"])]
    for i in range(k)
}

# Initialize colors for clusters
colors = {1: "r", 2: "g", 3:"b", 4: "y", 5: "c", 6: "m"}

# Display initial plots of math scores in relation to reading and writing scores with initial cluster centers
plt.scatter(math_read["math score"], math_read["reading score"], c="k")
for i in centers.keys():
    plt.scatter(*centers[i], c=colors[i], marker="*", s=200)
plt.title("Math and Reading")
plt.xlabel("Math Scores")
plt.ylabel("Reading Scores")
plt.show()

# Calculate first round of cluster assignments
math_read = calcDistances(math_read, centers)

# Display data in clusters
plt.scatter(math_read["math score"], math_read["reading score"], alpha=0.5, edgecolor="k", c=math_read["color"])
for i in centers.keys():
    plt.scatter(*centers[i], c="k", marker="*", s=200)
plt.title("Math and Reading")
plt.xlabel("Math Scores")
plt.ylabel("Reading Scores")
plt.show()

# Recompute each cluster center
centers = updateCenters(centers)

# Display new cluster centers:
plt.scatter(math_read["math score"], math_read["reading score"], c="k")
for i in centers.keys():
    plt.scatter(*centers[i], c=colors[i], marker="*", s=200)
plt.title("Math and Reading")
plt.xlabel("Math Scores")
plt.ylabel("Reading Scores")
plt.show()

# Calculate new round of cluster assignments
math_read = calcDistances(math_read, centers)

# Display data in new clusters
plt.scatter(math_read["math score"], math_read["reading score"], alpha=0.5, edgecolor="k", c=math_read["color"])
for i in centers.keys():
    plt.scatter(*centers[i], c="k", marker="*", s=200)
plt.title("Math and Reading")
plt.xlabel("Math Scores")
plt.ylabel("Reading Scores")
plt.show()

# Continue recomputing cluster centers and assigning points to closest clusters until the cluster's stabilize
while True:
    closest_centers = math_read["closest"].copy(deep=True)

    centers = updateCenters(centers)

    math_read = calcDistances(math_read, centers)

    # Breaks out of the loop when points have their closest cluster centers
    if closest_centers.equals(math_read["closest"]):
        break

print(math_read.head())

# Plot clusters after the multiple iterations
plt.scatter(math_read["math score"], math_read["reading score"], alpha=0.5, edgecolor="k", c=math_read["color"])
for i in centers.keys():
    plt.scatter(*centers[i], c="k", marker="*", s=200)
plt.title("Math and Reading")
plt.xlabel("Math Scores")
plt.ylabel("Reading Scores")
plt.show()