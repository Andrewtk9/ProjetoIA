import random
import matplotlib.pyplot as plt
import math

def generate_points(x_min, x_max, y_min, y_max, num_points, distribution='random', restricted_areas=None, min_distance=2):
    points = []
    
    def is_in_restricted_area(x, y):
        if restricted_areas:
            for rx_min, rx_max, ry_min, ry_max in restricted_areas:
                if rx_min <= x <= rx_max and ry_min <= y <= ry_max:
                    return True
        return False
    
    def has_min_distance(x, y):
        for px, py in points:
            if math.dist((x, y), (px, py)) < min_distance:
                return False
        return True
    
    if distribution == 'random':
        while len(points) < num_points:
            x = random.uniform(x_min, x_max)
            y = random.uniform(y_min, y_max)
            if not is_in_restricted_area(x, y) and has_min_distance(x, y):
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
                if not is_in_restricted_area(x, y) and has_min_distance(x, y):
                    points.append((x, y))
    else:
        raise ValueError("Distribuição inválida. Use 'random' ou 'grid'.")
    
    return points

def save_points_to_file(points, filename="pontos.txt"):
    with open(filename, "w") as file:
        for i, (x, y) in enumerate(points, start=1):
            file.write(f"Ponto{i}: ({int(x)}, {int(y)})\n")
    print(f"Pontos salvos em {filename}")

def plot_points(points, restricted_areas=None):
    x_vals, y_vals = zip(*points)
    plt.scatter(x_vals, y_vals, c='blue', marker='o', label='Pontos Válidos')
    
    if restricted_areas:
        for rx_min, rx_max, ry_min, ry_max in restricted_areas:
            plt.fill_between([rx_min, rx_max], ry_min, ry_max, color='red', alpha=0.3, label='Área Restrita')
    
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Pontos Gerados')
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    x_min, x_max = 0, 100
    y_min, y_max = 0, 100
    num_points = 200
    
    restricted_areas = [(0, 20, 0, 100), (0, 100, 0, 40), (0, 100, 70, 100), (80, 100, 0, 100),
                        (25, 32, 45, 60), (35, 60, 45, 52), (65, 72, 45, 60), (35, 60, 57, 80)]
    
    points = generate_points(x_min, x_max, y_min, y_max, num_points, distribution='random',
                             restricted_areas=restricted_areas, min_distance=2)
    
    save_points_to_file(points, "pontos.txt")
    plot_points(points, restricted_areas)