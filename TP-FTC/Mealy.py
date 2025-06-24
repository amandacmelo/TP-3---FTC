def ler_automato_mealy(nome_arquivo):
    """
    Lê um autômato Mealy de um arquivo no formato:
    Q: lista de estados
    I: estado inicial
    estado_origem -> estado_destino | entrada/saida entrada/saida ...
    """
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
        # Remove linhas vazias e espaços em branco
        linhas = [linha.strip() for linha in linhas if linha.strip()]
        
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
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None, None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
        return None, None

def imprime_dicionario_mealy(dicionario_transicoes):
    """Imprime o dicionário de transições Mealy de forma organizada"""
    print("\n╔══════════════════════════════════════════════════════════════╗")
    print("║                  DICIONÁRIO DE TRANSIÇÕES MEALY              ║")
    print("╠══════════════════════════════════════════════════════════════╣")
    print("║  Estado Atual  │  Entrada  │ Próximo Estado │     Saída      ║")
    print("╠════════════════╪═══════════╪════════════════╪════════════════╣")
    
    for chave, (destino, saida) in dicionario_transicoes.items():
        estado_atual, entrada = chave
        print(f"║ {estado_atual:^14} │ {entrada:^9} │ {destino:^14} │ {saida:^14} ║")
    
    print("╚════════════════╧═══════════╧════════════════╧════════════════╝")

    print("╔══════════════════════════════════════════════════════════════╗")
    print("║ Estado Inicial: I                                            ║")
    print("║ Estado Final: F                                              ║")
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

def obter_nome_ingrediente(simbolo, ingredientes):
    """Retorna o nome completo do ingrediente pelo símbolo"""
    if simbolo in ingredientes:
        return ingredientes[simbolo]['nome']
    return "Desconhecido"

def obter_reacao_ingrediente(simbolo, ingredientes):
    """Retorna a reação do ingrediente pelo símbolo"""
    if simbolo in ingredientes:
        return ingredientes[simbolo]['reacao']
    return "sem reação"

def executar_simulador_mealy(alfabeto, ingredientes):
    """Executa o simulador do autômato Mealy"""
    nome_arquivo = 'Entradas/maquina_mealy.txt'
    estado_inicial, dicionario_transicoes = ler_automato_mealy(nome_arquivo)
    
    if estado_inicial is None:
        print("Não foi possível carregar o autômato.")
        return
    
    
    # Mostra o dicionário de transições
    imprime_dicionario_mealy(dicionario_transicoes)
    
    print("\n INGREDIENTES DISPONÍVEIS:")
    print("╔══════════════════════════════════════════════════════════╗")
    for simbolo, info in ingredientes.items():
        print(f"║ {simbolo} - {info['nome']:<20} (Efeito: {info['reacao']:<10})            ║")
    print("╚══════════════════════════════════════════════════════════╝")
    
    lista_ingredientes = []
    lista_saidas = []
    estado_atual = estado_inicial
    
    print(f"\nEstado inicial: {estado_inicial}")
    
    # Pergunta pelo primeiro ingrediente
    primeiro_ingrediente = input("\nInsira o símbolo do primeiro ingrediente da receita: ").strip().lower()
    
    if primeiro_ingrediente not in alfabeto:
        print("Ingrediente inválido!")
        return
    
    lista_ingredientes.append(primeiro_ingrediente)
    proximo_estado, saida = realizar_transicao_mealy(estado_inicial, primeiro_ingrediente, dicionario_transicoes)
    
    if proximo_estado is None:
        print("Transição inválida!")
        return
    
    estado_atual = proximo_estado
    lista_saidas.append(saida)
    
    nome_ingrediente = obter_nome_ingrediente(primeiro_ingrediente, ingredientes)
    print(f"\n Adicionado: {nome_ingrediente} ({primeiro_ingrediente})")
    print(f"   -> Efeito: {saida}")
    print(f"   -> Estado atual: {estado_atual}")
    
    # Loop para perguntar por mais ingredientes
    while True:
        if estado_atual == 'erro' or estado_atual is None:
            print("\nERRO: A receita falhou!")
            print("Combinação de ingredientes resultou em erro.")
            break
        
        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        
        if resposta == 's':
            # Lista os ingredientes disponíveis baseado no alfabeto
            ingredientes_str = ', '.join(sorted(alfabeto))
            ingrediente = input(f"Insira um ingrediente ({ingredientes_str}): ").strip().lower()
            
            if ingrediente not in alfabeto:
                print("Ingrediente inválido!")
                continue
            
            lista_ingredientes.append(ingrediente)
            proximo_estado, saida = realizar_transicao_mealy(estado_atual, ingrediente, dicionario_transicoes)
            
            if proximo_estado is None:
                print("\nTransição inválida para este estado e ingrediente!")
                print("Receita não pode continuar.")
                break
            
            estado_atual = proximo_estado
            lista_saidas.append(saida)
            
            nome_ingrediente = obter_nome_ingrediente(ingrediente, ingredientes)
            print(f"\n Adicionado: {nome_ingrediente} ({ingrediente})")
            print(f"  -> Efeito: {saida}")
            print(f"  -> Estado atual: {estado_atual}")
            
        elif resposta == 'n':
            print("\nFinalizando receita... :)")
            print("Receita mágica concluída!")
            break
        else:
            print("Resposta inválida. Digite 's' para sim ou 'n' para não.")
    
    # Resumo final
    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║  RESUMO DA RECEITA                                                                   ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")
    print("════════════════════════════════════════════════════════════════════════════════════════")
    print(f" Estado inicial: {estado_inicial}")
    print(f" Estado final: {estado_atual}")
    print(f" \n Ingredientes utilizados: {' -> '.join(lista_ingredientes) if lista_ingredientes else 'Nenhum'}")
    print(f" Efeitos produzidos: {' -> '.join(lista_saidas) if lista_saidas else 'Nenhum'}")
    print("════════════════════════════════════════════════════════════════════════════════════════")
