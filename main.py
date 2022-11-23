# importando a biblioteca utilizada
from tkinter import*
from tkinter import Tk, StringVar, ttk, messagebox

#importando o pillow, biblioteca para manipulação de imagens
from PIL import Image, ImageTk

import csv

#Cores que serão utilizadas no projeto

cor_0 = "#f0f3f5" # Preta
cor_1 = "#feffff" #Branca
cor_2 = "#3fb5a3" #Verde
cor_3 = "#fc766d" #Vermelha
cor_4 = "#403d3d" #Letra
cor_5 = "#4a88e8" #Azul

#Criando a Janela

janela = Tk()
janela.title("")
janela.geometry('390x350')
janela.configure(background=cor_1)
janela.resizable(width=False, height=False)

#Criando os Frames

#criando o frame onde ficará a parte do cabeçalho/titulo
frame_logo = Frame(janela, width=400, height=60, bg=cor_1, relief="flat")
frame_logo.grid(row=0, column=0, pady=1, padx=0, sticky=NSEW)
#Criando o frame do corpo da tela
frame_corpo = Frame(janela,width=400, height=400, bg=cor_1, relief="flat")
frame_corpo.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

#Configurando Frame Logo ajustando a imagem

imagem = Image.open('block.png')
imagem = imagem.resize((44,44))
imagem = ImageTk.PhotoImage(imagem)

#Criando as Labels dos Frames
#Frame Logo
#Label da imagem
l_imagem = Label(frame_logo, height=45, image=imagem, bg=cor_1)
l_imagem.place(x=20, y=5)
#Label do Titulo
l_logo = Label(frame_logo, text='Bloqueador de sites', height=1, anchor=NE, font=('Ivy 25'), bg=cor_1, fg=cor_4)
l_logo.place(x=70, y=10)
#Label da linha abaixo do titulo
l_linha = Label(frame_logo, text='', width= 445, height=1, anchor=NW, font=('Ivy 1'), bg=cor_2)
l_linha.place(x=0, y=57)

#Criando as funções
global iniciar
global websites

iniciar = BooleanVar()



#Função que permite retornar na listbox os sites que adicionamos
def ver_site():
    listbox.delete(0, END)
    #acessando as informações do arquivo csv
    with open('sites.csv') as file:
        ler_csv = csv.reader(file)
        for row in ler_csv:
            listbox.insert(END, row)


#Função que salva os sites colocados na lista
def salvar_site(i):
    #acessando arquivo csv
    with open('sites.csv', 'a+', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([i])
        messagebox.showinfo('Aviso!', 'O site foi adicionado')

    ver_site()

#Função para remover sites da lista
def deletar_site(i):

    def adicionar(i):
        # acessando arquivo csv
        with open('sites.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(i)
            messagebox.showinfo('Aviso!', 'O site foi removido')

        ver_site()

    nova_lista = []
    with open('sites.csv', 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            nova_lista.append(row)
            for campo in row:
                if campo==i:
                    print(campo)
                    nova_lista.remove(row)

    adicionar(nova_lista)

#Função adicionar site
def adicionar():
    site = e_texto.get()
    if site == '':
        pass
    else:
        listbox.insert(END, site)
        e_texto.delete(0, END)

        salvar_site(site)
#Função Remover sites selecionados da lista
def remover_site():
    site = listbox.get(ACTIVE)
    sites = []
    for i in site:
        sites.append(i)
    deletar_site(sites[0])

def desbloquear_site():
    iniciar.set(False)
    messagebox.showinfo('Site', "Os sites na lista foram Desbloqueados")
    bloqueador_site()

def bloquear_site():
    iniciar.set(True)
    messagebox.showinfo('Site', "Os sites na lista foram Bloqueados")
    bloqueador_site()


#Função bloqueador site
def bloqueador_site():

    #caminho do arquivo host do windows
    local_do_host = r'C:\Windows\System32\drivers\etc\hosts'
    redirecionar = '127.0.0.1'

    websites = []

    #acessar o arquivo csv
    with open('sites.csv') as file:
        ler_csv = csv.reader(file)
        for row in ler_csv:
            websites.append(row[0])
#condição para bloquear
    if iniciar.get() == True:
        with open(local_do_host, 'r+') as arquivo:
            conteudo=arquivo.read()
            for site in websites:
                if site in conteudo:
                    pass
                else:
                    arquivo.write(redirecionar+" "+site+"\n")
# condição para desbloquear
    else:
        with open(local_do_host, 'r+') as arquivo:
            conteudo=arquivo.readlines()
            arquivo.seek(0)

            for line in conteudo:
                if not any(site in line for site in websites):
                    arquivo.write(line)
            arquivo.truncate()



#Frame Corpo
#Label do texto
l_texto = Label(frame_corpo, text='Digite o(s) site(s) que deseja bloquear no campo abaixo *', height=1, anchor=NE, font=('Ivy 8 bold'), bg=cor_1, fg=cor_4)
l_texto .place(x=20, y=10)

#Entry(caixa) do texto
e_texto = Entry(frame_corpo, width=30, justify='left', font=('15'), relief=SOLID)
e_texto.place(x=23, y=50)

#Criando os botões
#Botão caixa de Adicionar
b_adicionar = Button(frame_corpo, command=adicionar, text='Adicionar', width=10, height=1, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_5, fg=cor_1)
b_adicionar.place(x=300, y=50)
#Botão caixa de Remover
b_remover = Button(frame_corpo, command=remover_site, text='Remover', width=10, height=1, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_5, fg=cor_1)
b_remover.place(x=300, y=100)
#Botão caixa de Desbloquear
b_desbloquear = Button(frame_corpo, command=desbloquear_site, text='Desbloquear', width=10, height=1, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_2, fg=cor_1)
b_desbloquear.place(x=300, y=150)
#Botão caixa de Bloquear
b_bloquear = Button(frame_corpo, command=bloquear_site, text='Bloquear', width=10, height=1, font=('Ivy 8 bold'), relief=RAISED, overrelief=RIDGE, bg=cor_3, fg=cor_1)
b_bloquear.place(x=300, y=200)

#Criando a área da lista onde ficará a relação dos sites bloqueados
listbox = Listbox(frame_corpo, font=('Arial 9 bold'), width=38, height=10)
listbox.place(x=23, y=100)


#Inicializando funções
ver_site()

#Setando para abrir a janela
janela.mainloop()


