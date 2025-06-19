# main.py - Versão com dados centralizados
from APD import executar_simulador_pilha
from AFD import executar_simulador_arquivo

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
    print("🧙 Bem-vindo ao Simulador de Poções!")
    print("Escolha o tipo de autômato que deseja executar:")
    print("1 - Autômato de Pilha (APD)")
    print("2 - Autômato simples (sem pilha, lido de arquivo)")
    
    escolha = input("Digite 1 ou 2: ").strip()
    
    if escolha == '1':
        # Passa os dados como parâmetros
        executar_simulador_pilha(alfabeto, ingredientes)
    elif escolha == '2':
        # Passa os dados como parâmetros
        executar_simulador_arquivo(alfabeto, ingredientes)
    else:
        print("❌ Escolha inválida!")

if __name__ == "__main__":
    main()