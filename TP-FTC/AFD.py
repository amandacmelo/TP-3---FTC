import os
import time

# Ingredientes válidos (alfabeto)
'''
Ingredientes:
  a - água
  p - pétalas
  o - óleo
  d - dente de dragão
  c - costela de adão
  s - sapo
'''

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


# Lê o conteúdo de um autômato a partir de uma lista de strings
def ler_automato(linhas):
    estado_inicial = None
    estados_finais = set()
    dicionario_transicoes = {}
    i = 0

    if linhas[i].startswith('Q:'):
        i += 1
    if linhas[i].startswith('I:'):
        estado_inicial = linhas[i][2:].strip()
        i += 1
    if linhas[i].startswith('F:'):
        estados_finais_str = linhas[i][2:].strip()
        if estados_finais_str:
            estados_finais = set(estados_finais_str.split())
        i += 1

    while i < len(linhas):
        linha = linhas[i]
        if '->' in linha:
            partes = linha.split('->')
            estado_origem = partes[0].strip()
            resto = partes[1].strip()

            if '|' in resto:
                estado_destino, simbolos_str = resto.split('|', 1)
                estado_destino = estado_destino.strip()
                simbolos = simbolos_str.strip().split()
                for simbolo in simbolos:
                    chave = (estado_origem, simbolo)
                    dicionario_transicoes[chave] = estado_destino
        i += 1

    return estado_inicial, estados_finais, dicionario_transicoes


# Exibe o dicionário de transições do autômato
def imprime_dicionario(dicionario, finais, inicial):
    print("\n╔══════════════════════════════════════════════╗")
    print("║          DICIONÁRIO DE TRANSIÇÕES            ║")
    print("╠═════════════════╦═══════════╦════════════════╣")
    print("║  Estado Atual   ║  Símbolo  ║ Próximo Estado ║")
    print("╠═════════════════╬═══════════╬════════════════╣")
    for (estado_atual, simbolo), destino in dicionario.items():
        if destino != "erro":
            print(f"║ {estado_atual:^15} ║ {simbolo:^9} ║ {destino:^14} ║")
        print("╠═════════════════╬═══════════╬════════════════╣")
    print("╚═════════════════╩═══════════╩════════════════╝")
    print("╔══════════════════════════════════════════════╗")
    print(f"║ Estado Inicial: {inicial:<29}║")
    print(f"║ Estado(s) Final(is): {', '.join(finais):<24}║")
    print("╚══════════════════════════════════════════════╝")


# Realiza a transição de estado
def realizar_transicao(estado_atual, simbolo, transicoes):
    return transicoes.get((estado_atual, simbolo))


# Função principal de execução do simulador
def executar_simulador_arquivo(alfabeto, ingredientes, conteudo_arquivo):
    estado_inicial, estados_finais, dicionario_transicoes = ler_automato(conteudo_arquivo)

    if estado_inicial is None:
        print("Não foi possível carregar o autômato.")
        return

    ingredientes = []
    estado_atual = estado_inicial
    historico_transicoes = []

    imprime_dicionario(dicionario_transicoes, estados_finais, estado_inicial)

    while True:
        limpar_tela()
        imprime_dicionario(dicionario_transicoes, estados_finais, estado_inicial)
        if historico_transicoes:
            print("\n╔══════════════════════════════════════════════╗")
            print("║         📜 HISTÓRICO DE TRANSIÇÕES           ║")
            print("╠════════════╦══════════╦══════════════════════╣")
            print("║   Origem   ║ Símbolo  ║       Destino        ║")
            print("╠════════════╬══════════╬══════════════════════╣")
            for origem, simb, destino in historico_transicoes:
                print(f"║ {origem:^10} ║ {simb:^8} ║ {destino:^20} ║")
            print("╚════════════╩══════════╩══════════════════════╝")

        ingrediente = input("\nInsira um ingrediente (a, p, o, d, c, s): ").strip().lower()
        if ingrediente not in alfabeto:
            print(f"Ingrediente '{ingrediente}' inválido! Ingredientes válidos: {', '.join(alfabeto)}")
            time.sleep(1)
            continue

        ingredientes.append(ingrediente)
        novo_estado = realizar_transicao(estado_atual, ingrediente, dicionario_transicoes)

        historico_transicoes.append((estado_atual, ingrediente, novo_estado))
        print("\n╔══════════════════════════════════════════════╗")
        print("║         📜 HISTÓRICO DE TRANSIÇÕES           ║")
        print("╠════════════╦══════════╦══════════════════════╣")
        print("║   Origem   ║ Símbolo  ║       Destino        ║")
        print("╠════════════╬══════════╬══════════════════════╣")
        for origem, simb, destino in historico_transicoes:
            print(f"║ {origem:^10} ║ {simb:^8} ║ {destino:^20} ║")
        print("╚════════════╩══════════╩══════════════════════╝")
        estado_atual = novo_estado

        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        while resposta not in ('s', 'n'):
            print("Opção inválida! Tente novamente.")
            resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            break

    # Resultado final
    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                 🌟 RESULTADO FINAL 🌟                                ║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ Ingredientes inseridos:  {', '.join(ingredientes):<60}║")
    print(f"║ Estado final da execução: {estado_atual:<59}║")

    if estado_atual == 'erro':
        print("║ Resultado:   O autômato entrou em um estado de erro (transição inválida).            ║")
    elif estado_atual in estados_finais:
        print("║ Resultado:   A poção foi concluída com sucesso! Estado final alcançado!            ║")
    else:
        print("║ Resultado:   A execução terminou sem atingir um estado final.                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")

