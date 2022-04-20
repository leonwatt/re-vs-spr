import csv
import json

DATE_FORMAT = "%Y-%m-%dT%H:%M:%S"

def read_from_file(path):
    with open(path) as f:
        return f.read()

def write_to_file(path, content):
    with open(path, "w") as f:
        f.write(str(content))

def read_csv(path, delimiter = ","):
    with open(path) as f:
        return list(csv.DictReader(f, delimiter=delimiter))

def read_json(path):
    return json.loads(read_from_file(path))

def write_csv(path, content):
    with open(path, "w") as f:
        writer = csv.writer(f)
        header = content[0].keys()
        writer.writerow(header)
        writer.writerows([[row[h] for h in list(header)] for row in content])

def group_by(arr_of_dicts, grouping_attr):
    res = {}

    for el in arr_of_dicts:
        grouping_value = el[grouping_attr]
        res.setdefault(grouping_value, [])
        res[grouping_value] += [el]

    return res

def group_by_as_list(arr_of_dicts, grouping_attr):
    return list(group_by(arr_of_dicts, grouping_attr).values())


def divide_or_zero(numerator, denominator):
    if denominator == 0: return 0
    return numerator / denominator

def flatten(list_of_lists):
    res = []
    for l in list_of_lists: res.extend(l)
    return res

def filter_duplicates(arr, key_fn):
    return [el for (i, el) in enumerate(arr) if arr.index([el2 for el2 in arr if key_fn(el) == key_fn(el2)][0]) == i]