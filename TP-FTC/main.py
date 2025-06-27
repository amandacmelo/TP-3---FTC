# main.py - Versão com dados centralizados
from os import system
from APD import executar_simulador_pilha
from AFD import executar_simulador_arquivo
from Turing import executar_maquina_turing
from Mealy import executar_simulador_mealy
from Moore import executar_simulador_moore

# ==================== DADOS CENTRALIZADOS ====================
# alfabeto único para todo o sistema
alfabeto = {'a', 'p', 'o', 'd', 'c', 's', 'e'}

# Dicionário de ingredientes único
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

def main():
    sair = False
    while not sair:
        print(
            '   ° o   \n'
            ' _ o_° o \n'
            ' /  \\  ° \n'
            ' \\__/    ' "Bem-vindo ao Simulador de Poções! \n")

        print("╔══════════════════════════════╗")
        print("║   MENU OPÇÕES DE AUTOMATO:   ║")
        print("╠══════════════════════════════╣")
        print("║ 1) Autômato AFD              ║")
        print("║ 2) Autômato de Pilha (APD)   ║")
        print("║ 3) Máquina de Moore          ║")
        print("║ 4) Máquina de Mealy          ║")
        print("║ 5) Máquina de Turing         ║")
        print("╠══════════════════════════════╣")
        print("║ 6) Sair                      ║")
        print("╚══════════════════════════════╝")

        escolha = input("Digite sua escolha: ").strip()

        if escolha == '1':
            print("╔══════════════════════════════╗")
            print("║   Automato AFD Selecionado   ║")
            print("╚══════════════════════════════╝")
            executar_simulador_arquivo(alfabeto, ingredientes)
        elif escolha == '2':
            print("╔══════════════════════════════╗")
            print("║   Automato APD Selecionado   ║")
            print("╚══════════════════════════════╝")
            executar_simulador_pilha(alfabeto, ingredientes)
        elif escolha == '3':
            print("╔══════════════════════════════╗")
            print("║ Maquina de Moore Selecionada ║")
            print("╚══════════════════════════════╝")
            executar_simulador_moore(alfabeto, ingredientes)
        elif escolha == '4':
            print("╔══════════════════════════════╗")
            print("║ Maquina de Mealy Selecionada ║")
            print("╚══════════════════════════════╝")
            executar_simulador_mealy(alfabeto, ingredientes)
        elif escolha == '5':
            print("╔══════════════════════════════╗")
            print("║ Maquina de Turing Selecionada║")
            print("╚══════════════════════════════╝")
            executar_maquina_turing()
        elif escolha == '6':
            sair = True
            print("Saindo do simulador...\n")
            print('  ° o \n'
                  ' _ o_° o \n'
                  ' /  \\  ° \n'
                  '/____\\    Até a proxima.... \n')
            break
        else:
            print("Escolha inválida!")

        if not sair:
            sair_input = input("Deseja voltar ao menu principal? (s/n): ").strip().lower()
            #system.clear()
            if sair_input not in ['s', 'sim']:
                sair = True
                print("Saindo do simulador...\n")

if __name__ == "__main__":
    main()



