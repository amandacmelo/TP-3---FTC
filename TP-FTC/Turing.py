# Alfabeto dos ingredientes



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
    print("\n╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║                          DICIONÁRIO DE TRANSIÇÕES                            ║")
    print("╠═════════════════╦════════════╦═══════════════════════════════════════════════╣")
    print("║  Estado Atual   │  Símbolo   │   (Próximo Estado, Ingrediente, Direção)      ║")
    print("╠═════════════════╬════════════╬═══════════════════════════════════════════════╣")
    
    for chave, destino in dicionario_transicoes.items():
        estado_atual, simbolo = chave
        proximo_estado, simbolo_escrito, direcao = destino
        print(f"║ {estado_atual:^15} │ {simbolo:^10} │ ({proximo_estado}, {simbolo_escrito}, {direcao}){' ' * (39 - len(str(proximo_estado + simbolo_escrito + direcao)))} ║")
    
    print("╚═════════════════╩════════════╩═══════════════════════════════════════════════╝")
    print("╔══════════════════════════════════════════════════════════════════════════════╗")
    print("║  Estado Inicial: I                                                           ║")
    print("║  Estado Final: F                                                             ║")
    print("╚══════════════════════════════════════════════════════════════════════════════╝")

def executar_maquina_turing():
    estado_inicial, estados_finais, dicionario = ler_maquina_turing('Entradas/maquina_turing.txt')
    estado_atual = estado_inicial

    imprime_dicionario(dicionario)  # 🧠 Imprime o dicionário no início

    fita = ['_'] * 50
    cabecote = 0

    print(f"\nEstado Inicial: {estado_inicial}")

    simbolo = input("Insira o símbolo do primeiro ingrediente da receita: ").strip().lower()
    fita[cabecote] = simbolo

    chave = (estado_atual, simbolo)

    if chave in dicionario:
        novo_estado, simbolo_escrito, direcao = dicionario[chave]
        fita[cabecote] = simbolo_escrito
        estado_atual = novo_estado
        cabecote = move_cabecote(cabecote, direcao)
    else:
        estado_atual = 'erro'

    print(f"Estado atual após o primeiro ingrediente: {estado_atual}")

    while True:
        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()

        if resposta != 's':
            print("\nSaindo da máquina...")
            print(f"Estado Atual: {estado_atual}")
            print(f"Estado Inicial: {estado_inicial}")

            print("\n=== RESULTADO FINAL ===")
            print("Fita Final:", ' '.join(fita))
            print("              " + "    " * cabecote + "^ (Cabeçote Final)")

            intensidade = cabecote + 1
            print(f"\n>> Intensidade da poção: {intensidade+1} 🔥 (Quanto mais à direita, mais intensa!)")
            break

        simbolo = input("Insira um ingrediente (a, p, o, d, c, s): ").strip().lower()
        fita[cabecote] = simbolo

        chave = (estado_atual, simbolo)

        if chave in dicionario:
            novo_estado, simbolo_escrito, direcao = dicionario[chave]
            fita[cabecote] = simbolo_escrito
            estado_atual = novo_estado
            cabecote = move_cabecote(cabecote, direcao)
        else:
            estado_atual = 'erro'

        print(f"Estado atual após o ingrediente '{simbolo}': {estado_atual}")

        if estado_atual in estados_finais:
            print("✅ Atingiu um estado final!")
            intensidade = cabecote + 1
            print(f"\n>> Intensidade da poção: {intensidade} 🔥 (Quanto mais à direita, mais intensa!)")
            break

        if estado_atual == 'erro':
            print("❌ Erro: Ingrediente inválido ou transição inexistente.")
            break


def move_cabecote(cabecote, direcao):
    if direcao.upper() == 'D':
        cabecote += 1
    elif direcao.upper() == 'E':
        cabecote -= 1
        if cabecote < 0:
            cabecote = 0  # Não deixa o cabeçote ir antes da posição 0
    return cabecote
