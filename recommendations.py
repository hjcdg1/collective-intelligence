from math import sqrt

# A dictionary of movie critics and their ratings of a small set of movies
critics = {
    'Lisa Rose': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 3.5,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 3.0
    },
    'Gene Seymour': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 3.5,
        'Just My Luck': 1.5,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Michael Phillips': {
        'Lady in the Water': 2.5,
        'Snakes on a Plane': 3.0,
        'Superman Returns': 3.5,
        'The Night Listener': 4.0
    },
    'Claudia Puig': {
        'Snakes on a Plane': 3.5,
        'Just My Luck': 3.0,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 2.5,
        'The Night Listener': 4.5
    },
    'Mick LaSalle': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Just My Luck': 2.0,
        'Superman Returns': 3.0,
        'You, Me and Dupree': 2.0,
        'The Night Listener': 3.0
    },
    'Jack Matthews': {
        'Lady in the Water': 3.0,
        'Snakes on a Plane': 4.0,
        'Superman Returns': 5.0,
        'You, Me and Dupree': 3.5,
        'The Night Listener': 3.0
    },
    'Toby': {
        'Snakes on a Plane': 4.5,
        'Superman Returns': 4.0,
        'You, Me and Dupree': 1.0
    }
}

# Return a similarity score for `person1` and `person2`
def calculate_similarity(obj, person1, person2, method='pearson'):
    # Get the list of shared movies
    shared_movies = {}
    for movie in obj[person1]:
        if movie in obj[person2]:
            shared_movies[movie] = 1

    # If they have no ratings in common, return 0
    n = len(shared_movies)
    if n == 0:
        return 0

    # Pearson Correlation Score (Return a Pearson Correlation Coefficient) : Use people as axes in a chart
    if method == 'pearson':
        # Add up all the preferences
        sum1 = sum([obj[person1][movie] for movie in shared_movies])
        sum2 = sum([obj[person2][movie] for movie in shared_movies])

        # Sum up the squares
        sum1_of_squares = sum([pow(obj[person1][movie], 2) for movie in shared_movies])
        sum2_of_squares = sum([pow(obj[person2][movie], 2) for movie in shared_movies])

        # Sum up the products
        sum_of_products = sum([obj[person1][movie] * obj[person2][movie] for movie in shared_movies])

        # Calculate the Pearson Correlation Coefficient
        num = sum_of_products - (sum1 * sum2 / n)
        den = sqrt((sum1_of_squares - pow(sum1, 2) / n) * (sum2_of_squares - pow(sum2, 2) / n))
        return num / den if den != 0 else 0

    # Euclidean Distance Score (Return a distance-based similarity score) : Use movies as axes in a chart
    else:
        sum_of_squares = sum([pow(obj[person1][movie] - obj[person2][movie], 2) for movie in shared_movies])
        return 1 / (1 + sqrt(sum_of_squares))

# Return the best matches for `person`
def get_top_matches(obj, person, n=5, method='pearson'):
    scores = [(calculate_similarity(obj, person, other, method), other) for other in obj if other != person]

    return sorted(scores, reverse=True)[:n]

# Get Recommendations for `person` by using a weighted average of every other people's rankings
def get_recommendations(obj, person, method='pearson'):
    sum_of_weighted_scores = {}
    sum_of_similarities = {}

    for other in obj:
        # Don't compare me to myself
        if other == person:
            continue

        # Calculate the similarity score for `person1` and `person2`
        similarity = calculate_similarity(obj, person, other, method)

        # Ignore scores of zero or lower
        if similarity <= 0:
            continue

        for movie in obj[other]:
            # Exclude movies I've seen before
            if movie in obj[person] and obj[person][movie] != 0:
                continue

            # Sum of weighted scores
            sum_of_weighted_scores.setdefault(movie, 0)
            sum_of_weighted_scores[movie] += similarity * obj[other][movie]

            # Sum of similarities
            sum_of_similarities.setdefault(movie, 0)
            sum_of_similarities[movie] += similarity

    # Create the list of normalized scores (with the corresponding movie)
    rankings = [(sum_of_weighted_scores[movie] / sum_of_similarities[movie], movie) for movie in sum_of_weighted_scores]

    # Return the sorted list
    return sorted(rankings, reverse=True)

# Transform `obj` to new dictionary with person and movie swapped
def transform_obj(obj):
    transformed_obj = {}
    for person in obj:
        for movie in obj[person]:
            transformed_obj.setdefault(movie, {})
            transformed_obj[movie][person] = obj[person][movie]
    return transformed_obj
