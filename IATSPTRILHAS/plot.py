import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def plot_tsp_path(path, coordinates, image_path, cost):
    img = mpimg.imread(image_path)
    fig, ax = plt.subplots(figsize=(7, 14))  # Ajuste proporcional à imagem

    # Plot the map (invertendo os eixos)
    ax.imshow(img, extent=[0, 305, 0, 151])  # Agora X vai de 0 a 305 e Y de 0 a 151

    # Plot the nodes (invertendo X e Y)
    for city, (x, y) in zip(path, coordinates):
        ax.plot(y, x, 'bo')  # Agora Y é X e X é Y

    # plot the edges (linhas conectando os nós, também invertidas)
    for i in range(len(path) - 1):
        city1 = path[i]
        city2 = path[i + 1]
        x1, y1 = coordinates[i]
        x2, y2 = coordinates[i + 1]
        ax.plot([y1, y2], [x1, x2], 'r-')  # Inverteu para alinhar com a imagem

    # Conectar a última e a primeira cidade
    x1, y1 = coordinates[-1]
    x2, y2 = coordinates[0]
    ax.plot([y1, y2], [x1, x2], 'r-')

    # Anotar o custo
    cost_text = 'Total Cost: {:.2f}'.format(cost)
    ax.text(0.5, -0.1, cost_text, ha='center', va='center', transform=ax.transAxes,
            bbox=dict(facecolor='white', alpha=0.5, edgecolor='white', boxstyle='round4'))

    plt.title('TSP Path (Eixos Invertidos)')
    plt.show()



def plot_genetic_diversity(genetic_diversity_values):
    """
    Plot the genetic diversity over generations.

    Parameters:
    - genetic_diversity_values: List of genetic diversity values for each generation.
    """
    generations = range(1, len(genetic_diversity_values) + 1)
    plt.plot(generations, genetic_diversity_values, marker='o')
    plt.title('Genetic Diversity Over Generations')
    plt.xlabel('Generation')
    plt.ylabel('Genetic Diversity')
    plt.xticks(generations)
    plt.show()