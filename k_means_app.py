import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from k_means import (generate_centroids, assign_to_centroids,
                     calculate_centroids, k_means_clusters)
from live_k_means import AnimatedScatter


def start_app():

    print('Welcome to the K Means App!')

    active = True
    while active:

        file_name = input('Enter path to csv: ')
        while not os.path.isfile(file_name):
            file_name = input('Please enter a valid file: ')

        df = pd.read_csv(file_name)

        k = int(input('Enter k: '))

        valid_columns = df.columns

        print(valid_columns)

        prompt = 'Enter columns to consider. (seperated by spaces):\n'
        columns = input(prompt).split()
        while False in [column in df.columns for column in valid_columns]:
            columns = input(prompt).split()

        if len(columns) == 2:
            animated_xy(df, k, columns)
        else:
            scatter_matrix(df, k, columns)

        response = input('Continue plotting?[y/n] ')
        while response not in ['y', 'Y', 'n', 'N']:
            response = input('Continue plotting?[y/n] ')
        if response in ['n', 'N']:
            active = False


def animated_xy(df, k, columns):
    centroids = generate_centroids(df, k, columns)
    groups = assign_to_centroids(df, centroids, columns)
    groupings = [groups]
    for count in range(100):
        if(centroids == calculate_centroids(df, centroids, groups, columns)):
            print(f"Finished at PASS: ", count)
            break
        centroids = calculate_centroids(df, centroids, groups, columns)
        groups = assign_to_centroids(df, centroids, columns)
        groupings.append(groups)

    x, y = df[columns[0]], df[columns[1]]
    AnimatedScatter(x, y, groupings)
    plt.show()


def scatter_matrix(df, k, columns):
    sns.set(style="ticks")
    groups = k_means_clusters(df, k, columns, 100)
    df = df[columns].copy()
    df['groups'] = groups
    sns.pairplot(df, hue='groups')
    plt.show()


if __name__ == '__main__':
    start_app()
