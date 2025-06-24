# 1 - criar o alfabeto
''' Ingredientes
  a - água
  p - pétalas
  o - óleo
  d - dente de dragão
  c - costela de adão
  s - sapo
'''

# Le o arquivo
def ler_automato(nome_arquivo):

    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        # Remove linhas vazias e espaços em branco
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
            if estados_finais_str:  # Se não estiver vazio
                estados_finais = set(estados_finais_str.split())
            i += 1
        
        # Resto das linhas: transições
        while i < len(linhas):
            linha = linhas[i]
            if '->' in linha:
                # Parse da transição: "estado_origem -> estado_destino | símbolos"
                partes = linha.split('->')
                estado_origem = partes[0].strip()
                resto = partes[1].strip()
                
                # Separar estado destino dos símbolos
                if '|' in resto:
                    estado_destino, simbolos_str = resto.split('|', 1)
                    estado_destino = estado_destino.strip()
                    simbolos = simbolos_str.strip().split()
                    
                    # Adicionar cada transição ao dicionário
                    for simbolo in simbolos:
                        chave = (estado_origem, simbolo)
                        dicionario_transicoes[chave] = estado_destino
            i += 1
        
        return estado_inicial, estados_finais, dicionario_transicoes
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None, None, None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None, None, None
    
def imprime_dicionario(dicionario_transicoes):
    print("\n╔══════════════════════════════════════════════╗")
    print("║          DICIONÁRIO DE TRANSIÇÕES            ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  Estado Atual  │  Símbolo  │ Próximo Estado  ║")
    print("╠═════════════════╪═══════════╪════════════════╣")
    
    for chave, destino in dicionario_transicoes.items():
        estado_atual, simbolo = chave
        print(f"║ {estado_atual:^15} │ {simbolo:^9} │ {destino:^14} ║")
    
    print("╚═════════════════╧═══════════╧════════════════╝")
    print("╔══════════════════════════════════════════════╗")
    print("║  Estado Inicial: I                           ║")
    print("║  Estado Final: F                             ║")
    print("╚══════════════════════════════════════════════╝")


def realizar_transicao(estado_atual, simbolo, dicionario):
    chave = (estado_atual, simbolo)
    if chave in dicionario:
        prox_estado = dicionario[chave]
        return prox_estado
    else:# O simbolo ou o estado nao existe
        return None
    


def executar_simulador_arquivo(alfabeto, ingredientes):
    nome_arquivo = 'Entradas/automato.txt'
    estado_inicial, estados_finais, dicionario_transicoes = ler_automato(nome_arquivo)

    if estado_inicial is None:
        print("Não foi possível carregar o autômato.")
        return

    ingredientes = []
    estado_atual = estado_inicial
    atingiu_estado_final = False

    imprime_dicionario(dicionario_transicoes)

    while True:
        ingrediente = input("\nInsira um ingrediente (a, p, o, d, c, s): ").strip().lower()

        if ingrediente not in alfabeto:
            print(f"Ingrediente '{ingrediente}' inválido! Ingredientes válidos: {', '.join(alfabeto)}")
            continue

        ingredientes.append(ingrediente)

        novo_estado = realizar_transicao(estado_atual, ingrediente, dicionario_transicoes)
        print(f"Estado atual após o ingrediente '{ingrediente}': {novo_estado}")
        estado_atual = novo_estado

        if estado_atual in estados_finais:
            print("Parabéns! Você alcançou um estado final!")
            atingiu_estado_final = True
            break

        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            print("\nEncerrando a simulação...")
            break

    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║ RESULTADO FINAL                                                                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    print("════════════════════════════════════════════════════════════════════════════════════════")
    print(f" Ingredientes inseridos: {ingredientes}")
    print(f" Estado final da execução: {estado_atual}")
    if estado_atual == 'erro':
        print(" Atenção: O autômato entrou em um estado de erro (transição inválida).")
    elif not atingiu_estado_final:
        print(" Atenção: A execução terminou sem atingir um estado final. :( ")
    print("════════════════════════════════════════════════════════════════════════════════════════")
