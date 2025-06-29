import os
import time
# Códigos de cor ANSI para destacar o histórico
VERMELHO = '\033[91m'  # Erro
VERDE = '\033[92m'     # Estado final
AMARELO = '\033[93m'   # Estado atual
RESET = '\033[0m'      # Resetar para cor padrao

# Ingredientes validos (alfabeto)
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


# Le o conteudo de um autômato a partir de uma lista de strings
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
    # Transicao: estado_atual -> prox_estado | simbolos 
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


# Exibe o dicionario de transicoes do automato
def imprime_dicionario(dicionario, finais, inicial):
    linhas = []
    linhas.append("\n╔══════════════════════════════════════════════╗")
    linhas.append("║          DICIONÁRIO DE TRANSIÇÕES            ║")
    linhas.append("╠═════════════════╦═══════════╦════════════════╣")
    linhas.append("║  Estado Atual   ║  Símbolo  ║ Próximo Estado ║")
    linhas.append("╠═════════════════╬═══════════╬════════════════╣")
    
    for (estado_atual, simbolo), destino in dicionario.items():
        if destino != "erro":
            # Decide cor da linha inteira
            if estado_atual in finais:
                cor = VERDE
            elif estado_atual == inicial:
                cor = AMARELO
            else:
                cor = RESET

            # Linha com cor aplicada a todos os campos
            linha = (
                f"║ {cor}{estado_atual:^15}{RESET} ║ "
                f"{cor}{simbolo:^9}{RESET} ║ "
                f"{cor}{destino:^14}{RESET} ║"
            )
            linhas.append(linha)
            linhas.append("╠═════════════════╬═══════════╬════════════════╣")

    # Corrige o rodapé
    linhas[-1] = "╚═════════════════╩═══════════╩════════════════╝"
    for linha in linhas:
        print(linha)


    print("╔══════════════════════════════════════════════╗")
    print(f"║ Estado Inicial: {inicial:<29}║")
    print(f"║ Estado(s) Final(is): {', '.join(finais):<24}║")
    print("╚══════════════════════════════════════════════╝")


# Realiza a transicao de estado
def realizar_transicao(estado_atual, simbolo, transicoes):
    return transicoes.get((estado_atual, simbolo))


# Funcao principal de execucao do simulador
def executar_simulador_arquivo(alfabeto, ingredientes, conteudo_arquivo):
    estado_inicial, estados_finais, dicionario_transicoes = ler_automato(conteudo_arquivo)

    if estado_inicial is None:
        print("Não foi possível carregar o autômato.")
        return

    ingredientes_usados = []
    estado_atual = estado_inicial
    historico_transicoes = []

    imprime_dicionario(dicionario_transicoes, estados_finais, estado_inicial)

    while True:
        limpar_tela()
        imprime_dicionario(dicionario_transicoes, estados_finais, estado_inicial)
        if historico_transicoes:
            print("\n╔══════════════════════════════════════════════════╗")
            print("║           📜 HISTÓRICO DE TRANSIÇÕES             ║")
            print("╠════════════╦════════════════════════╦════════════╣")
            print("║   Origem   ║         Símbolo        ║  Destino   ║")
            print("╠════════════╬════════════════════════╬════════════╣")
            for i, (origem, simb, destino) in enumerate(historico_transicoes):
                cor = ""
                # Definindo a cor da linha
                if destino == "erro":
                    cor = VERMELHO
                elif destino in estados_finais:
                    cor = VERDE
                elif i == len(historico_transicoes) - 1:
                    cor = AMARELO
               
                else:
                    cor = RESET
                print(f"║{cor} {origem:^10} {RESET}║  {cor} {ingredientes[str(simb)]['nome']:^20}{RESET} ║ {cor}{destino:^10}{RESET} ║")
            print("╚════════════╩════════════════════════╩════════════╝")

        ingrediente = input("\nInsira um ingrediente (a, p, o, d, c, s): ").strip().lower()
        if ingrediente not in alfabeto:
            print(f"Ingrediente '{ingrediente}' inválido! Ingredientes válidos: {', '.join(alfabeto)}")
            time.sleep(1)
            continue

        ingredientes_usados.append(ingrediente)
        novo_estado = realizar_transicao(estado_atual, ingrediente, dicionario_transicoes)
       
        # possiveis erros nao relatados no txt
        if novo_estado is None:
            novo_estado = 'erro'

        historico_transicoes.append((estado_atual, ingrediente, novo_estado))
        print("\n╔══════════════════════════════════════════════════╗")
        print("║           📜 HISTÓRICO DE TRANSIÇÕES             ║")
        print("╠════════════╦════════════════════════╦════════════╣")
        print("║   Origem   ║         Símbolo        ║  Destino   ║")
        print("╠════════════╬════════════════════════╬════════════╣")
        for i, (origem, simb, destino) in enumerate(historico_transicoes):
            cor = ""

            # Definindo a cor da linha
            if destino == "erro":
                cor = VERMELHO
            elif destino in estados_finais:
                cor = VERDE
            elif i == len(historico_transicoes) - 1:
                cor = AMARELO
            
            else:
                cor = RESET
            print(f"║{cor} {origem:^10} {RESET}║  {cor} {ingredientes[str(simb)]['nome']:^20}{RESET} ║ {cor}{destino:^10}{RESET} ║")
        print("╚════════════╩════════════════════════╩════════════╝")

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
    print(f"║ Ingredientes inseridos:  {', '.join(ingredientes_usados):<60}║")
    print(f"║ Estado final da execução: {estado_atual:<59}║")

    if estado_atual == 'erro':
        print("║ Resultado:   O autômato entrou em um estado de erro (transição inválida).            ║")
    elif estado_atual in estados_finais:
        print("║ Resultado:   A poção foi concluída com sucesso! Estado final alcançado!            ║")
    else:
        print("║ Resultado:   A execução terminou sem atingir um estado final.                       ║")
    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")

