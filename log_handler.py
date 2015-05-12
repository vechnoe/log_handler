# coding: utf-8

"""Log handler"""


def length_checker(source_list):
    """
    :return Returns list with max and min length of item in list

    >>> length_checker([['42', 'ham', 'jam'], ['9000', 'jam', 'spam']])
    {'max': 4, 'min': 2}
    >>> length_checker([['404', 'ham', 'jam'], ['200', 'jam', 'spam']])
    {'max': 3, 'min': 3}
    """
    return dict(
        min=len(min(source_list, key=lambda s: len(s[0]))[0]),
        max=len(max(source_list, key=lambda s: len(s[0]))[0])
    )


def source_handler(source_list, item_length):
    """
    :return Returns two dictionary according
    max & min item length in the list

    >>> source_list = [['42', 'ham', 'jam'], ['34', 'muffin', 'ham'],
    ...                ['5000', 'spam', 'ham'], ['9000', 'jam', 'spam']]
    >>> item_length = length_checker(source_list)
    >>> out = source_handler(source_list, item_length)
    >>> out[0]
    {'5000': ['spam', 'ham'], '9000': ['jam', 'spam']}
    >>> out[1]
    {'42': ['ham', 'jam'], '34': ['muffin', 'ham']}
    """
    long_substrings = {}
    short_substrings = {}

    for item in source_list:
        if len(item[0]) == item_length['min']:
            short_substrings.update({item[0]: [item[1], item[2]]})
        elif len(item[0]) == item_length['max']:
            long_substrings.update({item[0]: [item[1], item[2]]})

    return [long_substrings, short_substrings]


def data_handler(data_set, item_length, substrings):
    """
    If the key is in the input dictionary is a prefix of
    line from the data_set, then add this
    line instead of the prefix to the output list
    :return output_list

    >>> data_set = set(['424013545', '424014545',
    ... '424024545', '424004545', '345013545',
    ... '345014545', '345024545', '345004545'])
    >>> source_list = [['4240', 'ham', 'toast'], ['42401', 'muffin', 'brad'],
    ... ['42402', 'milk', 'water'], ['3450', 'cola', 'whiskey'],
    ... ['34501', 'apple', 'orange'], ['34502', 'onion', 'tomato',]]
    >>> item_length =  length_checker(source_list)
    >>> substrings = source_handler(source_list, item_length)
    >>> data_handler(data_set, item_length, substrings) #doctest: +NORMALIZE_WHITESPACE
    [['345014545', ['apple', 'orange']], ['424013545', ['muffin', 'brad']],
        ['424024545', ['milk', 'water']], ['345024545', ['onion', 'tomato']],
        ['345013545', ['apple', 'orange']], ['424014545', ['muffin', 'brad']],
        ['345004545', ['cola', 'whiskey']], ['424004545', ['ham', 'toast']]]
    """
    long_substrings = substrings[0]
    short_substrings = substrings[1]

    output_set = set()
    output_list = []

    for item in data_set:
        # If the string from the source file
        # is prefix of the string from data file
        if item[:item_length['max']] in long_substrings:
            output_list.append(
                [item, long_substrings[item[:item_length['max']]]])
            output_set.add(item)

    # In the second pass handle only those lines
    # that not match in the first pass.
    data_set = data_set - output_set

    for item in data_set:
        if item[:item_length['min']] in short_substrings:
            output_list.append(
                [item, short_substrings[item[:item_length['min']]]])

    return output_list


if __name__ == '__main__':
    import sys

    info = 'Usage: log_handler.py in.csv source.dat'
    try:
        source = sys.argv[1]
        data = sys.argv[2]
    except (TypeError, ValueError, IndexError):
        sys.exit(info)
    if len(sys.argv) < 3:
        sys.exit(info)

    with open(source) as csv_file:
        # I think that the lines contain '\n'.
        # A slices saves at execution time in comparison with s.replace()
        source_list = [line[:-1].split(',') for line in csv_file]

    with open(data) as data_file:
        data_set = {line[:-1] for line in data_file}

    item_length = length_checker(source_list)

    substrings = source_handler(source_list, item_length)

    out_list = data_handler(data_set, item_length, substrings)

    with open('out.csv', 'w') as out_csv:
        for item in out_list:
            out_csv.write("%s,%s,%s\n" % (item[0], item[1][0], item[1][1]))




