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
    print("║          DICIONÁRIO DE TRANSIÇÕES           ║")
    print("╠══════════════════════════════════════════════╣")
    print("║  Estado Atual  │  Símbolo  │ Próximo Estado  ║")
    print("╠═════════════════╪═══════════╪════════════════╣")
    
    for chave, destino in dicionario_transicoes.items():
        estado_atual, simbolo = chave
        print(f"║ {estado_atual:^15} │ {simbolo:^9} │ {destino:^14} ║")
    
    print("╚═════════════════╧═══════════╧════════════════╝")


def realizar_transicao(estado_atual, simbolo, dicionario):
    chave = (estado_atual, simbolo)
    if chave in dicionario:
        prox_estado = dicionario[chave]
        return prox_estado
    else:# O simbolo ou o estado nao existe
        return None
    


def executar_simulador_arquivo(alfabeto, ingredientes):
    nome_arquivo = 'automato.txt'
    estado_inicial, estados_finais, dicionario_transicoes = ler_automato(nome_arquivo)
    ingredientes = []
    estado_atual = estado_inicial

    # Pergunta pelo primeiro ingrediente
    imprime_dicionario(dicionario_transicoes)
    primeiro_ingrediente = input("Insira o símbolo do primeiro ingrediente da receita: ").strip().lower()
     #primeiro_ingrediente = input().strip().lower()
    ingredientes.append(primeiro_ingrediente)
    estado_atual = realizar_transicao(estado_inicial, primeiro_ingrediente, dicionario_transicoes)
    print(f"Estado atual após o primeiro ingrediente: {estado_atual}")
    # Loop para perguntar por mais ingredientes
    while True:
        resposta = input("\nDeseja inserir mais um ingrediente (s/n)?").strip().lower()
        #resposta = input().strip().lower()
        
        if resposta == 's':
            ingrediente = input("Insira um ingrediente (a, p, o, d, c, s): ").strip().lower()
            #ingrediente = input().strip().lower()
            ingredientes.append(ingrediente)

            estado_atual = realizar_transicao(estado_atual, ingrediente, dicionario_transicoes)
            print(f"Estado atual após o ingrediente '{ingrediente}': {estado_atual}")
            if estado_atual in estados_finais:
                print("Parabéns! Você alcançou um estado final.")
                break
            if estado_atual is 'erro':
                print("Erro: Ingrediente inválido ou transição inexistente.")
                break
        elif resposta == 'n':
            print("Saindo da máquina")
            print("Estado Atual", estado_atual)
            break
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")
    
    if estado_inicial is not None:
        print(f"Estado Inicial: {estado_inicial}")
        #print(f"Estados Finais: {estados_finais}")
        #imprime_dicionario(dicionario_transicoes)
    else:
        print("Não foi possível carregar o autômato.")
