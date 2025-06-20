# Alfabeto dos ingredientes
alfabeto = ['a', 'p', 'o', 'd', 'c', 's', '_']  # '_' é espaço em branco na fita

# Leitura do arquivo da máquina de Turing
def ler_maquina_turing(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()

        linhas = [linha.strip() for linha in linhas if linha.strip()]

        estado_inicial = None
        estados_finais = set()
        dicionario_transicoes = {}

        i = 0

        # Primeira linha: Q: lista de estados
        if linhas[i].startswith('Q:'):
            estados = linhas[i][2:].strip().split()
            i += 1

        # Segunda linha: I: estado inicial
        if linhas[i].startswith('I:'):
            estado_inicial = linhas[i][2:].strip()
            i += 1

        # Terceira linha: F: estados finais
        if linhas[i].startswith('F:'):
            estados_finais_str = linhas[i][2:].strip()
            if estados_finais_str:
                estados_finais = set(estados_finais_str.split())
            i += 1

        # Resto: transições
        while i < len(linhas):
            linha = linhas[i]
            if '->' in linha:
                partes = linha.split('->')
                chave = tuple(partes[0].strip().split())  # (estado_atual, simbolo_lido)
                resultado = partes[1].strip().split()     # (novo_estado, simbolo_escrito, direção)

                if len(chave) == 2 and len(resultado) == 3:
                    dicionario_transicoes[(chave[0], chave[1])] = (resultado[0], resultado[1], resultado[2])
            i += 1

        return estado_inicial, estados_finais, dicionario_transicoes

    except Exception as e:
        print(f"Erro: {e}")
        return None, None, None


def imprime_dicionario(dicionario_transicoes):
    print("\n=== DICIONÁRIO DE TRANSIÇÕES ===")
    for chave, valor in dicionario_transicoes.items():
        print(f"{chave} -> {valor}")


def executar_maquina_turing():
    nome_arquivo = 'maquina_turing.txt'
    estado_inicial, estados_finais, dicionario = ler_maquina_turing(nome_arquivo)

    if estado_inicial is None:
        print("Erro ao carregar a máquina de Turing.")
        return

    # Inicializa a fita com espaços em branco e entrada inicial
    entrada = input("Digite os ingredientes (ex.: apdc): ").strip().lower()
    fita = list(entrada) + ['_'] * 20  # Acrescenta espaços em branco à direita
    cabecote = 0
    estado_atual = estado_inicial

    print(f"\nEstado Inicial: {estado_inicial}")
    print(f"Estados Finais: {estados_finais}")
    imprime_dicionario(dicionario)

    # Execução
    while True:
        simbolo_lido = fita[cabecote] if 0 <= cabecote < len(fita) else '_'

        chave = (estado_atual, simbolo_lido)

        if chave in dicionario:
            novo_estado, simbolo_escrito, direcao = dicionario[chave]
            print(f"\nLendo '{simbolo_lido}' no estado '{estado_atual}' -> escreve '{simbolo_escrito}', vai para '{novo_estado}', move '{direcao}'")

            # Escrever na fita
            fita[cabecote] = simbolo_escrito

            # Atualizar estado
            estado_atual = novo_estado

            # Mover cabeçote
            if direcao.upper() == 'D':
                cabecote += 1
                if cabecote >= len(fita):
                    fita.append('_')
            elif direcao.upper() == 'E':
                cabecote -= 1
                if cabecote < 0:
                    fita = ['_'] + fita
                    cabecote = 0
            else:
                print("Direção inválida. Use 'D' (Direita) ou 'E' (Esquerda).")
                break

            # Mostrar estado da fita
            print("Fita:", ' '.join(fita))
            print("       " + "    " * cabecote + "^ (Cabeçote)")

        else:
            print(f"\nSem transição definida para ({estado_atual}, {simbolo_lido}). Encerrando.")
            break

        if estado_atual in estados_finais:
            print(f"\nEstado '{estado_atual}' é final. Máquina aceita a entrada!")
            break


# Executa a máquina
executar_maquina_turing()
