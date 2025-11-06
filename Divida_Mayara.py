# --- 1. IMPORTAÇÕES ---
# Importa as bibliotecas necessárias para o projeto.
import customtkinter  # A biblioteca para criar a interface gráfica.
import json  # Para ler e escrever dados no formato JSON (nosso arquivo de salvamento).
from datetime import datetime  # Para trabalhar com datas, como pegar o dia de hoje.
from tkinter import messagebox, filedialog  # Para mostrar caixas de diálogo (como a de "tem certeza?").
import csv
import uuid  # Para gerar identificadores únicos para cada pagamento.
import matplotlib.pyplot as plt #Importações para o Matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os
import sys
import tkinter as tk

def resource_path(relative_path):
    # Retorna o caminho absoluto para o recurso, funcionando tanto no modo de desenvolvimento quanto no PyInstaller
    try:
        # PyInstaller cria uma pasta temporária e armazena o caminho em _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# --- 2. CONFIGURAÇÕES INICIAIS DA JANELA ---
# Define a aparência padrão do programa (pode ser "System", "Dark", "Light").
customtkinter.set_appearance_mode("System")
# Define o tema de cores padrão.
customtkinter.set_default_color_theme("blue")

# Cria a janela principal da aplicação. A variável 'app' representa essa janela.
app = customtkinter.CTk()
app.iconbitmap(resource_path("Dollar.ico"))
# Define o texto que aparece na barra de título da janela.
app.title("Gestor de Dívida com a Mayara")
# Variáveis globais para o gráfico
fig = None # Armazenará o objeto Figure do Matplotlib
canvas_widget = None # Armazenará o widget do Canvas do CustomTkinter para o gráfico
app.geometry("800x850") # Define o tamanho inicial da janela (largura x altura).
label_total, label_pago, label_restante = None, None, None
scrollable_frame_pagamentos = None
entry_data, entry_valor = None, None
label_status = None
frame_grafico = None


# --- 3. FUNÇÕES DE LÓGICA  ---

def carregar_dados():
    #Lê o JSON e retorna os dados como um dicionário Python.
    #Se o arquivo não existir ou estiver vazio/corrompido, cria e retorna uma estrutura de dados padrão.

    try:
        with open(resource_path('dados_divida.json'), 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        # Caso o arquivo não exista ou dê erro na leitura, retorna um dicionário zerado.
        return {"divida_total_inicial": 0.0, "pagamentos": []}


def salvar_dados(dados):
    #Recebe um dicionário com os dados e o salva no arquivo JSON.
    #O 'indent=4' serve para deixar o arquivo JSON formatado e legível para humanos.

    with open(resource_path('dados_divida.json'), 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def popular_dados():
    #Lê os dados e redesenha as informações na tela.

    # 1. Limpa a lista de pagamentos antiga para não exibir itens duplicados.
    for widget in scrollable_frame_pagamentos.winfo_children():
        widget.destroy()

    # 2. Carrega os dados mais recentes do arquivo.
    dados = carregar_dados()

    # 3. Garante que pagamentos antigos (sem ID) recebam um ID para poderem ser editados/excluídos.
    precisa_salvar = False
    for pg in dados['pagamentos']:
        if 'id' not in pg:
            pg['id'] = str(uuid.uuid4())
            precisa_salvar = True
    if precisa_salvar:
        salvar_dados(dados)

    # 4. Calcula os totais.
    divida_inicial = dados.get('divida_total_inicial', 0.0)
    pagamentos = dados.get('pagamentos', [])
    total_pago = sum(pg['valor'] for pg in pagamentos)
    restante = divida_inicial - total_pago

    # 5. Atualiza os textos dos labels de resumo na tela.
    label_total.configure(text=f"Dívida Inicial: R$ {divida_inicial:.2f}")
    label_pago.configure(text=f"Total Pago: R$ {total_pago:.2f}")
    label_restante.configure(text=f"Falta Pagar: R$ {restante:.2f}")

    # 6. Ordena e exibe cada pagamento na lista rolável.
    if pagamentos:
        pagamentos_ordenados = sorted(pagamentos, key=lambda pg: datetime.strptime(pg['data'], '%d/%m/%Y'),
                                      reverse=True)
        for pagamento in pagamentos_ordenados:
            # Chama a função auxiliar para criar os elementos visuais de cada linha.
            criar_linha_pagamento(pagamento)

    desenhar_grafico_pizza(divida_inicial, total_pago) # Chama a função para desenhar/atualizar o gráfico


def criar_linha_pagamento(pagamento):
    #Cria os widgets (frame, texto e botões) para uma única linha no histórico de pagamentos.

    frame_linha = customtkinter.CTkFrame(master=scrollable_frame_pagamentos)
    frame_linha.pack(fill='x', padx=5, pady=3)

    # Vincula os eventos de entrada e saída do mouse às nossas novas funções
    frame_linha.bind("<Enter>", lambda event, frame=frame_linha: on_enter(frame))
    frame_linha.bind("<Leave>", lambda event, frame=frame_linha: on_leave(frame))

    info_texto = f"{pagamento['data']}  -  R$ {pagamento['valor']:.2f}"
    label_info = customtkinter.CTkLabel(master=frame_linha, text=info_texto, font=("Roboto", 14))
    label_info.pack(side='left', padx=10, pady=5)

    # Botão de Excluir: usa 'lambda' para passar o ID do pagamento específico desta linha.
    btn_excluir = customtkinter.CTkButton(
        master=frame_linha, text="Excluir", width=80, fg_color="red", hover_color="#C00000",
        command=lambda pg_id=pagamento['id']: excluir_pagamento(pg_id)
    )
    btn_excluir.pack(side='right', padx=5, pady=5)

    # Botão de Editar: usa 'lambda' para passar o objeto de pagamento completo para a função.
    btn_editar = customtkinter.CTkButton(
        master=frame_linha, text="Editar", width=80,
        command=lambda pg=pagamento: abrir_janela_edicao(pg)
    )
    btn_editar.pack(side='right', padx=5, pady=5)


def adicionar_pagamento():
    #Pega os dados dos campos de entrada, valida, e adiciona um novo pagamento ao arquivo de dados.

    label_status.configure(text="")
    data_pagamento = entry_data.get()
    valor_pagamento_str = entry_valor.get().replace(',', '.')

    # Validação dos dados de entrada.
    if not valor_pagamento_str or not data_pagamento:
        label_status.configure(text="Preencha a data e o valor, Inseta!", text_color="red")
        return
    try:
        datetime.strptime(data_pagamento, '%d/%m/%Y')
        valor_pagamento = float(valor_pagamento_str)
    except ValueError:
        label_status.configure(text="Use apenas números, Abestada!", text_color="red")
        return

    # Adicionar o pagamento.
    dados = carregar_dados()
    novo_pagamento = {
        "id": str(uuid.uuid4()),  # Cria um ID único para o novo pagamento.
        "data": data_pagamento,
        "valor": valor_pagamento
    }
    dados['pagamentos'].append(novo_pagamento)
    salvar_dados(dados)

    # Feedback visual para o usuário.
    label_status.configure(text=f"Pagamento adicionado!", text_color="green")
    entry_valor.delete(0, 'end')
    popular_dados()  # Atualiza a tela para mostrar o novo pagamento.


def excluir_pagamento(pagamento_id):
    #Encontra um pagamento pelo seu ID único e o remove da lista de pagamentos.

    if messagebox.askyesno("Confirmar Exclusão", "Tem certeza que deseja excluir este pagamento?"):
        dados = carregar_dados()
        # Recria a lista de pagamentos, mantendo apenas aqueles com ID diferente do que foi passado.
        dados['pagamentos'] = [pg for pg in dados['pagamentos'] if pg['id'] != pagamento_id]
        salvar_dados(dados)
        label_status.configure(text="Pagamento excluído com sucesso!", text_color="green")
        popular_dados()


def abrir_janela_edicao(pagamento):
    #Cria uma nova janela (Toplevel) para editar um pagamento existente.

    janela_edicao = customtkinter.CTkToplevel(app)
    janela_edicao.title("Editar Pagamento")
    janela_edicao.geometry("300x220")
    janela_edicao.transient(app)  # Faz a janela de edição aparecer na frente da principal.
    janela_edicao.grab_set()  # Bloqueia a interação com a janela principal enquanto a de edição estiver aberta.

    # Cria os campos de entrada (Entry) já preenchidos com os dados do pagamento.
    label_data = customtkinter.CTkLabel(janela_edicao, text="Data (dd/mm/aaaa)")
    label_data.pack(pady=(10, 0))
    edit_entry_data = customtkinter.CTkEntry(janela_edicao)
    edit_entry_data.insert(0, pagamento['data'])
    edit_entry_data.pack()

    label_valor = customtkinter.CTkLabel(janela_edicao, text="Valor")
    label_valor.pack(pady=(10, 0))
    edit_entry_valor = customtkinter.CTkEntry(janela_edicao)
    edit_entry_valor.insert(0, str(pagamento['valor']))
    edit_entry_valor.pack()

    status_edicao = customtkinter.CTkLabel(janela_edicao, text="")
    status_edicao.pack()

    # Função interna (aninhada) para salvar as alterações.
    def salvar_edicao():
        dados = carregar_dados()
        for pg in dados['pagamentos']:
            if pg['id'] == pagamento['id']:
                try:
                    # Valida os novos dados antes de salvar.
                    nova_data = edit_entry_data.get()
                    novo_valor = float(edit_entry_valor.get().replace(',', '.'))
                    datetime.strptime(nova_data, '%d/%m/%Y')
                    # Atualiza os dados no dicionário.
                    pg['data'] = nova_data
                    pg['valor'] = novo_valor
                    break  # Para o loop, pois já encontrou e atualizou o pagamento.
                except ValueError:
                    status_edicao.configure(text="Formato inválido!", text_color="red")
                    return
        salvar_dados(dados)
        janela_edicao.destroy()  # Fecha a janela de edição.
        label_status.configure(text="Pagamento editado com sucesso!", text_color="green")
        popular_dados()  # Atualiza a tela principal.

    # Função "ponte" para o evento do Enter na janela de edição.
    def salvar_edicao_event(event):
        salvar_edicao()

    # Vincula a tecla Enter ao campo de valor da edição.
    edit_entry_valor.bind("<Return>", salvar_edicao_event)

    btn_salvar = customtkinter.CTkButton(janela_edicao, text="Salvar", command=salvar_edicao)
    btn_salvar.pack(pady=10)


def adicionar_pagamento_event(event):
    #Função 'ponte' para o evento da tecla Enter na tela principal.
    adicionar_pagamento()


def on_closing():
    #Função chamada quando o usuário clica no 'X' para fechar a janela.
    if messagebox.askyesno("Sair", "Tem certeza que deseja sair?"):
        app.destroy()


def trocar_tema():
    #Verifica o tema atual e alterna entre 'Dark' e 'Light'.
    tema_atual = customtkinter.get_appearance_mode()
    if tema_atual == "Dark":
        customtkinter.set_appearance_mode("Light")
    else:
        customtkinter.set_appearance_mode("Dark")

    # MUDANÇA DEFINITIVA: Agendamos a atualização para 10ms depois.
    # Isso dá tempo para o Tkinter finalizar tudo antes de recriarmos o gráfico.
    app.after(10, popular_dados)

# Função para exportar os dados para um arquivo .csv
def exportar_para_csv():
    # Abre uma janela de 'Salvar como', carrega os dados e os escreve em um arquivo CSV.
    dados = carregar_dados()
    if not dados['pagamentos']:
        label_status.configure(text="Nenhum pagamento para exportar!", text_color="red")
        return

    # Sugere um nome de arquivo padrão com a data atual
    nome_arquivo_sugerido = f"relatorio_pagamentos_{datetime.now().strftime('%Y-%m-%d')}.csv"

    # Abre a janela de diálogo para o usuário escolher o local e nome do arquivo
    caminho_arquivo = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")],
        initialfile=nome_arquivo_sugerido
    )

    # Se o usuário cancelar a janela de salvar, o caminho será vazio.
    if not caminho_arquivo:
        # Informamos ao usuário que a ação foi cancelada. Usamos uma cor neutra.
        label_status.configure(text="Exportação cancelada pelo usuário.", text_color="orange")
        return

    try:
        # Abre o arquivo escolhido no modo de escrita
        with open(caminho_arquivo, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)

            # Escreve o resumo no topo do arquivo
            divida_inicial = dados.get('divida_total_inicial', 0.0)
            total_pago = sum(pg['valor'] for pg in dados['pagamentos'])
            restante = divida_inicial - total_pago

            writer.writerow(["Resumo da Dívida"])
            writer.writerow(["Dívida Inicial", f"R$ {divida_inicial:.2f}"])
            writer.writerow(["Total Pago", f"R$ {total_pago:.2f}"])
            writer.writerow(["Valor Restante", f"R$ {restante:.2f}"])
            writer.writerow([])  # Linha em branco para separar

            # Escreve o cabeçalho da tabela de pagamentos
            writer.writerow(["Data do Pagamento", "Valor Pago"])

            # Escreve cada pagamento em uma nova linha
            for pagamento in dados['pagamentos']:
                writer.writerow([pagamento['data'], pagamento['valor']])

        label_status.configure(text=f"Exportado com sucesso para:\n{caminho_arquivo}", text_color="green")

    except Exception as e:
        label_status.configure(text="Ocorreu um erro ao exportar!", text_color="red")
        print(f"Erro de exportação: {e}")


# Função para desenhar o gráfico de pizza
def desenhar_grafico_pizza(divida_inicial, total_pago):
    global fig, canvas_widget

    # PASSO 1: Destruir o widget do canvas antigo, se ele existir. Esta é a chave!
    if canvas_widget:
        canvas_widget.get_tk_widget().destroy()
        canvas_widget = None

    # Garante que não haja divisão por zero se a dívida inicial for 0
    if divida_inicial <= 0:
        return

    restante = divida_inicial - total_pago

    # Dados para o gráfico
    labels = ['Valor Pago', 'Falta Pagar']
    sizes = [total_pago, restante]
    colors = ['#4CAF50', '#FF5733']

    # PASSO 2: Criar uma NOVA figura do Matplotlib do zero
    # Não vamos mais reutilizar a antiga com fig.clear(), vamos sempre criar uma nova.
    fig = plt.Figure(figsize=(5, 4), dpi=100)

    # Define a cor de fundo com base no tema ATUAL
    if customtkinter.get_appearance_mode() == "Dark":
        background_color = "#2b2b2b"
    else:
        background_color = "#ebebeb"

    fig.patch.set_facecolor(background_color)

    ax = fig.add_subplot(111)

    # Define a cor do texto com base no tema ATUAL
    cor_texto_grafico = "white" if customtkinter.get_appearance_mode() == "Dark" else "black"

    wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90,
                                      textprops={'color': cor_texto_grafico})

    for autotext in autotexts:
        autotext.set_color('white')

    ax.axis('equal')
    ax.set_title('')

    # PASSO 3: Criar um NOVO canvas e exibi-lo
    canvas_widget = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas_widget.draw()
    canvas_widget.get_tk_widget().pack(pady=10, padx=10, fill="both", expand=True)

def on_enter(frame):
    #Muda a cor de fundo do frame quando o mouse entra.
    hover_color = "#e5e5e5" if customtkinter.get_appearance_mode() == "Light" else "#3c3c3c"
    frame.configure(fg_color=hover_color)

def on_leave(frame):
    #Restaura a cor de fundo do frame quando o mouse sai.
    default_colors = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
    original_color = default_colors[0] if customtkinter.get_appearance_mode() == "Light" else default_colors[1]
    frame.configure(fg_color=original_color)




# --- 4. ESTRUTURA DA INTERFACE GRÁFICA ---
def criar_interface():
    # Aqui são criados e posicionados todos os widgets (botões, textos, campos, etc.).
    global label_total, label_pago, label_restante, scrollable_frame_pagamentos, entry_data, entry_valor, label_status, frame_grafico
    # Frame principal que contém tudo.
    frame_principal = customtkinter.CTkFrame(master=app)
    frame_principal.pack(pady=20, padx=20, fill="both", expand=True)

    # Botão para alterar o tema
    btn_tema = customtkinter.CTkButton(
        master=frame_principal,
        text="Light/Dark",
        command=trocar_tema,
        width=120
    )
    btn_tema.pack(anchor="ne", padx=10, pady=5)  # 'ne' significa North-East (canto superior direito)

    # Frame superior para organizar o resumo e a área de adição lado a lado.
    frame_superior = customtkinter.CTkFrame(master=frame_principal, fg_color="transparent")
    frame_superior.pack(pady=10, padx=10, fill="x")

    # Seção de Resumo (lado esquerdo).
    frame_resumo = customtkinter.CTkFrame(master=frame_superior)
    frame_resumo.pack(side="left", padx=10, fill="both", expand=True)
    label_titulo_resumo = customtkinter.CTkLabel(master=frame_resumo, text="Resumo da Dívida", font=("Roboto", 20))
    label_titulo_resumo.pack(pady=10)
    label_total = customtkinter.CTkLabel(master=frame_resumo, text="", font=("Roboto", 16))
    label_total.pack(pady=5, padx=10, anchor="w")
    label_pago = customtkinter.CTkLabel(master=frame_resumo, text="", font=("Roboto", 16))
    label_pago.pack(pady=5, padx=10, anchor="w")
    label_restante = customtkinter.CTkLabel(master=frame_resumo, text="", font=("Roboto", 16), text_color="red")
    label_restante.pack(pady=5, padx=10, anchor="w")

    # Seção para Adicionar Novo Pagamento (lado direito).
    frame_novo_pagamento = customtkinter.CTkFrame(master=frame_superior)
    frame_novo_pagamento.pack(side="left", padx=10, fill="both", expand=True)
    label_novo_pagamento = customtkinter.CTkLabel(master=frame_novo_pagamento, text="Adicionar Pagamento")
    label_novo_pagamento.pack(pady=10)
    data_hoje = datetime.now().strftime('%d/%m/%Y')
    entry_data = customtkinter.CTkEntry(master=frame_novo_pagamento, placeholder_text="Data")
    entry_data.insert(0, data_hoje)
    entry_data.pack(pady=5, padx=10)
    entry_valor = customtkinter.CTkEntry(master=frame_novo_pagamento, placeholder_text="Valor Pago")
    entry_valor.pack(pady=5, padx=10)
    entry_valor.bind("<Return>", adicionar_pagamento_event)
    button_adicionar = customtkinter.CTkButton(master=frame_novo_pagamento, text="Adicionar",
                                               command=adicionar_pagamento)
    button_adicionar.pack(pady=10)
    label_status = customtkinter.CTkLabel(master=frame_novo_pagamento, text="", font=("Roboto", 14))
    label_status.pack(pady=5)

    # Seção do Histórico de Pagamentos (parte de baixo).
    label_historico = customtkinter.CTkLabel(master=frame_principal, text="Histórico de Pagamentos",
                                             font=("Roboto", 20))
    label_historico.pack(pady=10)
    scrollable_frame_pagamentos = customtkinter.CTkScrollableFrame(master=frame_principal, height=200)
    scrollable_frame_pagamentos.pack(fill="x", padx=10, pady=10)

    # Botão para exportar os dados
    btn_exportar = customtkinter.CTkButton(master=frame_principal, text="Exportar para CSV", command=exportar_para_csv)
    btn_exportar.pack(pady=10)

# --- 5. INICIALIZAÇÃO DO PROGRAMA ---
# --- 6. INICIALIZAÇÃO DO PROGRAMA ---
if __name__ == "__main__":
    criar_interface()
    popular_dados()
    app.protocol("WM_DELETE_WINDOW", on_closing)

    try:
        # Descobre o caminho do diretório do executável
        if getattr(sys, 'frozen', False):
            # Rodando como .exe
            application_path = os.path.dirname(sys.executable)
            # O sinal deve ser criado na pasta pai (a pasta 'Splash')
            signal_file = os.path.join(application_path, '..', 'signal.tmp')
        else:
            # Rodando como .py no PyCharm
            application_path = os.path.dirname(os.path.abspath(__file__))
            signal_file = os.path.join(application_path, 'signal.tmp')

        # Cria o arquivo de sinal para avisar a splash screen
        with open(signal_file, "w") as f:
            f.write("ready")
    except Exception as e:
        print(f"Erro ao criar arquivo de sinal: {e}")

    app.mainloop()