import math


def average_matches(matches, k):
    """
    Calculate sum of top 3 samples for a song
    """
    song_matches = {}

    for i in range(len(matches)):
        match = matches[i]
        filename = match['filename']

        if not filename in song_matches:
            song_matches[filename] = {'sum': match['distance'], 'count': 1}
        elif song_matches[filename]['count'] < k:
            song_matches[filename]['count'] += 1
            # Add distance weighted by logarithm of its position in the list
            song_matches[filename]['sum'] += match['distance'] * \
                (1 + math.log(i + 1, 10))

    # Map into average
    return {key: (value['sum'] / value['count'])
            for key, value in song_matches.items()}
