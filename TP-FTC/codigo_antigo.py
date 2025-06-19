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


def ler_automato_pilha(nome_arquivo):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            linhas = arquivo.readlines()
        
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
            if estados_finais_str:
                estados_finais = set(estados_finais_str.split())
            i += 1
        
        # Resto das linhas: transições
        while i < len(linhas):
            linha = linhas[i]
            if '->' in linha:
                # Parse da transição APD: "estado_origem -> estado_destino | simbolo, topo_pilha, empilha"
                partes = linha.split('->')
                estado_origem = partes[0].strip()
                resto = partes[1].strip()
                
                if '|' in resto:
                    estado_destino, transicao_str = resto.split('|', 1)
                    estado_destino = estado_destino.strip()
                    transicao_info = transicao_str.strip().split(',')
                    
                    if len(transicao_info) >= 3:
                        simbolo = transicao_info[0].strip()
                        topo_pilha = transicao_info[1].strip()
                        empilha = transicao_info[2].strip()
                        
                        chave = (estado_origem, simbolo, topo_pilha)
                        dicionario_transicoes[chave] = (estado_destino, empilha)
            i += 1
        
        return estado_inicial, estados_finais, dicionario_transicoes
    
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None, None, None
    except Exception as e:
        print(f"Erro ao ler o arquivo: {e}")
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

def processar_pilha(simbolo, acao_pilha):
    global pilha_reacoes
    
    if simbolo not in ingrediente:
        return False
    
    reacao_atual = ingrediente[simbolo]['reacao']
    
    print(f"\n➕ Adicionando {ingrediente[simbolo]['nome']}...")
    print(f"   Propriedade/Reação: {reacao_atual}")
    
    # Executar ação da pilha conforme definido no autômato
    if acao_pilha == 'empilha':
        pilha_reacoes.append(reacao_atual)
        print(f"   📤 '{reacao_atual}' empilhada!")
    elif acao_pilha == 'desempilha':
        if pilha_reacoes:
            removido = pilha_reacoes.pop()
            print(f"   📥 '{removido}' desempilhada!")
        else:
            print(f"   ⚠️  Tentou desempilhar pilha vazia!")
            return False
    elif acao_pilha == 'nao_empilha':
        print(f"   ➡️  Sem ação na pilha")
    
    mostrar_pilha()
    return True

def realizar_transicao_apd(estado_atual, simbolo, dicionario):

    # Determinar topo da pilha para transição
    topo_pilha = pilha_reacoes[-1] if pilha_reacoes else 'vazio'
    
    # Procurar transição exata
    chave_exata = (estado_atual, simbolo, topo_pilha)
    if chave_exata in dicionario:
        novo_estado, acao_pilha = dicionario[chave_exata]
        return novo_estado, acao_pilha
    
    # Procurar transição genérica (qualquer topo de pilha)
    chave_generica = (estado_atual, simbolo, '*')
    if chave_generica in dicionario:
        novo_estado, acao_pilha = dicionario[chave_generica]
        return novo_estado, acao_pilha
    
    # Procurar transição com pilha vazia
    chave_vazia = (estado_atual, simbolo, 'vazio')
    if chave_vazia in dicionario:
        novo_estado, acao_pilha = dicionario[chave_vazia]
        return novo_estado, acao_pilha
    
    return None, None

def verificar_poção_finalizada():
    """Verifica se a poção está em um estado estável (pilha balanceada)"""
    if not pilha_reacoes:
        return True, "Poção perfeitamente balanceada! ⚖️"
    elif len(pilha_reacoes) == 1:
        return True, f"Poção com efeito dominante: {pilha_reacoes[0]} ✨"
    elif len(pilha_reacoes) <= 3:
        return True, f"Poção complexa com múltiplos efeitos: {', '.join(pilha_reacoes)} 🌟"
    else:
        return False, f"Poção instável! Muitas reações ativas: {len(pilha_reacoes)} reações 💥"

def main():
    
    print("=" * 60)
    print("🧙 SIMULADOR DE POÇÕES - AUTÔMATO DE PILHA 🧙")
    print("=" * 60)
    print("Ingredientes causam reações que são empilhadas na poção!")
    print("Alguns ingredientes podem neutralizar reações opostas.\n")
    
    # Tentar ler arquivo, senão usar padrão
    nome_arquivo = 'automato_pilha.txt'
    estado_inicial, estados_finais, dicionario_transicoes = ler_automato_pilha(nome_arquivo)
    
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
    
    # Pergunta pelo primeiro ingrediente
    print("\n" + "─" * 50)
    print("🥄 Insira o símbolo do primeiro ingrediente da receita:")
    primeiro_ingrediente = input(">>> ").strip().lower()
    
    if primeiro_ingrediente not in alfabeto:
        print("❌ Ingrediente inválido!")
        return
    
    ingredientes.append(primeiro_ingrediente)
    novo_estado, acao_pilha = realizar_transicao_apd(estado_inicial, primeiro_ingrediente, dicionario_transicoes)
    
    if novo_estado is None:
        print("❌ Transição inválida!")
        return
    elif novo_estado == 'e':
        print("💥 ERRO: Combinação de ingredientes incompatível!")
        return
    
    # Processar ação na pilha
    if not processar_pilha(primeiro_ingrediente, acao_pilha):
        print("💥 ERRO: Falha ao processar pilha!")
        return
    
    estado_atual = novo_estado
    print(f"📍 Estado atual: {estado_atual}")
    
    # Loop para mais ingredientes
    while True:
        print("\n" + "─" * 50)
        print("❓ Deseja inserir mais um ingrediente? (s/n)")
        resposta = input(">>> ").strip().lower()
        
        if resposta == 's':
            print("🥄 Qual ingrediente será inserido:")
            ingrediente_simbolo = input(">>> ").strip().lower()
            
            if ingrediente_simbolo not in alfabeto:
                print("❌ Ingrediente inválido!")
                continue
            
            ingredientes.append(ingrediente_simbolo)
            novo_estado, acao_pilha = realizar_transicao_apd(estado_atual, ingrediente_simbolo, dicionario_transicoes)
            
            if novo_estado is None:
                print("❌ Transição inválida!")
                break
            elif novo_estado == 'e':
                print("💥 ERRO: Combinação de ingredientes incompatível!")
                break
            
            # Processar ação na pilha
            if not processar_pilha(ingrediente_simbolo, acao_pilha):
                print("💥 ERRO: Falha ao processar pilha!")
                break
            
            estado_atual = novo_estado
            print(f"📍 Estado atual: {estado_atual}")
            
        elif resposta == 'n':
            break
        else:
            print("❌ Resposta inválida. Digite 's' para sim ou 'n' para não.")
    
    # Verificar resultado final
    print("\n" + "=" * 60)
    print("🏁 RESULTADO FINAL")
    print("=" * 60)
    
    print(f"📝 Ingredientes utilizados: {' -> '.join(ingredientes)}")
    print(f"📍 Estado final: {estado_atual}")
    
    if estado_atual in estados_finais:
        estavel, mensagem = verificar_poção_finalizada()
        if estavel:
            print(f"✅ SUCESSO: {mensagem}")
        else:
            print(f"⚠️  ATENÇÃO: {mensagem}")
        
        mostrar_pilha()
        
        if pilha_reacoes:
            print(f"\n🔬 Análise da poção:")
            print(f"   • Número de reações ativas: {len(pilha_reacoes)}")
            print(f"   • Reação dominante (topo): {pilha_reacoes[-1]}")
            if len(pilha_reacoes) > 1:
                print(f"   • Reações em segundo plano: {', '.join(pilha_reacoes[:-1])}")
    else:
        print("❌ ERRO: A receita não foi completada adequadamente!")
        mostrar_pilha()
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()