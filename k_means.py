from math import sqrt
from random import randint


def euclid_distance(point_a, point_b, ranges):
    """Finds the distance between two points"""

    acc = 0
    count = 0
    for dimension_a, dimension_b in zip(point_a, point_b):
        # Uses the ranges to determine a ratio between variable units
        ratio = ranges[0] / ranges[count]
        # Converts the Delta with the ratio before squaring
        acc += ((dimension_a - dimension_b) * ratio)**2
        count += 1

    return sqrt(acc)


def generate_centroids(df, k, data):
    """Initializes k centroids at a random point in the dataset"""

    centroids = []

    for centroid_num in range(k):
        centroids.append(
            [df.iloc[randint(0, len(df) - 1)][dim] for dim in data])

    return centroids


def assign_to_centroids(df, centroids, data):
    """Assignes every datapoint to the nearest centroid"""

    groups = []
    ranges = [max(df[dim]) - min(df[dim]) for dim in data]

    for index in range(len(df)):
        least = -1
        assigned_centroid = -1
        current_centroid = 0

        datapoint = [df.iloc[index][dim] for dim in data]

        for centroid in centroids:
            distance = euclid_distance(datapoint, centroid, ranges)
            if least == -1 or least > distance:
                least = distance
                assigned_centroid = current_centroid
            current_centroid += 1

        groups.append(assigned_centroid)

    return groups


def calculate_centroids(df, centroids, groups, data):
    """Averages the dimensions of each cluster to find new centroids"""

    new_centroids = []
    for centroid_num in range(len(centroids)):
        summ = [0 for _ in data]
        count = 0
        for index in range(len(df)):
            if groups[index] == centroid_num:
                for data_index in range(len(summ)):
                    summ[data_index] += df.iloc[index][data[data_index]]
                count += 1

        if(count != 0):
            new_centroids.append([total/count for total in summ])
        else:
            new_centroids.append(centroids[centroid_num])

    return new_centroids


def k_means_clusters(df, k, data, repeats):
    """Uses the k means formula to generate 'k' groups from the dataframe"""

    centroids = generate_centroids(df, k, data)
    groups = assign_to_centroids(df, centroids, data)
    for count in range(repeats):
        centroids = calculate_centroids(df, centroids, groups, data)
        groups = assign_to_centroids(df, centroids, data)

    return groups
