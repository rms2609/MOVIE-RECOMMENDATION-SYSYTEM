import data
import math


def euclidean_distance(dataset, critic1, critic2):
    """
    This function calculates the euclidean distance of two points.
    :param dataset: preferences of critics
    :param critic1: name of 1st critic
    :param critic2: name of 2nd critic
    :return: similarity score
    """
    shared_items = 0
    for items in dataset[critic1]:
        if items in dataset[critic2]:
            shared_items += 1
    if shared_items == 0:
        return 0
    else:
        sum_of_squares = sum([pow(dataset[critic1][item] - dataset[critic2][item], 2) for item in dataset[critic1] if
                              item in dataset[critic2]]) * 1.0
        sum_of_squares = 1 / (1 + sum_of_squares)
        return sum_of_squares


def pearson_correlation(dataset, critic1, critic2):
    """
    This function calculates the pearson correlation of two points.
    :param dataset: preferences of critics
    :param critic1: name of 1st critic
    :param critic2: name of 2nd critic
    :return: similarity score
    """
    shared_items = dict()
    for items in dataset[critic1]:
        if items in dataset[critic2]:
            shared_items[items] = 1
    length = len(shared_items)
    if length == 0:
        return 0
    else:
        sum1 = sum([dataset[critic1][item] for item in shared_items])
        sum2 = sum([dataset[critic2][item] for item in shared_items])
        square_sum1 = sum([pow(dataset[critic1][item], 2) for item in shared_items])
        square_sum2 = sum([pow(dataset[critic2][item], 2) for item in shared_items])
        product_sum = sum([dataset[critic1][item] * dataset[critic2][item] for item in shared_items])
        numerator = product_sum - (sum1 * sum2 / length)
        denominator = math.sqrt((square_sum1 - pow(sum1, 2) / length) * (square_sum2 - pow(sum2, 2) / length))
        if denominator == 0:
            return 0
        else:
            return numerator / denominator


def top_matches(dataset, critic, number=5, similarity_criterion=euclidean_distance):
    """
    Gives the top matching critics based on the training data
    :param dataset: preferences of critics
    :param critic: name of the critic
    :param number: number of matches required
    :param similarity_criterion: which criterion to be used for similarity checking
    :return: similarity score
    """
    scores = [(similarity_criterion(dataset, critic, other), other) for other in dataset if other != critic]
    scores.sort()
    scores.reverse()
    return scores[0:number]


def get_recommendation(dataset, critic, similarity_criterion=pearson_correlation):
    """
    This function gives the predictions based on a given similarity metric
    :param dataset: preferences of critics
    :param critic: name of the critic
    :param similarity_criterion: which criterion to be used for similarity checking
    :return: rankings
    """
    total = dict()
    similarity_sums = dict()
    for others in dataset:
        if others == critic:
            continue
        similarity = similarity_criterion(dataset, critic, others)
        if similarity <= 0:
            continue
        for items in dataset[others]:
            if items not in dataset[critic] or dataset[critic][items] == 0.0:
                total.setdefault(items, 0)
                total[items] += dataset[others][items] * similarity
                similarity_sums.setdefault(items, 0)
                similarity_sums[items] += similarity
    rankings = [(total / similarity_sums[item], item) for item, total in total.items()]
    rankings.sort()
    rankings.reverse()
    return rankings


def transform_dataset(dataset):
    """
    This function transforms the dataset to invert, movie names to rating in the dataset
    :param dataset: preferences of critics
    :return: result dictionary
    """
    result = dict()
    for items in dataset:
        for item in dataset[items]:
            result.setdefault(item, dict())
            result[item][items] = dataset[items][item]
    return result


data_object = data.DataGenerator()
Dataset = data_object.get_data()
ans='Y'
while ans=='Y':
    print("Critics name are from\ncritic0 to critic999")
    Critic = input("Enter name of the critic\n")
    k=int(Critic[6:])
    dic=[]
    if 0<=k<=999:
        dic=get_recommendation(Dataset, Critic)
        for i in dic:
           print("%s = %.3s"%(i[1],i[0]))
    else:
        print("Enter Valid Name")
    ans=input("Wanna give another shot (Y/N)?\n")
    if ans!='Y':
        print("Thanks for using")
