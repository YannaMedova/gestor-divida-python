# Splash.py
# --- 1. IMPORTAÇÕES ---
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os
import sys
import subprocess


# --- 2. FUNÇÃO AUXILIAR PARA CAMINHOS ---
def resource_path(relative_path):
    """
    Retorna o caminho absoluto para um recurso (asset), funcionando tanto no modo de
    desenvolvimento (.py) quanto no modo empacotado (.exe).
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# --- 3. CONFIGURAÇÕES DA SPLASH SCREEN ---
SPLASH_IMAGE_PATH = resource_path("splash_image.png")
SPLASH_WIDTH = 400
SPLASH_HEIGHT = 200


# --- 4. FUNÇÃO PRINCIPAL DA SPLASH ---
def run_splash():
    root = tk.Tk()
    root.withdraw()
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)

    try:
        img = Image.open(SPLASH_IMAGE_PATH)
        img = img.resize((SPLASH_WIDTH, SPLASH_HEIGHT), Image.LANCZOS)
        photo = ImageTk.PhotoImage(img)
    except FileNotFoundError:
        messagebox.showerror("Erro Crítico",
                             f"A imagem da splash screen '{os.path.basename(SPLASH_IMAGE_PATH)}' não foi encontrada.")
        sys.exit(1)

    label = tk.Label(splash, image=photo, bg="white")
    label.pack()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (SPLASH_WIDTH // 2)
    y = (screen_height // 2) - (SPLASH_HEIGHT // 2)
    splash.geometry(f"{SPLASH_WIDTH}x{SPLASH_HEIGHT}+{x}+{y}")

    # Descobre o caminho para o diretório onde o Splash.exe está rodando
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(os.path.abspath(__file__))

    # Define o caminho para o arquivo de sinal e para o app principal
    signal_file = os.path.join(application_path, 'signal.tmp')
    path_to_app = os.path.join(application_path, 'Divida_Mayara', 'Divida_Mayara.exe')

    # Limpa qualquer arquivo de sinal antigo antes de começar
    if os.path.exists(signal_file):
        os.remove(signal_file)

    # Inicia o app.exe em um processo separado.
    try:
        subprocess.Popen([path_to_app])
    except FileNotFoundError:
        messagebox.showerror("Erro Crítico", f"Não foi possível encontrar o executável principal em:\n{path_to_app}")
        sys.exit(1)

    def close_splash():
        """Função que destrói a splash e apaga o arquivo de sinal."""
        if os.path.exists(signal_file):
            os.remove(signal_file)
        splash.destroy()
        root.destroy()

    def check_for_signal():
        """Verifica se o arquivo de sinal foi criado."""
        if os.path.exists(signal_file):
            close_splash()
        else:
            # Se não encontrou, verifica de novo em 100ms
            splash.after(100, check_for_signal)

    # Inicia a primeira verificação pelo sinal
    splash.after(100, check_for_signal)

    root.mainloop()


# --- 5. PONTO DE ENTRADA DO SCRIPT ---
if __name__ == '__main__':
    from PIL import ImageTk

    run_splash()