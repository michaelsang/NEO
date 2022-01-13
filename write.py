"""Write a stream of close approaches to CSV or to JSON.

This module exports two functions: `write_to_csv` and `write_to_json`, each of
which accept an `results` stream of close approaches and a path to which to
write the data.

These functions are invoked by the main module with the output of the `limit`
function and the filename supplied by the user at the command line. The file's
extension determines which of these functions is used.

You'll edit this file in Part 4.
"""
import csv
import json
from helpers import datetime_to_str


def write_to_csv(results, filename):
    """Write an iterable of `CloseApproach` objects to a CSV file.

    The precise output specification is in `README.md`. Roughly, each output row
    corresponds to the information in a single close approach from the `results`
    stream and its associated near-Earth object.

    :param results: An iterable of `CloseApproach` objects, as produced by the limit function.
    :param filename: A Path-like object pointing to where the data should be saved.
    """

    fieldnames = (
        'datetime_utc', 'distance_au', 'velocity_km_s',
        'designation', 'name', 'diameter_km', 'potentially_hazardous'
    )

    # TODO: Write the results to a CSV file, following the specification in the instructions.

    #The fieldnames parameter is a sequence of keys that identify the order in which values in the dictionary
    #passed to the writerow() method are written to the csvfile.
    #The fieldnames are written to csv file as the first row.
    fieldnames = ('datetime_utc', 'distance_au', 'velocity_km_s',
                      'designation', 'name', 'diameter_km',
                      'potentially_hazardous')
    with open(filename, "w") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()  #function writeheader will return None from KB
        for approach in results:   #extract information from approach
            writer.writerow({ #pass dictionary to writerow
                'datetime_utc': datetime_to_str(approach.time),  #or approach.time_str?
                'distance_au': approach.distance,
                'velocity_km_s': approach.velocity,
                'designation': approach._designation,  #or approach.neo.designation
                'name' : approach.neo.name,
                'diameter_km' :approach.neo.diameter,
                'potentially_hazardous' : str(approach.neo.hazardous)}
            )



def write_to_json(results, filename):
    """Write an iterable of `CloseApproach` objects to a JSON file.
    The precise output specification is in `README.md`. Roughly, the output is a
    list containing dictionaries, each mapping `CloseApproach` attributes to
    their values and the 'neo' key mapping to a dictionary of the associated
    NEO's attributes.
    :param results: An iterable of `CloseApproach` objects.
    :param filename: A Path-like object pointing to where the data should be saved.
    """
    # TODO: Write the results to a JSON file, following the specification in the instructions.

    dict_list = []
    for approach in results:
        datetime_utc = approach.time_str
        # extract more information
        # create a dictionary, refer to README
        dictionary = {
            'datetime_utc': datetime_to_str(approach.time), #approach is the row. Do approach.time_str instead?
            'distance_au': approach.distance,
            'velocity_km_s': approach.velocity,
            'neo': {
                'designation': approach._designation,
                'name': approach.neo.name,
                'diameter_km': approach.neo.diameter,
                'potentially_hazardous': approach.neo.hazardous
            }
        }
        # append the dictionary to a list
        dict_list.append(dictionary)

    # write the list of dictionary to json file
    with open(filename, 'w') as json_file:
        json.dump(dict_list, json_file, indent="\t")