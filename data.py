import m_datasets


class DataGenerator:
    """
    This class generates the data in a dictionary.
    """

    def __init__(self):
        """
        Class constructor responsible for generating data
        """
        self.dataset = dict()
        for count1 in range(0, 1000):
            key1 = 'critic' + str(count1)
            value1 = dict()
            length = random.randint(1, 10)
            for count2 in range(0, length):
                key2 = 'movie' + str(count2)
                value2 = random.randrange(0, 5)
                value1[key2] = value2
            self.dataset[key1] = value1

    def get_data(self):
        """
        Returns the prepared data in the form of a dictionary
        :return: dictionary of data
        """
        return self.dataset
