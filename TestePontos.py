import random
import matplotlib.pyplot as plt

def generate_points(x_min, x_max, y_min, y_max, num_points, distribution='random'):
    """
    Gera pontos dentro de uma área definida pelos limites.
    :param x_min: Coordenada mínima em x
    :param x_max: Coordenada máxima em x
    :param y_min: Coordenada mínima em y
    :param y_max: Coordenada máxima em y
    :param num_points: Número de pontos a serem gerados
    :param distribution: Tipo de distribuição ('random' ou 'grid')
    :return: Lista de tuplas representando os pontos
    """
    points = []
    
    if distribution == 'random':
        for _ in range(num_points):
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            points.append((x, y))
    elif distribution == 'grid':
        cols = int(num_points ** 0.5)
        rows = (num_points // cols) + (1 if num_points % cols else 0)
        x_spacing = (x_max - x_min) / max(cols - 1, 1)
        y_spacing = (y_max - y_min) / max(rows - 1, 1)
        for i in range(rows):
            for j in range(cols):
                if len(points) >= num_points:
                    break
                x = x_min + j * x_spacing
                y = y_min + i * y_spacing
                points.append((x, y))
    else:
        raise ValueError("Distribuição inválida. Use 'random' ou 'grid'.")
    
    return points

def plot_points(points):
    """
    Plota os pontos gerados para visualização.
    """
    x_vals, y_vals = zip(*points)
    plt.scatter(x_vals, y_vals, c='blue', marker='o')
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Pontos Gerados')
    plt.grid()
    plt.show()

if __name__ == "__main__":
    # Definir a área e número de pontos
    x_min, x_max = 0, 100
    y_min, y_max = 0, 100
    num_points = 50
    
    # Gerar pontos
    points = generate_points(x_min, x_max, y_min, y_max, num_points, distribution='random')
    
    # Exibir os pontos gerados
    print("Pontos Gerados:", points)
    
    # Plotar os pontos
    plot_points(points)
    