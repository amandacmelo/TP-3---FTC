import os
import time
# Codigos de cores ANSI
VERMELHO = '\033[91m'
VERDE = '\033[92m'
AMARELO = '\033[93m'
RESET = '\033[0m'

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def simbolo_para_nome_reacao(simbolo):
    mapeamento_reacoes = {
        'A': 'Dilui',
        'P': 'Perfuma', 
        'O': 'Engrossa',
        'D': 'Acido',
        'C': 'Alcalino',
        'S': 'Fedido',
        'λ': 'λ'
    }
    return mapeamento_reacoes.get(simbolo, simbolo)


# Pilha para armazenar as reacoes 
pilha_reacoes = []

def ler_automato_pilha(linhas):
    estados = set()
    estado_inicial = None
    estados_finais = set()
    dicionario_transicoes = {}

    i = 0

    # Lista de estadados
    if i < len(linhas) and linhas[i].startswith('Q:'):
        estados_str = linhas[i][2:].strip()
        estados = set(estados_str.split())
        i += 1

    # Estado Inicial
    if i < len(linhas) and linhas[i].startswith('I:'):
        estado_inicial = linhas[i][2:].strip()
        i += 1

    # Estados Finais
    if i < len(linhas) and linhas[i].startswith('F:'):
        estados_finais_str = linhas[i][2:].strip()
        if estados_finais_str:
            estados_finais = set(estados_finais_str.split())
        i += 1

    # Transicoes: atual -> prox | simbolo desempilhar empilhar
    while i < len(linhas):
        linha = linhas[i]
        if '->' in linha:
            partes = linha.split('->')
            estado_origem = partes[0].strip()
            resto = partes[1].strip()

            if '|' in resto:
                estado_destino, transicao_str = resto.split('|', 1)
                estado_destino = estado_destino.strip()
                transicao_info = [x.strip() for x in transicao_str.strip().split(',')]

                if len(transicao_info) >= 3:
                    simbolo_lido = transicao_info[0].strip()
                    simbolo_desempilhar = transicao_info[1].strip()
                    simbolo_empilhar = transicao_info[2].strip()

                    if simbolo_desempilhar == 'v':
                        simbolo_desempilhar = ''
                    if simbolo_empilhar == 'v':
                        simbolo_empilhar = ''

                    chave = (estado_origem, simbolo_lido, simbolo_desempilhar)
                    dicionario_transicoes[chave] = (estado_destino, simbolo_empilhar)
        i += 1

    return estado_inicial, estados_finais, dicionario_transicoes

def imprime_dicionario_apd(dicionario_transicoes, estado_inicial, estados_finais):
    
    linhas = []
    linhas.append("╔═════════════════╦═══════════╦═══════════════╦═══════════════╦═══════════════╗")
    linhas.append("║  Estado Atual   ║  Símbolo  ║  Desempilha   ║    Empilha    ║ Próximo Estado║")
    linhas.append("╠═════════════════╬═══════════╬═══════════════╬═══════════════╬═══════════════╣")
    
    for chave, valor in dicionario_transicoes.items():
        estado_atual, simbolo, desempilha = chave
        novo_estado, empilha = valor

        # Substitui vazio por lambda
        desempilha = desempilha if desempilha else 'λ'
        empilha = empilha if empilha else 'λ'

        # Aplica cor à linha inteira
        if estado_atual in estados_finais:
            cor = VERDE
        elif estado_atual == estado_inicial:
            cor = AMARELO
        else:
            cor = RESET

        if novo_estado != 'erro':
            linhas.append(
                f"║ {cor}{estado_atual:^15}{RESET} ║ {cor}{simbolo:^9}{RESET} ║ "
                f"{cor}{simbolo_para_nome_reacao(desempilha):^13}{RESET} ║ "
                f"{cor}{simbolo_para_nome_reacao(empilha):^13}{RESET} ║ "
                f"{cor}{novo_estado:^13}{RESET} ║"
            )
            linhas.append("╠═════════════════╬═══════════╬═══════════════╬═══════════════╬═══════════════╣")
    
    linhas[-1] = "╚═════════════════╩═══════════╩═══════════════╩═══════════════╩═══════════════╝"
    
    for linha in linhas:
        print(linha)

    
    print("╔═════════════════════════════════════════════════════════════════════════════╗") 
    print(f"║ Estado Inicial: {estado_inicial:<60}║")
    print(f"║ Estado(s) Final(is): {', '.join(estados_finais):<55}║")
    print("╚═════════════════════════════════════════════════════════════════════════════╝")

def mostrar_pilha(ingredientes):
    if not pilha_reacoes:
        print("\n╔══════════════════════╗")
        print("║ Poção neutra (vazia) ║")
        print("╚══════════════════════╝")
    else:
        print("\n🧪 Reações ativas na poção:")
        print("╔════════════════╗")
        for simbolo in reversed(pilha_reacoes):
            reacao = simbolo_para_nome_reacao(simbolo) 
            print(f"║ {reacao:^14} ║")
        print("╚════════════════╝")

def processar_pilha(simbolo, simbolo_desempilhar, simbolo_empilhar, ingredientes):
    global pilha_reacoes
    
    if simbolo not in ingredientes:
        print("⚠️ Ingrediente desconhecido!")
        return False

    nome = ingredientes[simbolo]['nome']
    reacao = ingredientes[simbolo]['reacao']
    
    
    # Verificar se pode desempilhar
    if simbolo_desempilhar != '':
        # Desempilhar simbolo especifico
        if not pilha_reacoes or pilha_reacoes[-1] != simbolo_desempilhar:
            topo_atual = pilha_reacoes[-1] if pilha_reacoes else 'VAZIA'
            print(f"Erro ao desempilhar: esperava '{simbolo_desempilhar}', topo é '{topo_atual}'")
        
            return False
        else:
            removido = pilha_reacoes.pop()
            reacao_removida = simbolo_para_nome_reacao(removido)

    
    # Empilhar se necessario
    if simbolo_empilhar != '':
        pilha_reacoes.append(simbolo_empilhar)
        empilhado = simbolo_para_nome_reacao(simbolo_empilhar)
    return True

def realizar_transicao_apd(estado_atual, simbolo, dicionario):
    """
    Procura por uma transição válida no autômato de pilha
    """
    # Determinar topo da pilha
    if pilha_reacoes:
        topo_pilha = pilha_reacoes[-1]
    else:
        topo_pilha = ''  # Pilha vazia representada por string vazia

    # 1. Transicao que desempilha o topo atual (se pilha nao esta vazia)
    if topo_pilha != '':
        chave_desempilha = (estado_atual, simbolo, topo_pilha)
        if chave_desempilha in dicionario:
            novo_estado, simbolo_empilhar = dicionario[chave_desempilha]
            return novo_estado, topo_pilha, simbolo_empilhar
    
    # 2. Transicao que nao desempilha (epsilon) 
    chave_epsilon = (estado_atual, simbolo, '')
    if chave_epsilon in dicionario:
        novo_estado, simbolo_empilhar = dicionario[chave_epsilon]
        return novo_estado, '', simbolo_empilhar
    
    return None, None, None

def executar_simulador_pilha(alfabeto, ingredientes, conteudo):
    global pilha_reacoes

    estado_inicial, estados_finais, dicionario_transicoes = ler_automato_pilha(conteudo)

    if estado_inicial is None:
        print("Erro ao ler o autômato.")
        return
        
    imprime_dicionario_apd(dicionario_transicoes, estado_inicial, estados_finais)
    
    ingredientes_usados = []
    estado_atual = estado_inicial
    pilha_reacoes = []
    historico_transicoes = []

    mostrar_pilha(ingredientes)

    while True:
        limpar_tela()
        imprime_dicionario_apd(dicionario_transicoes, estado_inicial, estados_finais)
        if historico_transicoes != []:
            print("╔════════════════════════════════════════════════════════════════╗")
            print("║                       HISTÓRICO DE TRANSIÇÕES                  ║")
            print("╠═══════════╦══════════╦═══════════╦══════════════╦══════════════╣")
            print("║  Origem   ║ Símbolo  ║  Destino  ║  Desempilha  ║   Empilha    ║")
            print("╠═══════════╬══════════╬═══════════╬══════════════╬══════════════╣")

            for i, (origem, simb, destino, desemp, emp) in enumerate(historico_transicoes):
            
                # Definindo a cor da linha
                if destino == "erro":
                    cor = VERMELHO
                elif destino in estados_finais:
                    cor = VERDE
                elif i == len(historico_transicoes) - 1:
                    cor = AMARELO
               
                else:
                    cor = RESET

                print(f"║ {cor}{origem:^9}{RESET} ║ {cor}{simb:^8}{RESET} ║ {cor}{destino:^9}{RESET} ║ {cor}{simbolo_para_nome_reacao(desemp):^12}{RESET} ║ {cor}{simbolo_para_nome_reacao(emp):^12}{RESET} ║")

            print("╚═══════════╩══════════╩═══════════╩══════════════╩══════════════╝")

        

        simbolo = input("\nInsira um ingrediente (a, p, o, d, c, s): ").strip().lower()
        if simbolo not in alfabeto:
            print(f"Ingrediente '{simbolo}' inválido! Ingredientes válidos: {', '.join(alfabeto)}")
            time.sleep(1)
            continue

        novo_estado, simbolo_desempilhar, simbolo_empilhar = realizar_transicao_apd(estado_atual, simbolo, dicionario_transicoes)


        # Processar acao na pilha
        if not processar_pilha(simbolo, simbolo_desempilhar, simbolo_empilhar, ingredientes):
            print("Erro ao processar pilha.")
            estado_atual = 'erro'
            break
        ingredientes_usados.append(simbolo)
        estado_atual = novo_estado

        # Mostrar historico de transicoes
        if simbolo_desempilhar == '':
            simbolo_desempilhar = 'λ'
            
        if simbolo_empilhar == '':

            simbolo_empilhar = 'λ'
        historico_transicoes.append((estado_atual, simbolo, novo_estado, simbolo_desempilhar, simbolo_empilhar))


        print("╔════════════════════════════════════════════════════════════════╗")
        print("║                       HISTÓRICO DE TRANSIÇÕES                  ║")
        print("╠═══════════╦══════════╦═══════════╦══════════════╦══════════════╣")
        print("║  Origem   ║ Símbolo  ║  Destino  ║  Desempilha  ║   Empilha    ║")
        print("╠═══════════╬══════════╬═══════════╬══════════════╬══════════════╣")

        for i, (origem, simb, destino, desemp, emp) in enumerate(historico_transicoes):
        
            # Definindo a cor da linha
            if destino == "erro":
                cor = VERMELHO
            elif destino in estados_finais:
                cor = VERDE
            elif i == len(historico_transicoes) - 1:
                cor = AMARELO
            
            else:
                cor = RESET

            print(f"║ {cor}{origem:^9}{RESET} ║ {cor}{simb:^8}{RESET} ║ {cor}{destino:^9}{RESET} ║ {cor}{simbolo_para_nome_reacao(desemp):^12}{RESET} ║ {cor}{simbolo_para_nome_reacao(emp):^12}{RESET} ║")

        print("╚═══════════╩══════════╩═══════════╩══════════════╩══════════════╝")
        mostrar_pilha(ingredientes)
       
        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        while resposta not in ('s', 'n'):
            print("Opção inválida! Tente novamente.")
            resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            break



    # Verificações para o resultado final
    estado_final_valido = estado_atual in estados_finais
    pilha_vazia = len(pilha_reacoes) == 0    
    # Resultado final
    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                 🌟 RESULTADO FINAL 🌟                                ║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ Estado final da execução: {estado_atual:<59}║")

    if estado_atual == 'erro':
        print("║ Resultado:   O autômato entrou em um estado de erro (transição inválida).            ║")
        print("╚══════════════════════════════════════════════════════════════════════════════════════╝")

    elif estado_final_valido and pilha_vazia:
        print("║ Resultado:   A poção foi concluída com sucesso! Estado final alcançado!              ║")
        print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    elif not estado_final_valido and pilha_vazia:
        print("║ Resultado:   A execução terminou sem atingir um estado final.                        ║")
        print("╚══════════════════════════════════════════════════════════════════════════════════════╝")

    elif estado_final_valido and not pilha_vazia:
        print("║ Resultado:   Estado final alcançado, mas a pilha não está vazia.                     ║")
        print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
        mostrar_pilha(ingredientes)

    else:
        print("║ Resultado:   A execução falhou - estado não final e pilha não vazia.                 ║")
        print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
        mostrar_pilha(ingredientes)