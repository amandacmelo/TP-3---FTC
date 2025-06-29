from os import system
from APD import executar_simulador_pilha
from AFD import executar_simulador_arquivo
from Turing import executar_maquina_turing
from Mealy import executar_simulador_mealy
from Moore import executar_simulador_moore
import os
import time

ROXO = '\033[95m'
RESET = '\033[0m'

# Alfabeto geral do sistema (baseado nas iniciais dos ingredientes)
alfabeto = {'a', 'p', 'o', 'd', 'c', 's', 'e'}

# Ingredientes e seus efeitos

# Dicionario de ingredientes
ingredientes = {
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

def limpar_terminal():
    comando = 'cls' if os.name == 'nt' else 'clear'
    os.system(comando)

def ler_arquivo(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as f:
            linhas = [linha.strip() for linha in f if linha.strip()]
        print(f"\nArquivo '{nome_arquivo}' carregado com sucesso!\n")
        return linhas
    except FileNotFoundError:
        print(f"\nArquivo '{nome_arquivo}' não encontrado. Tente novamente.\n")
        return None

def selecionar_arquivo(arquivo_padrao):
    print("╔════════════════════════════════════╗")
    print("║ Deseja usar qual tipo de arquivo?  ║")
    print("╠════════════════════════════════════╣")
    print("║ 1) Usar arquivo padrão             ║")
    print("║ 2) Informar um novo arquivo        ║")
    print("╚════════════════════════════════════╝")

    opcao = input("Digite sua escolha: ").strip()

    if opcao == '1':
        return ler_arquivo(arquivo_padrao)
    elif opcao == '2':
        nome_arquivo = input("Digite o nome do arquivo (ex: exemplo.txt): ").strip()
        return ler_arquivo(nome_arquivo)
    else:
        print("Opção inválida!")
        return None

def mostrar_menu_principal():
    print(ROXO + 
      '   ° o   \n'
      ' _ o_° o \n'
      ' /  \\  ° \n'
      ' \\__/    Bem-vindo ao Simulador de Poções!\n' + 
      RESET)
    print("╔══════════════════════════════╗")
    print("║   MENU OPÇÕES DE AUTÔMATO:   ║")
    print("╠══════════════════════════════╣")
    print("║ 1) Autômato AFD              ║")
    print("║ 2) Autômato de Pilha (APD)   ║")
    print("║ 3) Máquina de Moore          ║")
    print("║ 4) Máquina de Mealy          ║")
    print("║ 5) Máquina de Turing         ║")
    print("║ 6) Sair                      ║")
    print("╚══════════════════════════════╝")

def main():
    sair = False

    while not sair:
        mostrar_menu_principal()
        escolha = input("Digite sua escolha: ").strip()

        match escolha:
            case '1':
                print("╔══════════════════════════════╗")
                print("║   Autômato AFD Selecionado   ║")
                print("╚══════════════════════════════╝")
                conteudo = selecionar_arquivo("Entradas/automato.txt")
                if conteudo:
                    time.sleep(1)
                    limpar_terminal()
                    executar_simulador_arquivo(alfabeto, ingredientes, conteudo)

            case '2':
                print("╔══════════════════════════════╗")
                print("║   Autômato APD Selecionado   ║")
                print("╚══════════════════════════════╝")
                conteudo = selecionar_arquivo("Entradas/automato_pilha.txt")
                if conteudo:
                    time.sleep(1)
                    limpar_terminal()
                    executar_simulador_pilha(alfabeto, ingredientes, conteudo)

            case '3':
                print("╔══════════════════════════════╗")
                print("║ Máquina de Moore Selecionada ║")
                print("╚══════════════════════════════╝")
                conteudo = selecionar_arquivo("Entradas/maquina_moore.txt")
                if conteudo:
                    time.sleep(1)
                    limpar_terminal()
                    executar_simulador_moore(alfabeto, ingredientes, conteudo)

            case '4':
                print("╔══════════════════════════════╗")
                print("║ Máquina de Mealy Selecionada ║")
                print("╚══════════════════════════════╝")
                conteudo = selecionar_arquivo("Entradas/maquina_mealy.txt")
                if conteudo:
                    time.sleep(1)
                    limpar_terminal()
                    executar_simulador_mealy(alfabeto, ingredientes, conteudo)

            case '5':
                print("╔══════════════════════════════╗")
                print("║ Máquina de Turing Selecionada║")
                print("╚══════════════════════════════╝")
                conteudo = selecionar_arquivo("Entradas/maquina_turing.txt")
                if conteudo:
                    time.sleep(1)
                    limpar_terminal()
                    executar_maquina_turing(conteudo, alfabeto, ingredientes)

            case '6':
                sair = True
                print("Saindo do simulador...\n")
                print(ROXO +'  ° o \n'
                      ' _ o_° o \n'
                      ' /  \\  ° \n'
                      '/____\\    Até a próxima.... \n' + RESET)
                break

            case _:
                print("Escolha inválida!")

        if not sair:
            voltar = input("Deseja voltar ao menu principal? (s/n): ").strip().lower()
            if voltar not in ['s', 'sim']:
                sair = True
                print("Saindo do simulador...\n")
            limpar_terminal()

if __name__ == "__main__":
    main()
