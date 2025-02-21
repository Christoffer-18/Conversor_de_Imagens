from tkinter.filedialog import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from pacotes import back as bk
import tkinter as tk
from tkinter import messagebox

def buscar_pasta(caminho):
    '''
    Busca a pasta selecionada pelo usuário.
    '''
    pasta = askdirectory(title="Selecione uma pasta:")
    if pasta:
        caminho.set(pasta) # atualiza o texto do Entry com o caminho da pasta
    
def atencao(mensagem):
    '''
    Mostra uma tela de mensagem que bloqueia a interação com a tela principal.
    '''
    root = tk.Toplevel()
    root.grab_set() # Bloqueia o interação com a janela principal
    root.geometry("450x200")
    root.title("Aviso")

    label = ttk.Label(root, text=mensagem, font=("Arial", 14,"bold"), background="#2b3e50", foreground="white")
    label.pack(pady=25)

    ok_button = ttk.Button(root, text="OK",  bootstyle="light", command=root.destroy)
    ok_button.pack(pady=10)
    root.mainloop()

def mensagem(texto):
    '''
    Abre uma tela e mostra uma mensagem, não bloqueia a interação com a tela principal, 
    por isso recomendo usar apenas quando não tiver uma tela principal.
    '''
    root = ttk.Window("mensagem", themename="superhero")
    root.geometry("450x200")
    
    label = ttk.Label(root, text=texto, font=("Arial", 14, "bold"), background="#2b3e50", foreground="white")
    label.pack(padx=25)

    ok_button = ttk.Button(root, text="OK", bootstyle="light", command=root.destroy)
    ok_button.pack(pady=10)
    root.mainloop()

def my_label(frame, texto,variavel,side=LEFT):
    '''
    Cria uma label.
    '''
    ttk.Label(frame, text=texto).pack(side=side, padx=5)
    ttk.Entry(frame, textvariable=variavel).pack(side=side, fill="x",expand=True, padx=5)

def criando_toggle(root, frame, texto, bootstyle, font, callback, side=LEFT):
    '''
    Criando um toggle switch, os toggle são para verificar se tem o pixel max e min para as imagens.
    '''
    # Criando o texto
    label = ttk.Label(frame, text=texto, font=font)
    label.pack(side=side, padx=5, pady=5)

    # Criando umaa váriavel que controla o checkbutton
    var = tk.BooleanVar() # o que tranforma a váriavel em True ou False
    button = ttk.Checkbutton(frame, bootstyle=bootstyle, variable=var)
    button.pack(side=side, padx=5, pady=5)

    #Criando o label "invisivel" que será atualizado
    invisivel = ttk.Label(root, text="", font=font)
    invisivel.pack(padx=5, pady=5)

    # Usando o método trace para monitorar a mudança no valor da variável
    var.trace_add("write", lambda *args: update(var, invisivel, callback))

def update(var, frame, callback):
    '''
    Verifica se o toggle foi acionado e guardar o valor digitado.
    '''
    for widget in frame.winfo_children():
        widget.destroy()

    if var.get():
        # Variavei para altura e larugura 
        altura_var = ttk.StringVar(value=0)
        largura_var = ttk.StringVar(value=0)

        # Criando frames
        altura_frame = ttk.Frame(frame)
        altura_frame.pack(side=LEFT, fill="x", pady=5)

        largura_frame = ttk.Frame(frame)
        largura_frame.pack(side=LEFT, fill="x", pady=5)

        #Chamando função
        my_label(altura_frame, "Altura: ", altura_var, side=TOP)
        my_label(largura_frame, "Largura: ", largura_var, side=TOP)

        def mudanca_valor(*args):
            try:
                altura = int(altura_var.get()) if altura_var.get() else 0
                largura = int(largura_var.get()) if largura_var.get() else 0
                callback(altura, largura)
            except ValueError:
                pass
        
        altura_var.trace_add("write", mudanca_valor)
        largura_var.trace_add("write", mudanca_valor)
        
def click_button(ext, var):
    var.set(ext)

def fechar(root): 
    '''
    Verificador se a pessoa realmete deseja finalizar o programa.
    '''
    if messagebox.askokcancel("Sair", "Você tem certeza que deseja sair?"):
        root.destroy()
        return False

def entrada():
    '''
    Cria a janela principal e todos os seus componentes visuais.
    '''
    # Criando a janela
    root = ttk.Window("Conversor",themename="superhero")
    root.geometry("550x500") # tamanho

    # Variáveis 
    caminho_var = ttk.StringVar()
    altura_max = tk.IntVar(value=0)
    altura_min = tk.IntVar(value=0)
    largura_max = tk.IntVar(value=0)
    largura_min = tk.IntVar(value=0)
    extensoes = bk.extensoes_global
    cores = list(root.style.colors)
    fonte_padrao = ("Arial", 12, "normal")
    formato_var = ttk.StringVar()
    resultado = dict()

    # Pegando valor da altura e largura
    def salvar_max(altura, largura):
        if altura and largura:
            altura_max.set(altura)
            largura_max.set(largura)

    def salvar_min(altura, largura):
        if altura and largura:
            altura_min.set(altura)
            largura_min.set(largura)

    # Título 
    label = ttk.Label(root, text="Conversor em massa de imagens.")
    label.pack(pady=30)
    label.config(font=("Arial",18,"bold"))

    # Caminho do diretóro
    caminho = ttk.Frame(root)
    caminho.pack(pady=18,padx=10,fill="x")
    my_label(caminho, "Caminho", caminho_var)

    # botão para buscar o diretório
    b1 = ttk.Button(caminho, text="...", width=2, bootstyle="primary", command=lambda: buscar_pasta(caminho_var))
    b1.pack(side=LEFT, padx=5)
    
    # Criando framde do butão deslizante
    toggle = ttk.Frame(root)
    toggle.pack(padx=5, pady=5)

    # Criando o toggle
    deslizante = "succes-round-toggle"
    criando_toggle(root, toggle, "Tamanho máximo px : ", deslizante, fonte_padrao, salvar_max)
    criando_toggle(root, toggle, "Tamanho mínimox px : ", deslizante, fonte_padrao, salvar_min)

    # Gerando botão de extensão
    titulo_extensao = ttk.Label(root, text="Vai converter para: ", font=fonte_padrao)
    titulo_extensao.pack(side=LEFT, pady=20)

    # Frame para os botões
    frama_extensoes = ttk.Frame(root)
    frama_extensoes.pack(side=LEFT, padx=10)

    # Botões da extensões
    for c in range(0,len(extensoes)):
        cor = cores[c % len(cores)]
        b_variavel1 = ttk.Button(frama_extensoes, text=extensoes[c], width=7, bootstyle=cor, command= lambda ext=extensoes[c]: click_button(ext, formato_var))
        b_variavel1.pack(side=LEFT, padx=5, pady=5)

    # Gerando botão ok
    def confirmar():
        nonlocal resultado
        #Captura os dados da interface
        resultado = {
            "caminho": caminho_var.get(),
            "altura_max": altura_max.get(),
            "largura_max": largura_max.get(),
            "altura_min": altura_min.get(), 
            "largura_min": largura_min.get(),
            "formato": formato_var.get(),
        }
        valores = list(resultado.values())
        validado = bk.verificador(valores)
        if validado:
            root.destroy()
        
    #b_ok = ttk.Button(root, text="OK", width=4, bootstyle="light", command=lambda: bk.listar_imagens(caminho_var.get()))
    b_ok = ttk.Button(root, text="OK", width=4, bootstyle="light", command=confirmar)
    b_ok.pack(side="bottom", anchor="e", padx=10,pady=10)

    # Associar o evento de fechar (o botão "X")
    root.protocol("WM_DELETE_WINDOW", lambda: fechar(root))

    root.mainloop()

    return resultado
