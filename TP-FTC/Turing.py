import os
import time

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def move_cabecote(cabecote, direcao):
    if direcao.upper() == 'D':
        cabecote += 1
    elif direcao.upper() == 'E':
        cabecote -= 1
        if cabecote < 1:  # não deixa passar da posição 〈
            cabecote = 1
    return cabecote

# Leitura do arquivo da máquina de Turing
def ler_maquina_turing(linhas):
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

    # Resto: transições
    while i < len(linhas):
        linha = linhas[i]
        if '->' in linha:
            partes = linha.split('->')
            chave = tuple(partes[0].strip().split())  # (estado_atual, simbolo_lido)
            resultado = partes[1].strip().split()     # (novo_estado, simbolo_escrito, direção)

            if len(chave) == 2 and len(resultado) == 3:
                dicionario_transicoes[(chave[0], chave[1])] = (resultado[0], resultado[1], resultado[2])
        i += 1

    return estado_inicial, estados_finais, dicionario_transicoes

def imprime_dicionario(dicionario_transicoes, ingredientes, estado_inicial, estados_finais):
    linhas = []
    linhas.append("╔══════════════════╦═══════════════════╦════════════════╦══════════════════════╦══════════════╗")
    linhas.append("║   Estado Atual   ║   Símbolo Lido    ║   Novo Estado  ║   Símbolo Escrito    ║   Direção    ║")
    linhas.append("╠══════════════════╬═══════════════════╬════════════════╬══════════════════════╬══════════════╣")

    for (estado_atual, simbolo_lido), (novo_estado, simbolo_escrito, direcao) in dicionario_transicoes.items():
        linhas.append(f"║ {estado_atual:^16} ║ {ingredientes[simbolo_lido]['nome']:^17} ║ {novo_estado:^14} ║ {ingredientes[simbolo_escrito]['nome']:^20} ║ {direcao:^12} ║")
        linhas.append("╠══════════════════╬═══════════════════╬════════════════╬══════════════════════╬══════════════╣")

    # Substitui a última linha pelo rodapé da tabela
    linhas[-1] ="╚══════════════════╩═══════════════════╩════════════════╩══════════════════════╩══════════════╝"

    for linha in linhas:
        print(linha)
    print("╔═════════════════════════════════════════════════════════════════════════════════════════════╗") 
    print(f"║ Estado Inicial: {estado_inicial:<76}║")
    print(f"║ Estado(s) Final(is): {', '.join(estados_finais):<71}║")
    print("╚═════════════════════════════════════════════════════════════════════════════════════════════╝")

def exibir_fita(fita, cabecote):
    RED = '\033[91m'
    RESET = '\033[0m'

    print("\n🧪 Fita Completa:")

    # Linha da fita com destaque na posição do cabeçote
    visual_fita = ""
    for i, simbolo in enumerate(fita):
        if i == cabecote:
            visual_fita += f"{RED}{simbolo}{RESET} "  # Cor vermelha
        else:
            visual_fita += f"{simbolo} "
    print(visual_fita.strip())



def executar_maquina_turing(conteudo_arquivo, alfabeto, ingredientes):
    estado_inicial, estados_finais, dicionario = ler_maquina_turing(conteudo_arquivo)
    if dicionario is None:
        print(" Erro: Arquivo maquina_turing.txt não encontrado ou está mal formatado.")
        return
    estado_atual = estado_inicial
    historico = []
    imprime_dicionario(dicionario, ingredientes, estado_inicial, estados_finais)  #  Imprime o dicionário no início

    fita = ['〈'] + ['_'] * 50 #〈 ocupa a posição 0

    cabecote = 1
    estado_erro = False  # Indicador de erro

    while True:

        limpar_tela()
        imprime_dicionario(dicionario, ingredientes, estado_inicial, estados_finais)  #  Imprime o dicionário para auxiliar
        if historico != []:
            print("\n╔═════════════════════════════════════════════════════════════════════════════════════════════╗")
            print("║                               📜 HISTÓRICO DE TRANSIÇÕES                                    ║")
            print("╠══════════════════╦═══════════════════╦════════════════╦══════════════════════╦══════════════╣")
            print("║   Estado Atual   ║   Símbolo Lido    ║   Novo Estado  ║   Símbolo Escrito    ║   Direção    ║")
            print("╠══════════════════╬═══════════════════╬════════════════╬══════════════════════╬══════════════╣")
            for atual, lido, proximo, escrito, direcao in historico:
                print(f"║ {atual:^16} ║ {ingredientes[lido]['nome']:^17} ║ {proximo:^14} ║ {ingredientes[lido]['nome']:^20} ║ {direcao:^12} ║")
            print("╚══════════════════╩═══════════════════╩════════════════╩══════════════════════╩══════════════╝")
            exibir_fita(fita, cabecote)
        simbolo_lido = input("Insira um ingrediente (a, p, o, d, c, s): ").strip().lower()

        if simbolo_lido not in alfabeto:
            print(" Ingrediente inválido! Insira apenas (a, p, o, d, c, s).\n")
            continue
        
        # Realiza uma transiçao
        chave = (estado_atual, simbolo_lido)

        if chave in dicionario:
            novo_estado, simbolo_escrito, direcao = dicionario[chave]
            fita[cabecote] = simbolo_escrito
            estado_atual = novo_estado
            cabecote = move_cabecote(cabecote, direcao)
            historico.append((estado_atual, simbolo_lido, novo_estado, simbolo_escrito, direcao))
            print("\n╔═════════════════════════════════════════════════════════════════════════════════════════════╗")
            print("║                               📜 HISTÓRICO DE TRANSIÇÕES                                    ║")
            print("╠══════════════════╦═══════════════════╦════════════════╦══════════════════════╦══════════════╣")
            print("║   Estado Atual   ║   Símbolo Lido    ║   Novo Estado  ║   Símbolo Escrito    ║   Direção    ║")
            print("╠══════════════════╬═══════════════════╬════════════════╬══════════════════════╬══════════════╣")
            for atual, lido, proximo, escrito, direcao in historico:
                print(f"║ {atual:^16} ║ {ingredientes[lido]['nome']:^17} ║ {proximo:^14} ║ {ingredientes[lido]['nome']:^20} ║ {direcao:^12} ║")
            print("╚══════════════════╩═══════════════════╩════════════════╩══════════════════════╩══════════════╝")
            exibir_fita(fita, cabecote)
        else:
            print(f"⚠️ Atenção: Transição inexistente para ({estado_atual}, '{simbolo_lido}'). Cabeçote permanece.")
            estado_erro = True  # Marca que houve transição inválida



        resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        while resposta not in ('s', 'n'):
            print("Opção inválida! Tente novamente.")
            resposta = input("\nDeseja inserir mais um ingrediente (s/n)? ").strip().lower()
        if resposta != 's':
            break

    print("\n╔══════════════════════════════════════════════════════════════════════════════════════╗")
    print("║                                 🌟 RESULTADO FINAL 🌟                                ║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")
    print(f"║ Estado inicial da execução: {estado_inicial:<57}║")
    print(f"║ Estado final da execução:   {estado_atual:<57}║")
    intensidade = cabecote + 1
    print(f"║ Intensidade da poção:     🔥{intensidade:<57}║")
    print("╠══════════════════════════════════════════════════════════════════════════════════════╣")


    # Mensagens de aviso e resultado
    if estado_erro:
        print("║ Resultado:   A máquina entrou em um estado de erro (transição inválida).             ║")
    elif estado_atual not in estados_finais:
        print("║ Resultado:   A execução terminou sem atingir um estado final.                        ║")
    else:
        print("║ Resultado:   A execução terminou corretamente em um estado final.                    ║")

    print("╚══════════════════════════════════════════════════════════════════════════════════════╝")


