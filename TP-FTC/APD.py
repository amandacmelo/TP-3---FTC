# APD.py - Versão refatorada sem Z0

# Pilha para armazenar as reações (variável global do módulo)
pilha_reacoes = []

def ler_automato_pilha(entrada_texto):
    """
    Lê um autômato de pilha a partir de texto formatado
    """
    try:
        linhas = entrada_texto.strip().split('\n')
        linhas = [linha.strip() for linha in linhas if linha.strip()]
        
        estados = set()
        estado_inicial = None
        estados_finais = set()
        dicionario_transicoes = {}
        
        i = 0
        
        # Primeira linha: Q: lista de estados
        if i < len(linhas) and linhas[i].startswith('Q:'):
            estados_str = linhas[i][2:].strip()
            estados = set(estados_str.split())
            i += 1
        
        # Segunda linha: I: estado inicial
        if i < len(linhas) and linhas[i].startswith('I:'):
            estado_inicial = linhas[i][2:].strip()
            i += 1
        
        # Terceira linha: F: estados finais
        if i < len(linhas) and linhas[i].startswith('F:'):
            estados_finais_str = linhas[i][2:].strip()
            if estados_finais_str:
                estados_finais = set(estados_finais_str.split())
            i += 1
        
        # Resto das linhas: transições
        while i < len(linhas):
            linha = linhas[i]
            if '->' in linha:
                # Parse da transição APD: "estado_origem -> estado_destino | simbolo_lido, simbolo_desempilhar, simbolo_empilhar"
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
                        
                        # Tratar epsilon (ε) como string vazia
                        if simbolo_desempilhar == 'v':
                            simbolo_desempilhar = ''
                        if simbolo_empilhar == 'v':
                            simbolo_empilhar = ''
                        
                        chave = (estado_origem, simbolo_lido, simbolo_desempilhar)
                        dicionario_transicoes[chave] = (estado_destino, simbolo_empilhar)

            i += 1
            
        imprime_dicionario_apd(dicionario_transicoes)
    
        return estado_inicial, estados_finais, dicionario_transicoes
    
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")
        return None, None, None

def imprime_dicionario_apd(dicionario_transicoes):
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                     DICIONÁRIO DE TRANSIÇÕES APD             ║")
    print("╠═════════════════╪═══════════╪═══════════════╪════════════════╣")
    print("║ Estado Atual    │ Símbolo   │ Topo Pilha    │ Próximo Estado ║")
    print("╠═════════════════╪═══════════╪═══════════════╪════════════════╣")
    
    for chave, valor in dicionario_transicoes.items():
        estado_atual, simbolo, topo_pilha = chave
        novo_estado, empilha = valor
        # Aqui você pode formatar o valor 'empilha' para exibir como string, se for lista ou algo assim
        print(f"║ {estado_atual:^15} │ {simbolo:^9} │ {topo_pilha:^13} │ {novo_estado:^14} ║")
    
    print("╚═════════════════╧═══════════╧═══════════════╧════════════════╝")
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║ Estado Inicial: I                                            ║")
    print("║ Estado Final: F                                              ║")
    print("╚══════════════════════════════════════════════════════════════╝")

def mostrar_pilha():
    if not pilha_reacoes:
        print("\nPoção neutra (pilha vazia)")
    else:
        print(f"\nReações ativas na poção: {' -> '.join(pilha_reacoes[::-1])} (topo)")

def processar_pilha(simbolo, simbolo_desempilhar, simbolo_empilhar, ingredientes):
    global pilha_reacoes
    
    if simbolo not in ingredientes:
        return False
    
    reacao_atual = ingredientes[simbolo]['reacao']
    
    print(f"\nAdicionando {ingredientes[simbolo]['nome']}...")
    print(f"   -Propriedade/Reação: {reacao_atual}")
    
    # Verificar se pode desempilhar
    if simbolo_desempilhar != '':
        # Desempilhar símbolo específico
        if not pilha_reacoes or pilha_reacoes[-1] != simbolo_desempilhar:
            topo_atual = pilha_reacoes[-1] if pilha_reacoes else 'VAZIA'
            print(f"Erro: Tentou desempilhar '{simbolo_desempilhar}' mas topo é '{topo_atual}'!")
            return False
        else:
            removido = pilha_reacoes.pop()
            print(f"   '{removido}' desempilhada!")
    else:
        print(f"   -Sem desempilhamento necessário")
    
    # Empilhar se necessário
    if simbolo_empilhar != '':
        pilha_reacoes.append(simbolo_empilhar)
        print(f"   -'{simbolo_empilhar}' empilhada!")
    else:
        print(f"   -Sem empilhamento necessário")
    
    mostrar_pilha()
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
    
    # Procurar transições possíveis
    # 1. Transição que desempilha o topo atual (se pilha não está vazia)
    if topo_pilha != '':
        chave_desempilha = (estado_atual, simbolo, topo_pilha)
        if chave_desempilha in dicionario:
            novo_estado, simbolo_empilhar = dicionario[chave_desempilha]
            return novo_estado, topo_pilha, simbolo_empilhar
    
    # 2. Transição que não desempilha (epsilon) - funciona com pilha vazia ou não
    chave_epsilon = (estado_atual, simbolo, '')
    if chave_epsilon in dicionario:
        novo_estado, simbolo_empilhar = dicionario[chave_epsilon]
        return novo_estado, '', simbolo_empilhar
    
    return None, None, None

def executar_simulador_pilha(alfabeto, ingredientes):
    """
    Simulador de autômato de pilha com saída formatada estilo máquina de estados.
    """
    global pilha_reacoes

    try:
        with open("Entradas/automato_pilha.txt", "r") as arquivo:
            entrada_automato = arquivo.read()
    except FileNotFoundError:
        print("Erro: Arquivo 'automato_pilha.txt' não encontrado!")
        return

    estado_inicial, estados_finais, dicionario_transicoes = ler_automato_pilha(entrada_automato)

    if estado_inicial is None:
        print(" Erro ao ler autômato.")
        return

    ingredientes_usados = []
    estado_atual = estado_inicial
    pilha_reacoes = []

    print("\n Ingredientes disponíveis:")
    for simbolo, info in ingredientes.items():
        if simbolo != 'e':
            print(f"  {simbolo} - {info['nome']} (causa: {info['reacao']}, neutraliza: {info['neutraliza']})")

    mostrar_pilha()

    continuar = 's'
    while continuar == 's':
        continuar = input("\nDeseja inserir um ingrediente (s/n)? ").strip().lower()
        if continuar != 's':
            print("\nEncerrando a simulação...")
            break

        ingrediente_simbolo = input("Insira um ingrediente (a, p, o, d, c, s): ").strip().lower()

        if ingrediente_simbolo not in alfabeto:
            print(f"Ingrediente '{ingrediente_simbolo}' inválido! Ingredientes válidos: {', '.join(alfabeto)}")
            continue

        novo_estado, simbolo_desempilhar, simbolo_empilhar = realizar_transicao_apd(
            estado_atual, ingrediente_simbolo, dicionario_transicoes)

        if novo_estado is None:
            print("\n Transição inválida!")
            print(f"   Estado atual: {estado_atual}")
            print(f"   Ingrediente: {ingrediente_simbolo}")
            print(f"   Topo da pilha: {pilha_reacoes[-1] if pilha_reacoes else 'VAZIA'}")
            continue

        # Processar ação na pilha
        if not processar_pilha(ingrediente_simbolo, simbolo_desempilhar, simbolo_empilhar, ingredientes):
            print(" ERRO: Falha ao processar pilha!")
            break

        ingredientes_usados.append(ingrediente_simbolo)
        estado_atual = novo_estado
        print(f"📍 Estado atual: {estado_atual}")

        if estado_atual == 'erro':
            print("ERRO: A poção explodiu! Estado de erro atingido!")
            break

    # Resultado final
    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║ RESULTADO FINAL                                                                      ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    print("════════════════════════════════════════════════════════════════════════════════════════")
    print(f" Ingredientes utilizados: {' -> '.join(ingredientes_usados) if ingredientes_usados else 'Nenhum'}")
    print(f" Estado final da execução: {estado_atual}")
    print("                                                                                      ")

    estado_final_valido = estado_atual in estados_finais
    pilha_vazia = not pilha_reacoes

    #print(f" Estado final válido: {'✅ Sim' if estado_final_valido else ' Não'}")
    #print(f" Pilha vazia: {'✅ Sim' if pilha_vazia else ' Não'}")

    if estado_final_valido and pilha_vazia:
        print("A poção está perfeita! Autômato ACEITOU a sequência! :)")
    else:
        print(" A combinação não funcionou. Autômato REJEITOU a sequência. :( ")
        if not estado_final_valido:
            print("    -> Não terminou em estado final")
        if not pilha_vazia:
            print("    -> Pilha não está vazia")

    mostrar_pilha()
    print("════════════════════════════════════════════════════════════════════════════════════════")
