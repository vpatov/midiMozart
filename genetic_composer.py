## 1) Test each sample and assign a fitness score (0.0 - 1.0)
## 2) Select two samples from the population, with more fit samples more likely to be selected.
## 3) Given a certain crossover rate, merge the two samples.
## 4) Return the child sample to a new population pool, part of a new generation.


def gen_random_population(population_size,member_size):
    """
    Generate a random population to be used as the seed for genetic improvement.
    :param population_size: The amount of samples in the population
    :param member_size: The length, in seconds (approximately), of each member of the population
    :return: a list of samples
    """
    population = []