def ler_moore(entrada_texto):
    """
    formato maquina moore
    Q: lista de estados
    I: estado inicial
    F: estados finais
    O: saidas para cada estado (formato: estado=saida)
    transicoes: estado_origem -> estado_destino | simbolos
    
    """

    try:
        linhas = entrada_texto.strip().split('\n')
        linhas = [linha.strip() for linha in linhas if linha.strip()]
        
        estados = set()
        estado_inicial = None
        estados_finais = set()
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
        
        # F: estados finais
        if i < len(linhas) and linhas[i].startswith('F:'):
            estados_finais_str = linhas[i][2:].strip()
            if estados_finais_str:
                estados_finais = set(estados_finais_str.split())
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
        
        return estado_inicial, estados_finais, saidas_estados, dicionario_transicoes
    
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")
        return None, None, None, None


def imprimeMoore(dicionario_transicoes, saidas_estados):
    print("\n=== MAQUINA DE MOORE ===")
    print("\n--- SAIDAS DOS ESTADOS ---")
    for estado, saida in saidas_estados.items():
        print(f"Estado {estado}: {saida}")
    
    print("\n--- TRANSICOES ---")
    for chave, valor in dicionario_transicoes.items():
        print(f"{chave} -> {valor}")

def obter_saida_estado(estado, saidas_estados):
    """
    Obtem a saida associada ao estado atual
    """
    if estado in saidas_estados:
        codigo_saida = saidas_estados[estado]
        
        # Mapear codigos de saida para descricoes simples
        mapeamento_saidas = {
            'inicio': 'Caldeirao preparado para receber ingredientes',
            'processando': 'Processando ingredientes iniciais...',
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

def ler_arquivo_moore(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            conteudo = arquivo.read()
            return conteudo
    except FileNotFoundError:
        print(f"Arquivo '{nome_arquivo}' nao encontrado!")
        return None
    except Exception as e:
        print(f"Erro ao ler arquivo: {e}")
        return None

def executar_simulador_moore(alfabeto, ingredientes):
    print("=" * 60)
    print("SIMULADOR DE POCOES - MAQUINA DE MOORE")
    print("=" * 60)
    
    # Solicitar nome do arquivo
    print("Digite o nome do arquivo da Maquina de Moore:")
    nome_arquivo = input(">>> ").strip()
    
    if not nome_arquivo:
        print("Nome do arquivo nao pode estar vazio!")
        return
    
    # leitura arquivo
    entrada_moore = ler_arquivo_moore(nome_arquivo)
    if entrada_moore is None:
        print("Erro ao ler o arquivo da Maquina de Moore")
        return
    
    # Processar maquina
    estado_inicial, estados_finais, saidas_estados, dicionario_transicoes = ler_moore(entrada_moore)
    
    if estado_inicial is None:
        print("Erro ao carregar maquina de Moore! Verifique o formato do arquivo.")
        return
    
    #imprimeMoore(dicionario_transicoes, saidas_estados)
    
    ingredientes_usados = []
    estado_atual = estado_inicial
    historico_saidas = []
    
    print(f"\nIngredientes disponiveis:")
    for simbolo, info in ingredientes.items():
        if simbolo != 'e':
            print(f"   {simbolo} - {info['nome']}")
    
    # saida do estado
    saida_atual = obter_saida_estado(estado_atual, saidas_estados)
    print(f"Saida atual: {saida_atual}")
    historico_saidas.append(saida_atual)
    
    # Loop principal de processamento
    while True:
        print("\n" + "-" * 50)
        print("Insira o simbolo do ingrediente (ou 'sair' para terminar):")
        ingrediente_simbolo = input(">>> ").strip().lower()
        
        if ingrediente_simbolo == 'sair':
            break
            
        if ingrediente_simbolo not in alfabeto:
            print(f"Ingrediente '{ingrediente_simbolo}' nao esta no alfabeto valido!")
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
        
        # Obter e mostrar informacoes do ingrediente
        if ingrediente_simbolo in ingredientes:
            info_ingrediente = ingredientes[ingrediente_simbolo]
            print(f"Adicionado: {info_ingrediente['nome']}")
        
        # Mostrar novo estado e sua saida
        saida_atual = obter_saida_estado(estado_atual, saidas_estados)
        print(f"Novo estado: {estado_atual}")
        print(f"Saida do estado: {saida_atual}")
        historico_saidas.append(saida_atual)
        
        # Verificar se chegou a um estado final
        if estado_atual in estados_finais:
            print("A pocao ja esta pronta para ser utilizada\n Voce pode continuar adicionando ingredientes ou encerrar a preparacao.")
        elif estado_atual == 'erro':
            print("ERRO: Chegou ao estado de erro :(")
    
    # Verificar resultado final
    print("\n" + "=" * 60)
    print("RESULTADO FINAL")
    print("=" * 60)
    
    print(f"Ingredientes utilizados: {' -> '.join(ingredientes_usados)}")

    if estado_atual in estados_finais:
        print("SUCESSO: A maquina terminou em estado final! A pocao esta prontinha!")
    else:
        print("A maquina nao terminou em estado final.")
    
    print(f"\nHistorico de saidas:")
    for i, saida in enumerate(historico_saidas):
        if i == 0:
            print(f"   {i}: {saida} (inicial)")
        else:
            print(f"   {i}: {saida} (apos '{ingredientes_usados[i-1]}')")
    
    print("\n" + "=" * 60)