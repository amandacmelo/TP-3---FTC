import os
import time
# Codigos de cores ANSI
VERMELHO = '\033[91m'
AMARELO = '\033[93m'
RESET = '\033[0m'

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def ler_moore(linhas):
    """
    formato maquina moore
    Q: lista de estados
    I: estado inicial
    F: estados finais
    O: saidas para cada estado (formato: estado=saida)
    transicoes: estado_origem -> estado_destino | simbolos
    
    """

    estados = set()
    estado_inicial = None
    saidas_estados = {}  # Dicionario: estado -> saida
    dicionario_transicoes = {}
    
    i = 0
    
    # Q: lista de estados
    if i < len(linhas) and linhas[i].startswith('Q:'):
        estados_str = linhas[i][2:].strip()
        estados = set(estados_str.split())
        i += 1
    
    # I: estado inicial
    if i < len(linhas) and linhas[i].startswith('I:'):
        estado_inicial = linhas[i][2:].strip()
        i += 1
    
    # O: saidas dos estados
    if i < len(linhas) and linhas[i].startswith('O:'):
        saidas_str = linhas[i][2:].strip()
        
        saidas_items = saidas_str.split()
        for item in saidas_items:
            if '=' in item:
                estado, saida = item.split('=', 1)
                saidas_estados[estado.strip()] = saida.strip()
        i += 1
    
    # transicoes
    while i < len(linhas):
        linha = linhas[i]
        if '->' in linha:
            # "estado_origem -> estado_destino | simbolos"
            partes = linha.split('->')
            estado_origem = partes[0].strip()
            resto = partes[1].strip()
            
            if '|' in resto:
                estado_destino, simbolos_str = resto.split('|', 1)
                estado_destino = estado_destino.strip()
                simbolos = simbolos_str.strip().split()
                
                # adicionando a transicao no dicionario
                for simbolo in simbolos:
                    chave = (estado_origem, simbolo)
                    dicionario_transicoes[chave] = estado_destino
        i += 1
    
    return estado_inicial, saidas_estados, dicionario_transicoes



def imprimeMoore(dicionario_transicoes, saidas_estados, estado_inicial):

    linhas = []
    linhas.append("\n╔════════════════╦═══════════╦════════════════╦════════════════╗")
    linhas.append("║  Estado Atual  ║  Entrada  ║ Próximo Estado ║     Saída      ║")
    linhas.append("╠════════════════╬═══════════╬════════════════╬════════════════╣")

    for (estado_origem, simbolo), estado_destino in dicionario_transicoes.items():
        if estado_destino != 'erro':
            saida_destino = saidas_estados.get(estado_destino, "N/A")

            # Define cor por linha
            if estado_origem == estado_inicial:
                cor = AMARELO
            else:
                cor = RESET

            # Linha colorida completa
            linhas.append(
                f"║ {cor}{estado_origem:^14}{RESET} ║ {cor}{simbolo:^9}{RESET} ║ "
                f"{cor}{estado_destino:^14}{RESET} ║ {cor}{saida_destino:^14}{RESET} ║"
            )
            linhas.append("╠════════════════╬═══════════╬════════════════╬════════════════╣")

    # Corrigir última linha
    linhas[-1] = "╚════════════════╩═══════════╩════════════════╩════════════════╝"

    for linha in linhas:
        print(linha)

    # Informacoes adicionais
    print("╔══════════════════════════════════════════════════════════════╗")
    print(f"║ Estado Inicial: {estado_inicial:<45}║")
    print("╚══════════════════════════════════════════════════════════════╝")

def obter_saida_estado(estado, saidas_estados):
    """
    Obtem a saida associada ao estado atual
    """
    if estado in saidas_estados:
        codigo_saida = saidas_estados[estado]
        
        # Mapear codigos de saida para descricoes simples
        mapeamento_saidas = {
            'inicio': 'Caldeirao preparado para receber ingredientes',
            'processando': 'Processando ingre dientes iniciais...',
            'misturando': 'Misturando componentes ativos...',
            'refinando': 'Refinando a mistura final...',
            'completo': 'Pocao completa e pronta para uso!',
            'erro': 'Erro na preparacao da pocao!'
        }
        
        return mapeamento_saidas.get(codigo_saida, f"Saida: {codigo_saida}")
    else:
        return "Saida nao definida"

def realizar_transicao_moore(estado_atual, simbolo, dicionario):
    chave = (estado_atual, simbolo)
    if chave in dicionario:
        return dicionario[chave]
    else:
        return None

def executar_simulador_moore(alfabeto, ingredientes, conteudo_arquivo):

    # Processar maquina
    estado_inicial, saidas_estados, dicionario_transicoes = ler_moore(conteudo_arquivo)
    
    if estado_inicial is None:
        print("Erro ao carregar maquina de Moore! Verifique o formato do arquivo.")
        return
    
    imprimeMoore(dicionario_transicoes, saidas_estados, estado_inicial)
    
    ingredientes_usados = []
    estado_atual = estado_inicial
    historico_saidas = []
    historico_transicoes = []

    estado_atual = estado_inicial
    saida_atual = obter_saida_estado(estado_atual, saidas_estados)
    historico_saidas.append(saida_atual)
    estado_anterior = estado_atual
    historico_transicoes.append((estado_anterior, '', estado_atual, saida_atual))

    # Loop principal de processamento
    while True:
        limpar_tela()
        imprimeMoore(dicionario_transicoes, saidas_estados, estado_inicial)
        # Mostrar histórico em formato de tabela com cabeçalho
        print("\n╔═════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("║                                📜 HISTÓRICO DE TRANSIÇÕES                                   ║")
        print("╠════════════╦════════════╦════════════════╦══════════════════════════════════════════════════╣")
        print("║  Origem    ║  Entrada   ║    Destino     ║            Saída                                 ║")
        print("╠════════════╬════════════╬════════════════╬══════════════════════════════════════════════════╣")

        for i, (origem, simb, destino, saida) in enumerate(historico_transicoes):
            destino_str = destino if destino is not None else "erro"
            saida_str = saida if saida is not None else "--"

            # Determina a cor
            if destino_str == "erro":
                cor = VERMELHO
            elif i == len(historico_transicoes) - 1:
                cor = AMARELO
            else:
                cor = RESET

            print(f"║ {cor}{origem:^10}{RESET} ║ {cor}{simb:^10}{RESET} ║ {cor}{destino_str:^14}{RESET} ║ {cor}{saida_str:^48}{RESET} ║")

        print("╚════════════╩════════════╩════════════════╩══════════════════════════════════════════════════╝")

        ingrediente_simbolo = input("\nInsira um ingrediente (a, p, o, d, c, s): ").strip().lower()
        if ingrediente_simbolo not in alfabeto:
            print(f"Ingrediente '{ingrediente_simbolo}' inválido! ")
            time.sleep(1)
            continue
        
        ingredientes_usados.append(ingrediente_simbolo)
        
        # Realizar transicao
        novo_estado = realizar_transicao_moore(estado_atual, ingrediente_simbolo, dicionario_transicoes)
        
        if novo_estado is None:
            print("Transicao invalida! Nao ha transicao definida para este ingrediente neste estado.")
            print(f"   Estado atual: {estado_atual}")
            print(f"   Ingrediente: '{ingrediente_simbolo}'")
            continue
        


        estado_atual = novo_estado
        # Mostrar novo estado e sua saida
        saida_atual = obter_saida_estado(estado_atual, saidas_estados)
        historico_saidas.append(saida_atual)
        estado_anterior = estado_atual
        historico_transicoes.append((estado_anterior, ingrediente_simbolo, estado_atual, saida_atual))


        print("\n╔═════════════════════════════════════════════════════════════════════════════════════════════╗")
        print("║                                📜 HISTÓRICO DE TRANSIÇÕES                                   ║")
        print("╠════════════╦════════════╦════════════════╦══════════════════════════════════════════════════╣")
        print("║  Origem    ║  Entrada   ║    Destino     ║            Saída                                 ║")
        print("╠════════════╬════════════╬════════════════╬══════════════════════════════════════════════════╣")

        for i, (origem, simb, destino, saida) in enumerate(historico_transicoes):
            destino_str = destino if destino is not None else "erro"
            saida_str = saida if saida is not None else "--"

            # Determina a cor
            if destino_str == "erro":
                cor = VERMELHO
            elif i == len(historico_transicoes) - 1:
                cor = AMARELO
            else:
                cor = RESET

            print(f"║ {cor}{origem:^10}{RESET} ║ {cor}{simb:^10}{RESET} ║ {cor}{destino_str:^14}{RESET} ║ {cor}{saida_str:^48}{RESET} ║")

        print("╚════════════╩════════════╩════════════════╩══════════════════════════════════════════════════╝")

        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        while resposta not in ('s', 'n'):
            print("Opção inválida! Tente novamente.")
            resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            break
        
    
    # Verificar resultado final
    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                 🌟 RESULTADO FINAL 🌟                                ║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ Estado inicial da execução: {estado_inicial:<57}║")
    print(f"║ Estado final da execução:   {estado_atual:<57}║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")

    

    # Histórico de saidas
    print("║ Histórico de saídas:                                                                 ║")
    for i, saida in enumerate(historico_saidas):
        if i == 0:
            linha_saida = f"{i+1}: {saida} (inicial)"
        else:
            linha_saida = f"{i+1}: {saida} (após '{ingredientes_usados[i - 1]}')"
        print(f"║   {linha_saida:<83}║")

    # Resultado geral (sem depender de estado final)
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    if estado_atual == 'erro':
        print("║ Resultado:   A máquina entrou em um estado de erro (transição inválida).             ║")
    else:
        print("║ Resultado:   A execução terminou corretamente sem transições inválidas.              ║")

    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
