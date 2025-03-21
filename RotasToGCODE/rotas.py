import re
import os

# ====== CONFIGURAÇÃO ======
arquivo_pontos = "pontos.txt"  # Nome do arquivo que contém os pontos
limite_distancia = 6.0  # Distância acima da qual o Z sobe antes do movimento


# Obtém o diretório do script atual
diretorio_script = os.path.dirname(os.path.abspath(__file__))

# Caminho completo do arquivo de pontos
caminho_pontos = os.path.join(diretorio_script, arquivo_pontos)

# ====== LER O ARQUIVO DE PONTOS ======
ponto_dict = {}
try:
    with open(arquivo_pontos, "r") as f:
        pontos_txt = f.read()

    # Parse dos pontos no formato "PontoX: (X, Y)"
    for match in re.finditer(r"Ponto(\d+):\s*\((\d+),\s*(\d+)\)", pontos_txt):
        nome = f"Ponto{match.group(1)}"
        x = int(match.group(2)) / 10.0
        y = int(match.group(3)) / 10.0
        ponto_dict[nome] = (x, y)

except FileNotFoundError:
    raise FileNotFoundError(f"Arquivo '{arquivo_pontos}' não encontrado na pasta do script!")

# ====== DEFINIR A ROTA (ESTA DEVE SER ALTERADA CONFORME O USO) ======
rota_str = """Ponto1 -> Ponto72 -> Ponto76 -> Ponto129 -> Ponto161 -> Ponto32 -> Ponto34 -> Ponto35 -> Ponto41 -> Ponto77 -> Ponto212 -> Ponto24 -> Ponto26 -> Ponto58 -> Ponto57 -> Ponto75 -> Ponto89 -> Ponto160 -> Ponto152 -> Ponto13 -> Ponto201 -> Ponto189 -> Ponto199 -> Ponto209 -> Ponto214 -> Ponto4 -> Ponto44 -> Ponto95 -> Ponto230 -> Ponto229 -> Ponto211 -> Ponto165 -> Ponto141 -> Ponto94 -> Ponto25 -> Ponto54 -> Ponto22 -> Ponto167 -> Ponto220 -> Ponto221 -> Ponto224 -> Ponto148 -> Ponto144 -> Ponto106 -> Ponto10 -> Ponto36 -> Ponto113 -> Ponto192 -> Ponto93 -> Ponto14 -> Ponto114 -> Ponto191 -> Ponto202 -> Ponto154 -> Ponto166 -> Ponto170 -> Ponto162 -> Ponto150 -> Ponto42 -> Ponto194 -> Ponto12 -> Ponto112 -> Ponto92 -> Ponto198 -> Ponto225 -> Ponto172 -> Ponto128 -> Ponto84 -> Ponto80 -> Ponto136 -> Ponto168 -> Ponto208 -> Ponto188 -> Ponto184 -> Ponto226 -> Ponto223 -> Ponto100 -> Ponto120 -> Ponto102 -> Ponto103 -> Ponto121 -> Ponto122 -> Ponto134 -> Ponto130 -> Ponto126 -> Ponto39 -> Ponto157 -> Ponto153 -> Ponto169 -> Ponto177 -> Ponto88 -> Ponto65 -> Ponto74 -> Ponto123 -> Ponto111 -> Ponto193 -> Ponto46 -> Ponto96 -> Ponto38 -> Ponto149 -> Ponto145 -> Ponto137 -> Ponto107 -> Ponto85 -> Ponto204 -> Ponto110 -> Ponto98 -> Ponto97 -> Ponto142 -> Ponto146 -> Ponto138 -> Ponto158 -> Ponto178 -> Ponto186 -> Ponto174 -> Ponto195 -> Ponto206 -> Ponto53 -> Ponto64 -> Ponto69 -> Ponto21 -> Ponto19 -> Ponto16 -> Ponto99 -> Ponto117 -> Ponto118 -> Ponto87 -> Ponto104 -> Ponto163 -> Ponto143 -> Ponto71 -> Ponto29 -> Ponto28 -> Ponto23 -> Ponto55 -> Ponto70 -> Ponto151 -> Ponto159 -> Ponto175 -> Ponto222 -> Ponto218 -> Ponto179 -> Ponto45 -> Ponto203 -> Ponto11 -> Ponto5 -> Ponto116 -> Ponto109 -> Ponto81 -> Ponto90 -> Ponto185 -> Ponto181 -> Ponto173 -> Ponto133 -> Ponto33 -> Ponto2 -> Ponto3 -> Ponto63 -> Ponto67 -> Ponto125 -> Ponto79 -> Ponto83 -> Ponto105 -> Ponto139 -> Ponto135 -> Ponto127 -> Ponto131 -> Ponto59 -> Ponto60 -> Ponto30 -> Ponto62 -> Ponto66 -> Ponto180 -> Ponto176 -> Ponto140 -> Ponto132 -> Ponto147 -> Ponto155 -> Ponto78 -> Ponto73 -> Ponto18 -> Ponto49 -> Ponto50 -> Ponto20 -> Ponto51 -> Ponto7 -> Ponto15 -> Ponto43 -> Ponto108 -> Ponto47 -> Ponto37 -> Ponto8 -> Ponto205 -> Ponto6 -> Ponto207 -> Ponto219 -> Ponto217 -> Ponto197 -> Ponto183 -> Ponto187 -> Ponto171 -> Ponto82 -> Ponto52 -> Ponto17 -> Ponto48 -> Ponto119 -> Ponto101 -> Ponto40 -> Ponto227 -> Ponto190 -> Ponto200 -> Ponto228 -> Ponto210 -> Ponto196 -> Ponto216 -> Ponto215 -> Ponto182 -> Ponto9 -> Ponto213 -> Ponto86 -> Ponto68 -> Ponto91 -> Ponto115 -> Ponto56 -> Ponto27 -> Ponto61 -> Ponto31 -> Ponto124 -> Ponto156 -> Ponto164 -> Ponto1"""

rota = [p.strip() for p in rota_str.split("->")]

# ====== GERAÇÃO DO GCODE ======
nc_lines = ["(Generated NC Program)"]
z_position = 0  # Estado inicial do eixo Z

for i, ponto in enumerate(rota):
    if ponto not in ponto_dict:
        nc_lines.append(f"(ERRO: {ponto} não encontrado)")
        continue

    x, y = ponto_dict[ponto]

    if i == 0:
        nc_lines.append(f"G0 X{x:.1f} Y{y:.1f}")  # Movimento inicial rápido
    else:
        # Calcula a distância do último ponto
        x_ant, y_ant = ponto_dict[rota[i - 1]]
        distancia = ((x - x_ant) ** 2 + (y - y_ant) ** 2) ** 0.5

        if distancia > limite_distancia:
            nc_lines.append("G0 Z1.0")  # Levanta o eixo Z
            z_position = 1

        nc_lines.append(f"G0 X{x:.1f} Y{y:.1f}")  # Movimento linear

        if distancia > limite_distancia and z_position == 1:
            nc_lines.append("G0 Z0.0")  # Abaixa o eixo Z de volta
            z_position = 0

# ====== SALVAR O GCODE EM ARQUIVO ======
caminho_nc = os.path.join(diretorio_script, "rota_gerada2.nc")

with open(caminho_nc, "w") as f:
    f.write("\n".join(nc_lines))

caminho_nc  # Caminho do arquivo NC salvo