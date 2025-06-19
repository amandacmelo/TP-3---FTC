# Pilha para armazenar as reações
pilha_reacoes = []

# 1 - criar o alfabeto
''' Ingredientes
  a - água
  p - pétalas
  o - óleo
  d - dente de dragão
  c - costela de adão
  s - sapo
'''

alfabeto = {'a', 'p', 'o', 'd', 'c', 's', 'e'}

ingrediente = {
  'a': {
    'nome': 'Agua',
    'simbolo': 'a',
    'reacao': 'dilui',
    'neutraliza': ['engrossa']
  },
  'p': {
    'nome': 'Petalas',
    'simbolo': 'p',
    'reacao': 'perfuma',
    'neutraliza': ['fedido']
  },
  'o': {
    'nome': 'Oleo',
    'simbolo': 'o',
    'reacao': 'engrossa',
    'neutraliza': ['dilui']
  },
  'd': {
    'nome': 'Dente de Dragao',
    'simbolo': 'd',
    'reacao': 'acido',
    'neutraliza': ['alcalino']
  },
  'c': {
    'nome': 'Costela de Adao',
    'simbolo': 'c',
    'reacao': 'alcalino',
    'neutraliza': ['acido']
  },
  's': {
    'nome': 'Sapo',
    'simbolo': 's',
    'reacao': 'fedido',
    'neutraliza': ['perfuma']
  },
  'e': {
    'nome': 'Erro',
    'simbolo': 'e',
    'reacao': 'erro',
    'neutraliza': []
  }
}


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
                        if simbolo_desempilhar == 'ε':
                            simbolo_desempilhar = ''
                        if simbolo_empilhar == 'ε':
                            simbolo_empilhar = ''
                        
                        chave = (estado_origem, simbolo_lido, simbolo_desempilhar)
                        dicionario_transicoes[chave] = (estado_destino, simbolo_empilhar)
            i += 1
        
        return estado_inicial, estados_finais, dicionario_transicoes
    
    except Exception as e:
        print(f"Erro ao processar entrada: {e}")
        return None, None, None

def imprime_dicionario_apd(dicionario_transicoes):
    print("\n=== DICIONÁRIO DE TRANSIÇÕES APD ===")
    print("Formato: (estado_atual, simbolo, topo_pilha) -> (novo_estado, empilha)")
    for chave, valor in dicionario_transicoes.items():
        print(f"{chave} -> {valor}")

def mostrar_pilha():
    if not pilha_reacoes:
        print("🧪 Poção neutra (sem reações ativas)")
    else:
        print(f"🧪 Reações ativas na poção: {' -> '.join(pilha_reacoes[::-1])} (topo)")

def processar_pilha(simbolo, simbolo_desempilhar, simbolo_empilhar):
    global pilha_reacoes
    
    if simbolo not in ingrediente:
        return False
    
    reacao_atual = ingrediente[simbolo]['reacao']
    
    print(f"\n➕ Adicionando {ingrediente[simbolo]['nome']}...")
    print(f"   Propriedade/Reação: {reacao_atual}")
    
    # Verificar se pode desempilhar
    if simbolo_desempilhar != '':
        if simbolo_desempilhar == 'Z0':
            # Z0 está implícito no fundo da pilha
            if pilha_reacoes:
                print(f"   ❌ Erro: Tentou desempilhar Z0 mas pilha não está vazia!")
                return False
            else:
                print(f"   📥 Verificação Z0 OK (pilha estava vazia)")
        else:
            # Desempilhar símbolo específico
            if not pilha_reacoes or pilha_reacoes[-1] != simbolo_desempilhar:
                topo_atual = pilha_reacoes[-1] if pilha_reacoes else 'Z0'
                print(f"   ❌ Erro: Tentou desempilhar '{simbolo_desempilhar}' mas topo é '{topo_atual}'!")
                return False
            else:
                removido = pilha_reacoes.pop()
                print(f"   📥 '{removido}' desempilhada!")
    else:
        print(f"   ➡️  Sem desempilhamento necessário")
    
    # Empilhar se necessário
    if simbolo_empilhar != '':
        pilha_reacoes.append(simbolo_empilhar)
        print(f"   📤 '{simbolo_empilhar}' empilhada!")
    else:
        print(f"   ➡️  Sem empilhamento necessário")
    
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
        topo_pilha = 'Z0'  # Símbolo especial para pilha vazia
    
    # Procurar transições possíveis
    # 1. Transição que desempilha o topo atual
    chave_desempilha = (estado_atual, simbolo, topo_pilha)
    if chave_desempilha in dicionario:
        novo_estado, simbolo_empilhar = dicionario[chave_desempilha]
        return novo_estado, topo_pilha, simbolo_empilhar
    
    # 2. Transição que não desempilha (epsilon)
    chave_epsilon = (estado_atual, simbolo, '')
    if chave_epsilon in dicionario:
        novo_estado, simbolo_empilhar = dicionario[chave_epsilon]
        return novo_estado, '', simbolo_empilhar
    
    # 3. Transição com Z0 (pilha vazia)
    if topo_pilha == 'Z0':
        chave_z0 = (estado_atual, simbolo, 'Z0')
        if chave_z0 in dicionario:
            novo_estado, simbolo_empilhar = dicionario[chave_z0]
            return novo_estado, 'Z0', simbolo_empilhar
    
    return None, None, None

def main():
    
    print("=" * 60)
    print("🧙 SIMULADOR DE POÇÕES - AUTÔMATO DE PILHA 🧙")
    print("=" * 60)
    print("Baseado na entrada do autômato fornecida!\n")
    
    # Entrada do autômato (como fornecida)
    entrada_automato = """Q: I Q1 Q2 Q3 F erro
I: I
F: F
I -> Q1 | a, Z0, D
Q1 -> Q1 | a, ε, D
Q1 -> Q2 | p, ε, P
Q2 -> Q2 | p, ε, P
Q2 -> Q3 | s, P, ε
Q3 -> F | o, D, ε
F -> F | o, D, ε"""
    
    estado_inicial, estados_finais, dicionario_transicoes = ler_automato_pilha(entrada_automato)
    
    if estado_inicial is None:
        print("❌ Erro ao carregar autômato!")
        return
    
    imprime_dicionario_apd(dicionario_transicoes)
    
    ingredientes = []
    estado_atual = estado_inicial
    pilha_reacoes = []  # Reset da pilha
    
    print(f"\n📋 Ingredientes disponíveis:")
    for simbolo, info in ingrediente.items():
        if simbolo != 'e':
            print(f"   {simbolo} - {info['nome']} (causa: {info['reacao']}, neutraliza: {info['neutraliza']})")
    
    print(f"\n🏁 Estado inicial: {estado_inicial}")
    print(f"🎯 Estados finais: {estados_finais}")
    
    mostrar_pilha()
    
    # Loop principal de processamento
    while True:
        print("\n" + "─" * 50)
        print("🥄 Insira o símbolo do ingrediente (ou 'sair' para terminar):")
        ingrediente_simbolo = input(">>> ").strip().lower()
        
        if ingrediente_simbolo == 'sair':
            break
            
        if ingrediente_simbolo not in alfabeto:
            print("❌ Ingrediente inválido!")
            continue
        
        ingredientes.append(ingrediente_simbolo)
        novo_estado, simbolo_desempilhar, simbolo_empilhar = realizar_transicao_apd(estado_atual, ingrediente_simbolo, dicionario_transicoes)
        
        if novo_estado is None:
            print("❌ Transição inválida! Não há transição definida para este ingrediente neste estado.")
            print(f"   Estado atual: {estado_atual}")
            print(f"   Ingrediente: {ingrediente_simbolo}")
            print(f"   Topo da pilha: {pilha_reacoes[-1] if pilha_reacoes else 'Z0'}")
            continue
        elif novo_estado == 'erro':
            print("💥 ERRO: Combinação de ingredientes levou ao estado de erro!")
            break
        
        # Processar ação na pilha
        if not processar_pilha(ingrediente_simbolo, simbolo_desempilhar, simbolo_empilhar):
            print("💥 ERRO: Falha ao processar pilha!")
            break
        
        estado_atual = novo_estado
        print(f"📍 Estado atual: {estado_atual}")
        
        # Verificar se chegou a um estado final
        if estado_atual in estados_finais:
            print("🎉 Chegou a um estado final! Você pode continuar ou terminar aqui.")
    
    # Verificar resultado final
    print("\n" + "=" * 60)
    print("🏁 RESULTADO FINAL")
    print("=" * 60)
    
    print(f"📝 Ingredientes utilizados: {' -> '.join(ingredientes)}")
    print(f"📍 Estado final: {estado_atual}")
    
    if estado_atual in estados_finais:
        print("✅ SUCESSO: A sequência foi aceita pelo autômato!")
        if not pilha_reacoes:
            print("✅ PERFEITO: Pilha está vazia (balanceada)!")
        else:
            print(f"⚠️  Pilha não está vazia: {pilha_reacoes}")
    else:
        print("❌ FALHA: A sequência não foi aceita (não terminou em estado final)!")
    
    mostrar_pilha()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()