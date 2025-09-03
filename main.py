# main.py
from ui_manager import App
from database import init_db
import matplotlib

# Importações necessárias para definir o AppUserModelID
import sys
import ctypes
from ctypes import wintypes

# Define o backend do Matplotlib antes de qualquer outra coisa
matplotlib.use('TkAgg')

def main():
    """
    Função principal que configura e executa a aplicação.
    """
    # No Windows, define um AppUserModelID explícito para garantir que o 
    # ícone correto seja exibido na barra de tarefas.
    if sys.platform == 'win32':
        # Este ID é uma string única que identifica seu programa para o Windows.
        # Formato recomendado: NomeDaEmpresa.NomeDoProduto.Versao
        myappid = 'Fisk.FollowUp.1.0' 
        try:
            # Chama a função da API do Windows para definir o ID
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except AttributeError:
            # Acontece em versões muito antigas do Windows. Pode ser ignorado.
            pass

    # Garante que a tabela do banco de dados exista com todas as colunas
    init_db()
    
    # Cria e executa a aplicação
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()