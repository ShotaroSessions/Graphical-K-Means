import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns

from k_means import (generate_centroids, assign_to_centroids,
                     calculate_centroids, k_means_clusters)

from live_k_means import AnimatedScatter


def start_app():

    print('Welcome to the K Means App!')

    while True:

        file_name = input('Enter path to csv: ')
        while not os.path.isfile(file_name):
            file_name = input('Please enter a valid file: ')

        df = pd.read_csv(file_name)

        k = int(input('Enter k: '))

        print(df.columns)

        valid_columns = False
        while not valid_columns:
            columns = input('Enter columns to consider. (seperated by spaces):\n').split()
            valid_columns = True
            for column in columns:
                if column not in df.columns:
                    valid_columns = False

        if len(columns) == 2:
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
            a = AnimatedScatter(x, y, groupings)
            plt.show()
        else:
            sns.set(style="ticks")
            groups = k_means_clusters(df, k, columns, 100)
            df = df[columns].copy()
            df['groups'] = groups
            sns.pairplot(df, hue='groups')
            plt.show()

        response = input('Continue plotting?[y/n] ')
        while response not in ['y', 'Y', 'n', 'N']:
            response = input('Continue plotting?[y/n] ')
        if response in ['n', 'N']:
            break;


if __name__ == '__main__':
    start_app()
