import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def ler_automato_mealy(linhas):
    """
    Lê um autômato Mealy de um arquivo no formato:
    Q: lista de estados
    I: estado inicial
    estado_origem -> estado_destino | entrada/saida entrada/saida ...
    """
    estado_inicial = None
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
    
    # Resto das linhas: transições Mealy
    while i < len(linhas):
        linha = linhas[i]
        if '->' in linha:
            # Parse da transição: "estado_origem -> estado_destino | entrada/saida entrada/saida"
            partes = linha.split('->')
            estado_origem = partes[0].strip()
            resto = partes[1].strip()
            
            # Separar estado destino das transições entrada/saida
            if '|' in resto:
                estado_destino, transicoes_str = resto.split('|', 1)
                estado_destino = estado_destino.strip()
                transicoes = transicoes_str.strip().split()
                
                # Processar cada transição entrada/saida
                for transicao in transicoes:
                    if '/' in transicao:
                        entrada, saida = transicao.split('/', 1)
                        chave = (estado_origem, entrada)
                        dicionario_transicoes[chave] = (estado_destino, saida)
        i += 1
    
    return estado_inicial, dicionario_transicoes

def classificar_pocao_final(lista_saidas):
    
    #Analisa a lista de saídas (reacoes) e determina a descricao da pocao final com base na reação predominante
    
    if not lista_saidas:
       
        return "Vazio :()"

    # Contar a ocorrência de cada reação
    contagem_reacoes = {}
    for reacao in lista_saidas:
        if reacao not in contagem_reacoes:
            contagem_reacoes[reacao] = 0
        contagem_reacoes[reacao] += 1

    # Encontrar a reação mais frequente
    reacao_predominante = max(contagem_reacoes, key=contagem_reacoes.get)

    # Mapear reação para descrição da poção
    descricao_pocao = {
        'dilui': 'Poção aguada',
        'perfuma': 'Poção perfumada',
        'engrossa': 'Poção espessa',
        'acido': 'Poção ácida',
        'alcalino': 'Poção alcalina',
        'fedido': 'Poção fedida',
        'erro': 'Poção explodiu'
    }

    return descricao_pocao[reacao_predominante]


def imprime_dicionario_mealy(dicionario_transicoes, estado_inicial):
    """Imprime o dicionário de transições Mealy de forma organizada"""
    linhas = []
    linhas.append("╔════════════════╦═══════════╦════════════════╦════════════════╗")
    linhas.append("║  Estado Atual  ║  Entrada  ║ Próximo Estado ║     Saída      ║")
    linhas.append("╠════════════════╬═══════════╬════════════════╬════════════════╣")
    
    for chave, (destino, saida) in dicionario_transicoes.items():
        estado_atual, entrada = chave
        linhas.append(f"║ {estado_atual:^14} ║ {entrada:^9} ║ {destino:^14} ║ {saida:^14} ║")
        linhas.append("╠════════════════╬═══════════╬════════════════╬════════════════╣")
    
    # Remove a última linha de separação e adiciona o fechamento
    linhas[-1] = "╚════════════════╩═══════════╩════════════════╩════════════════╝"
    
    # Imprime todas as linhas da tabela
    for linha in linhas:
        print(linha)
    
    # Informações adicionais
    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"║ Estado Inicial: {estado_inicial:<45}║")
    print("╚══════════════════════════════════════════════════════════════╝")

def realizar_transicao_mealy(estado_atual, entrada, dicionario):
    """
    Realiza uma transição Mealy e retorna o próximo estado e a saída
    """
    chave = (estado_atual, entrada)
    if chave in dicionario:
        proximo_estado, saida = dicionario[chave]
        return proximo_estado, saida
    else:
        return None, None


def executar_simulador_mealy(alfabeto, ingredientes, conteudo_arquivo):
    """Executa o simulador do autômato Mealy"""
    estado_inicial, dicionario_transicoes = ler_automato_mealy(conteudo_arquivo)
    
    if estado_inicial is None:
        print("Não foi possível carregar o autômato.")
        return
    
    # Mostra o dicionário de transições
    imprime_dicionario_mealy(dicionario_transicoes, estado_inicial)

    lista_ingredientes = []
    lista_saidas = []
    estado_atual = estado_inicial
    historico_transicoes = []
    
    
    # Loop para perguntar por mais ingredientes
    while True:
        limpar_tela()
        imprime_dicionario_mealy(dicionario_transicoes, estado_inicial)
        if historico_transicoes != []:
            print("\n╔════════════════════════════════════════════════════════════╗")
            print("║                   📜 HISTÓRICO DE TRANSIÇÕES               ║")
            print("╠════════════╦════════════╦════════════════╦═════════════════╣")
            print("║  Origem    ║  Entrada   ║   Destino      ║      Saída      ║")
            print("╠════════════╬════════════╬════════════════╬═════════════════╣")
            for origem, simb, destino, saida in historico_transicoes:
                nome_ingrediente = ingredientes[simb]['nome']
                print(f"║ {origem:^10} ║ {simb:^10} ║ {destino:^14} ║ {saida:^15} ║")
            print("╚════════════╩════════════╩════════════════╩═════════════════╝")

        ingrediente = input("\nInsira um ingrediente (a, p, o, d, c, s): ").strip().lower()
        if ingrediente not in alfabeto:
            print(f"Ingrediente '{ingrediente}' inválido! Ingredientes válidos: {', '.join(alfabeto)}")
            time.sleep(1)
            continue
        
        lista_ingredientes.append(ingrediente)
        proximo_estado, saida = realizar_transicao_mealy(estado_atual, ingrediente, dicionario_transicoes)

        # Estados de erro ficaram implicitos nessa maquina
        if proximo_estado is None:
            proximo_estado = 'erro'
            saida = "Explosao"

        historico_transicoes.append((estado_atual, ingrediente, proximo_estado, saida))
        estado_atual = proximo_estado
        lista_saidas.append(saida)
        
        print("\n╔════════════════════════════════════════════════════════════╗")
        print("║                   📜 HISTÓRICO DE TRANSIÇÕES               ║")
        print("╠════════════╦════════════╦════════════════╦═════════════════╣")
        print("║  Origem    ║  Entrada   ║   Destino      ║      Saída      ║")
        print("╠════════════╬════════════╬════════════════╬═════════════════╣")
        for origem, simb, destino, saida in historico_transicoes:
            nome_ingrediente = ingredientes[simb]['nome']
            print(f"║ {origem:^10} ║ {simb:^10} ║ {destino:^14} ║ {saida:^15} ║")
        print("╚════════════╩════════════╩════════════════╩═════════════════╝")

            
        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        while resposta not in ('s', 'n'):
            print("Opção inválida! Tente novamente.")
            resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            break
    # Resumo final 
    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                 🌟 RESULTADO FINAL 🌟                                ║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ Estado inicial da execução: {estado_inicial:<57}║")
    print(f"║ Estado final da execução:   {estado_atual:<57}║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    

    print(f"║ Saida:  {classificar_pocao_final(lista_saidas):<77}║")

    # Análise do resultado
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    if estado_atual == 'erro':
        print("║ Resultado:   O autômato entrou em um estado de erro (transição inválida)             ║")
    else:
        print("║ Resultado:   A execução terminou corretamente sem transições inválidas               ║")

    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
 