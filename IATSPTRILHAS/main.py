import re
from graph import Graph
from genetic_algorithm_tsp import GeneticAlgorithmTSP
from plot import plot_tsp_path, plot_genetic_diversity
from collections import OrderedDict


def main():
    # read cities from file
    with open('cities.txt', 'r') as file:
        cities_data = file.read()

    # 33 - 126 visible characters (94 total)

    # define a regular expression pattern to extract city information
    city_pattern = re.compile(r'(\w+):\s\((\d+),\s(\d+)\)')

    # extract city information from the data using the pattern
    cities = city_pattern.findall(cities_data)

    if len(cities) > 230:
        raise ValueError("Cannot accept more cities.")

    # create a mapping from city names to characters using OrderedDict
    city_mapping = OrderedDict((city[0], chr(i + 33)) for i, city in enumerate(cities))

    # create a graph instance and add nodes with city names and coordinates
    germany_graph = Graph(len(cities), False)

    for city, x, y in cities:
        germany_graph.add_node(city_mapping[city], int(x), int(y))

    # set the start city for the TSP algorithm
    germany_graph.start_city = city_mapping['Ponto1']

    # create an instance of the GeneticAlgorithmTSP class
    ga_tsp_germany = GeneticAlgorithmTSP(
        graph=germany_graph,
        city_names=[city for city, _, _ in cities], # pass the list of city names
<<<<<<< HEAD
        generations=500,
        population_size=500,
        tournament_size=2,
        mutationRate=0.9,
        fitness_selection_rate=0.1,
=======
        generations=1000,
        population_size=500,
        tournament_size=10,
        mutationRate=0.7,
        fitness_selection_rate=0.25,
>>>>>>> bd0c405d1ed2ecf1249a0eaccb08541b6e779441
    )

    # find the fittest path using the genetic algorithm
    fittest_path, path_cost = ga_tsp_germany.find_fittest_path(germany_graph)

    # get genetic diversity values for each generation
    genetic_diversity_values = ga_tsp_germany.get_genetic_diversity_values()

    # display the results
    formatted_path = ' -> '.join(fittest_path)
    print('\nPath: {0}\nCost: {1}'.format(formatted_path, path_cost))

    # create a dictionary with city coordinates
    coordinates_dict = {city: (int(x), int(y)) for city, x, y in cities}

    # create a list of coordinates for the fittest path
    coordinates_list = [coordinates_dict[city] for city in fittest_path]

    # plot the TSP path with nodes, edges, and cost annotation
    plot_tsp_path(fittest_path, coordinates_list, 'background.png', path_cost)

    # plot the genetic diversity over generations
    plot_genetic_diversity(genetic_diversity_values)

if __name__ == "__main__":
    main()