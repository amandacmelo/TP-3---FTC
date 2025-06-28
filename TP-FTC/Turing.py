# Alfabeto dos ingredientes



# Leitura do arquivo da máquina de Turing
def ler_maquina_turing(linhas):
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

def executar_maquina_turing(conteudo_arquivo):
    estado_inicial, estados_finais, dicionario = ler_maquina_turing(conteudo_arquivo)
    if dicionario is None:
        print(" Erro: Arquivo maquina_turing.txt não encontrado ou está mal formatado.")
        return
    estado_atual = estado_inicial

    imprime_dicionario(dicionario)  #  Imprime o dicionário no início

    fita = ['_'] * 50
    cabecote = 0
    estado_invalido = False  # Indicador de erro

    while True:
        simbolo = input("Insira um ingrediente (a, p, o, d, c, s): ").strip().lower()

        if simbolo not in ['a', 'p', 'o', 'd', 'c', 's']:
            print(" Ingrediente inválido! Insira apenas (a, p, o, d, c, s).\n")
            continue
        
        if simbolo in ['a', 'p', 'o', 'd', 'c', 's']:
            fita[cabecote] = simbolo
            chave = (estado_atual, simbolo)

        if chave in dicionario:
            novo_estado, simbolo_escrito, direcao = dicionario[chave]
            fita[cabecote] = simbolo_escrito
            estado_atual = novo_estado
            cabecote = move_cabecote(cabecote, direcao)
            print(f"Estado atual após o ingrediente '{simbolo}': {estado_atual}")
        else:
            print(f"⚠️ Atenção: Transição inexistente para ({estado_atual}, '{simbolo}'). Cabeçote permanece.")
            estado_invalido = True  # Marca que houve transição inválida

        if estado_atual in estados_finais:
            print("\n✅ Atingiu um estado final!")
            break

        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            break

    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║ RESULTADO FINAL                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    intensidade = cabecote + 1
    print(f" -> Intensidade da poção: {intensidade} 🔥 (Quanto mais à direita, mais intensa!)     ")
    print(f" -> Estado final da execução: {estado_atual}                                          ")
    if estado_invalido:
        print("  Atenção: Houve pelo menos uma transição inválida durante a execução.              ")
    elif estado_atual not in estados_finais:
        print("  Atenção: A execução terminou sem atingir um estado final.                         ")
    print("\n Fita Final: ", ' '.join(fita), '\n')
    # print("              " + "    " * cabecote + "^ (Cabeçote Final)")
    print("════════════════════════════════════════════════════════════════════════════════════════")


def move_cabecote(cabecote, direcao):
    if direcao.upper() == 'D':
        cabecote += 1
    elif direcao.upper() == 'E':
        cabecote -= 1
        if cabecote < 0:
            cabecote = 0  # Não deixa o cabeçote ir antes da posição 0
    return cabecote