import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

def generate_ordered_points(x_min, x_max, y_min, y_max, num_points, restricted_areas=None, spacing=10, fileira_dist=15):
    points = []
    
    # Gerar as fileiras lado a lado
    y_values = list(range(y_min, y_max, spacing))
    
    for y in y_values:
        # Fileira da esquerda
        x_values_left = list(range(x_min, x_max, spacing))
        # Fileira da direita (deslocada)
        x_values_right = list(range(x_min + fileira_dist, x_max + fileira_dist, spacing))
        
        # Gerando os pontos para a fileira esquerda
        for x in x_values_left:
            in_restricted_area = any(x_min_r <= x <= x_max_r and y_min_r <= y <= y_max_r for x_min_r, x_max_r, y_min_r, y_max_r in (restricted_areas or []))
            if not in_restricted_area:
                points.append((x, y))
        
        # Gerando os pontos para a fileira direita
        for x in x_values_right:
            in_restricted_area = any(x_min_r <= x <= x_max_r and y_min_r <= y <= y_max_r for x_min_r, x_max_r, y_min_r, y_max_r in (restricted_areas or []))
            if not in_restricted_area:
                points.append((x, y))
    
    return points[:num_points]

def save_points_to_file(points, filename="pontos.txt"):
    if points:
        with open(filename, "w") as file:
            for i, (x, y) in enumerate(points, 1):
                file.write(f"Ponto{i}: ({x}, {y})\n")
        print(f"Pontos salvos em {filename}")
    else:
        print("Nenhum ponto válido gerado para salvar.")

def plot_points(points, restricted_areas=None, background_image=None):
    plt.figure(figsize=(8, 8))
    
    if background_image:
        try:
            img = mpimg.imread(background_image)
            plt.imshow(img, extent=[0, 305, 0, 151], aspect='auto', origin='upper')
        except FileNotFoundError:
            print(f"Erro: Imagem '{background_image}' não encontrada.")
    
    if points:
        x_vals, y_vals = zip(*points)
        plt.scatter(x_vals, y_vals, c='blue', marker='o', label='Pontos Válidos')
    
    if restricted_areas:
        for x_min_r, x_max_r, y_min_r, y_max_r in restricted_areas:
            plt.fill_between([x_min_r, x_max_r], y_min_r, y_max_r, color='red', alpha=0.3, label='Área Restrita')
    
    plt.xlim(0, 305)
    plt.ylim(0, 151)
    plt.legend()
    plt.show()

if __name__ == "__main__":
    x_min, x_max = 0, 305
    y_min, y_max = 0, 151
    num_points = 900  # Número de pontos ordenados a serem gerados
    
    restricted_areas = [(0, 15, 0, 151), (0, 305, 0, 27), (0, 305, 115, 151), (290, 305, 0, 151),
                        (20, 55, 33, 105), (59, 137, 33, 51), (240, 283, 33, 110), (60, 230, 57, 115), (142, 230, 27, 57)]
    
    # Gerar pontos em fileiras duplas lado a lado
    points = generate_ordered_points(x_min, x_max, y_min, y_max, num_points, restricted_areas=restricted_areas, spacing=3, fileira_dist=5)
    
    # Salvar pontos em arquivo
    save_points_to_file(points, "pontos.txt")
    
    # Plotar pontos no gráfico
    background_image = "background.png"  # Substitua pelo caminho correto da imagem
    plot_points(points, restricted_areas, background_image)
