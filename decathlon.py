import csv
import json
import math
import sys


def load_from_csv(path):
    """load from csv raw data and store them into output dictionary"""

    with open(path, mode='r') as data:
        reader = csv.reader(data)

        table = {}
        for rows in reader:
            columns = tuple(rows[0].split(';'))

            athlete = columns[0]
            points = columns[1:]

            table[athlete] = {'points': points, 'score': 0, 'place': '-'}

        return table


def calculate_score(table):
    """calculate score for each athletes. return
        output dictionary with filled score
        dictionary with only athletes scores (needing in the future)"""

    scored = table

    coefficients = [
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
                    if coefficients[i]['b'] > value:
                        score = math.trunc(
                            coefficients[i]['a'] * (coefficients[i]['b'] - value) ** coefficients[i]['c'])
                else:
                    if value > coefficients[i]['b']:
                        score = math.trunc(
                            coefficients[i]['a'] * (value - coefficients[i]['b']) ** coefficients[i]['c'])

            total = total + score

        scored[athlete]['score'] = total
        athletes_score[athlete] = total

    return scored, athletes_score


def distribute_places(table, athletes_score):
    """collect coincidences for each point values
        return output dictionary with filled places"""

    distributed = table

    athletes_score_sorted = {k: v for k, v in sorted(athletes_score.items(), key=lambda item: item[1], reverse=True)}

    frequency_distribution = calculate_frequency_distribution(athletes_score_sorted)

    for (athlete, score) in athletes_score_sorted.items():
        if frequency_distribution[score]['coincidence'] == 0:
            distributed[athlete]['place'] = str(frequency_distribution[score]['place'])
        else:
            start = frequency_distribution[score]['place']
            end = frequency_distribution[score]['place'] + frequency_distribution[score]['coincidence']

            distributed[athlete]['place'] = '{start}-{end}'.format(start=start, end=end)

    return distributed


def calculate_frequency_distribution(athletes_score):
    """calculate for each score coincidence events
        return dictionary with this information"""

    distribution = {}

    for index, (athlete, score) in enumerate(athletes_score.items()):
        if score in distribution.keys():
            distribution[score]['coincidence'] = distribution[score]['coincidence'] + 1
        else:
            distribution[score] = {'place': index + 1, 'coincidence': 0}

    return distribution


def store_to_json(data, output_file_name):
    """generate output file"""

    with open(output_file_name, 'w') as file:
        json.dump(data, file, indent=4)


def main():
    # check enough cmd parameters
    if len(sys.argv) < 3:
        print('please set source or/and output file names')
        print('example:\n\tdecathlon.py <source file name> <output file name>')

        return

    # init source and output file names
    source_file_name = sys.argv[1]
    output_file_name = sys.argv[2]

    # load from source file raw data and convert to dictionary
    table = load_from_csv(source_file_name)

    # calculate and store score for each athletes
    scored, athletes_score = calculate_score(table)

    # distribute places using athletes score
    distributed = distribute_places(scored, athletes_score)

    # create file for output data and store into it
    store_to_json(distributed, output_file_name)

    print('work completed')


main()
