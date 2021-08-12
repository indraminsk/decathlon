import csv
import json
import math


class Decathlon:
    __COEFFICIENTS = [
            {'a': 25.4347, 'b': 18, 'c': 1.81},
            {'a': 0.14354, 'b': 220, 'c': 1.4},
            {'a': 51.39, 'b': 15, 'c': 1.05},
            {'a': 0.8465, 'b': 75, 'c': 1.42},
            {'a': 1.53775, 'b': 82, 'c': 1.81},
            {'a': 5.74352, 'b': 28.5, 'c': 1.92},
            {'a': 12.91, 'b': 4, 'c': 1.1},
            {'a': 0.2797, 'b': 100, 'c': 1.35},
            {'a': 10.14, 'b': 7, 'c': 1.08},
            {'a': 0.03768, 'b': 480, 'c': 1.85},
        ]

    __source_file_name = ''
    __output_file_name = ''

    __distributed = {}

    def __init__(self, source_file_name, output_file_name):
        self.__source_file_name = source_file_name
        self.__output_file_name = output_file_name

    def run_distributing(self):
        # load from source file raw data and convert to dictionary
        table = self.__load_from_csv()

        # calculate and store score for each athletes
        scored, athletes_score = self.__calculate_score(table)

        # distribute places using athletes score
        self.__distributed = self.__distribute_places(scored, athletes_score)

    def store_to_json(self):
        """generate output file"""

        with open(self.__output_file_name, 'w') as file:
            json.dump(self.__distributed, file, indent=4)

    def __load_from_csv(self):
        """load from csv raw data and store them into output dictionary"""

        with open(self.__source_file_name, mode='r') as data:
            reader = csv.reader(data)

            table = {}
            for rows in reader:
                columns = tuple(rows[0].split(';'))

                athlete = columns[0]
                points = columns[1:]

                table[athlete] = {'points': points, 'score': 0, 'place': '-'}

            return table

    def __calculate_score(self, table):
        """calculate score for each athletes. return
            output dictionary with filled score
            dictionary with only athletes scores (needing in the future)"""

        scored = table

        athletes_score = {}

        for athlete in table:
            total = 0

            for i in range(len(table[athlete]['points'])):
                score = 0

                if i == 9:
                    continue
                else:
                    value = float(table[athlete]['points'][i])

                    if i == 0 or i == 4 or i == 5:
                        if self.__COEFFICIENTS[i]['b'] > value:
                            score = math.trunc(
                                self.__COEFFICIENTS[i]['a'] * (self.__COEFFICIENTS[i]['b'] - value) ** self.__COEFFICIENTS[i]['c'])
                    else:
                        if value > self.__COEFFICIENTS[i]['b']:
                            score = math.trunc(
                                self.__COEFFICIENTS[i]['a'] * (value - self.__COEFFICIENTS[i]['b']) ** self.__COEFFICIENTS[i]['c'])

                total = total + score

            scored[athlete]['score'] = total
            athletes_score[athlete] = total

        return scored, athletes_score

    def __distribute_places(self, table, athletes_score):
        """collect coincidences for each point values
            return output dictionary with filled places"""

        distributed = table

        athletes_score_sorted = {k: v for k, v in
                                 sorted(athletes_score.items(), key=lambda item: item[1], reverse=True)}

        frequency_distribution = self.__calculate_frequency_distribution(athletes_score_sorted)

        for (athlete, score) in athletes_score_sorted.items():
            if frequency_distribution[score]['coincidence'] == 0:
                distributed[athlete]['place'] = str(frequency_distribution[score]['place'])
            else:
                start = frequency_distribution[score]['place']
                end = frequency_distribution[score]['place'] + frequency_distribution[score]['coincidence']

                distributed[athlete]['place'] = '{start}-{end}'.format(start=start, end=end)

        return distributed

    # noinspection PyMethodMayBeStatic
    def __calculate_frequency_distribution(self, athletes_score):
        """calculate for each score coincidence events
            return dictionary with this information"""

        frequency_distribution = {}

        for index, (athlete, score) in enumerate(athletes_score.items()):
            if score in frequency_distribution.keys():
                frequency_distribution[score]['coincidence'] = frequency_distribution[score]['coincidence'] + 1
            else:
                frequency_distribution[score] = {'place': index + 1, 'coincidence': 0}

        return frequency_distribution
