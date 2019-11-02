import csv
import argparse

from operator import itemgetter
from datetime import datetime
from itertools import groupby

# import helper functions from util file
from utils import my_round, output_list, count_the_months, check_all_there
from utils import calculate_average_crossing_per_month_and_measure


def parse_args():
    """
    This util function takes in the arguments passed in the shell to be used in the main script.
    Returns:
        args -- arguments
    """
    parser = argparse.ArgumentParser(description='Look for Border Crossing Statistics')
    parser.add_argument('--input', help="enter the input filename", type=str)
    parser.add_argument('--output', help="enter the output filename", type=str)
    args = parser.parse_args()
    return args


def main():
    """ This is Main function that takes in the input file of border crossing entry data and returns
     the desired statistics. """

    # Input and Output files Error-Handling
    args = parse_args()
    if args.input is None:
        raise ImportError('Did not specify the correct input file!')
    if args.output is None:
        raise ImportError('Did not specify the correct output file!')

    # Read in the border_crossing data
    with open(args.input, mode='r') as csv_file:

        # Read the CSV data into a list of lists
        csv_reader = csv.reader(csv_file, delimiter=',')

        # Sort the list by Border, Date, and Measure in descending order
        sorted_list = sorted(csv_reader, key=itemgetter(3, 5))

        # Group the sorted list via the keys--border names, dates, and measures, so
        # that we have a bunch of rows with the same border name, date, measure, but different values!
        # In each row, check if the 6th index (this is our value) is a number and is not 0!
        # If this is true, then add that those values together and create a new list
        # which holds this aggregated summation of values for each border name, date, and measure
        list_with_agg_values = [key + [sum([int(r[6]) for r in rows if r[6].isdigit() and int(r[6]) != 0])]
                                for key, rows in groupby(sorted_list, key=lambda x: x[3:6])]

        # To find the count of number of months 
        num_of_months = count_the_months(list_with_agg_values)

        # calculate the average crossing per month and per measure
        list_with_avg = calculate_average_crossing_per_month_and_measure(num_of_months, list_with_agg_values)

        # Sort the list by Date in descending order
        sorted_list_with_val_border_measure = sorted(list_with_avg, key=itemgetter(1), reverse=True)

    # Write out to the output csv file
    with open(args.output, mode='w') as csv_outfile:
        outfile_writer = csv.writer(csv_outfile, delimiter=',', quoting=csv.QUOTE_NONE)

        # Column headers--Don't quote them
        outfile_writer.writerow(['Border', 'Date', 'Measure', 'Value', 'Average'])

        outfile_writer = csv.writer(csv_outfile, delimiter=',', quoting=csv.QUOTE_NONE)

        # for each row in the final list, remove the list of list and create one list
        for row in sorted_list_with_val_border_measure:
            outfile_writer.writerow(output_list(row))

if __name__ == '__main__':
    main()