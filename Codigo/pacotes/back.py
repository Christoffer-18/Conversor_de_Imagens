import os
from PIL import Image
from pacotes import front as ft
import datetime as data

# Váriaves globais
extensoes_global = ('.jpg', '.jpeg', '.png', '.webp')

def verificador(lista):
    '''Verifica se o usuário colocou um caminho existente, se o tamanho do pixel está dentro do limite e se ele selecionou
    a extensão da imagem.'''
    #Verificando se o caminho existe 
    if not os.path.isdir(lista[0]):
        ft.atencao("Caminho não encontrado!")
        return False
    else:
        tem_imagens = verificador_imagens(lista[0])
        if len(tem_imagens) == 0:
            ft.atencao("Não tem imagens na pasta!")
            return False

    # Verificando se o pixel está correto
    valor_invalido = False

    for valor in lista[1:5]:
        if valor !=0 and (valor >1500 or valor <50):
            valor_invalido = True
            break # Se achar um valor incorreto ela sai da repetição

    if valor_invalido:
        ft.atencao("Os valores digitdos não são válidos\nPixel max: 1500 \nPixel min: 50")
        return False

    # Verifica se selecionou o extensão 
    if lista[5] == '':
        ft.atencao("Selecione uma extensão!")
        return False

    return True

def verificador_imagens(caminho):
    ''' 
    Verifica todos os itens do diretório e retorna apenas os que são imagens.
    '''
    ext = extensoes_global
    imagens_alterar = list()
    
    # Lista todos os arquivos no diretório
    arquivos = os.listdir(caminho)
    #filtra apenas arquivos com extensões de imagem
    imagens = [ imagem for imagem in arquivos if imagem.lower().endswith(ext)]

    return imagens

def listar_imagens(diretorio, ext, valores):
    '''
    Lista todas as imagens dentro de um diretorio e verifica se tem alguma imagem com a extenão diferente do qual foi passada na "ext", 
    se não tiver ele e nem um valor de pixel para alterar ele retorna falso.
    '''
    try:
        todas_imagens = verificador_imagens(diretorio)
        para_alterar_ext = [arquivo for arquivo in todas_imagens if not arquivo.lower().endswith(ext)]
        para_alterar_px = list()
        
        # Verificando se tem arquivo para alterar
        if len (para_alterar_ext) == 0 and sum(valores) == 0:
            logs(diretorio, "Não tem arquivios para alterar.")
            return False
        else:
            return para_alterar_ext
    except Exception as e :
        logs(diretorio, e)

def logs(diretorio,mensagem, pasta="L", nome_arquivo=""):
    '''
    Função para abrir um txt e escrever o erro ou modificação que aconteceu.
    Pasta = se vai escrver a mensagem de erro na pasta (L)og ou vai apenas fazer um txt falando quais arquivos alterou no (D)iretório.
    Diretório = local onde está o arquivo. 
    Mensagem = O que vai ser escrito no txt, se for D pode passar uma lista com todas as mensagen de modificações.
    Nome_arquivo = se for D, tem que colocar o nome do arquivo txt.
    '''
    data_atual = data.datetime.now()
    data_formatada = data_atual.strftime("%d/%m/%Y %H:%M")
    separacao = "--" * 20
    if pasta == "L":
        log = diretorio + "/Logs"
        if not os.path.exists(log):
            os.makedirs(log)
        with open(os.path.join(log, "Logs.txt"), "a", encoding="utf-8") as file:
            file.write(f"Data do log: {data_formatada}\n")
            file.write(f"{mensagem} \n")
            file.write(f"{separacao} \n")
    else:
        with open(os.path.join(diretorio, nome_arquivo), "a", encoding="utf-8") as mod:
            mod.write(f"Data da mudança: {data_formatada}\n")
            for item in mensagem:
                mod.write(f"{item} \n")
            mod.write(f"{separacao} \n")

def conversor_img(alterar, ext, diretorio):
    '''
    Convertento a imagem para a extensão desejada.
    '''
    alterados = list()
    for img in alterar:
        try:
            caminho_imagem = diretorio+'/'+img
            imagem = Image.open(caminho_imagem)

            # Transformando em RBG, para conseguir converter para qualquer formato
            imagem_rgb = imagem.convert("RGB")
            
            # Nome sem extensão
            nome_dividido = os.path.splitext(img)
            if len(nome_dividido) == 2:
                nome_base = f"{nome_dividido[0]}{ext}"
                caminho_salvar = os.path.join(diretorio, nome_base)
                imagem_rgb.save(caminho_salvar)

                # Adicinando os nomes  modificados
                nome_alterados = f"Modifiquei o arquivo {img} para -> {nome_base}"
                alterados.append(nome_alterados)
                os.remove(caminho_imagem)
            else:
                logs(diretorio,"O nome do arquivo está no formato errado, confira e não use '.' no meio do nome")
        except Exception as e:
            # Em caso de qualquer exceção, joga o erro
            logs(diretorio, f"Erro ao processar o arquivo {img}: {e}")

    # Escrevendo o nome 
    logs(diretorio, alterados, "D", "Extensao_modificada.txt")

def listar_px(diretorio, valores):
    '''
    Lista todas as imagens que vão ser alteradas.
    '''
    todas_imagens = verificador_imagens(diretorio)
    para_alterar_px = list()

    for imagem in todas_imagens:
        try:
            caminho_imagem = diretorio+'/'+imagem
            imagem_ver = Image.open(caminho_imagem)
            largura, altura = imagem_ver.size
            if((altura > valores[0] and valores[0] !=0) or altura < valores[2]) or ((largura > valores[1] and valores[1] !=0) or largura < valores[3]) :
                para_alterar_px.append(imagem)
        except Exception as e :
            logs(diretorio, f"Erro ao processar o arquivo {imagem}: {e}")

    return para_alterar_px

def conversor_px(alterar, valores, diretorio):
    '''
    Altera os pixels da imagem e sobreescre a original.
    '''
    alterados = list()
    for img in alterar:
        try:
            caminho_imagem = os.path.join(diretorio, img)
            imagem_ver = Image.open(caminho_imagem)
            largura, altura = imagem_ver.size
            modificado = False
            nova_altura, nova_largura = altura, largura

            # Verifica o maximo 
            if (valores[0] + valores[1]) != 0:
                if altura > valores[0]:
                    nova_altura = valores[0]
                    modificado = True
                
                if largura > valores[1]:
                    nova_largura = valores[1]
                    modificado = True
                
                if modificado:
                    imagem_mod = imagem_ver.resize((nova_largura,nova_altura), Image.LANCZOS)
                    imagem_mod.save(caminho_imagem)
                    alterados.append(f"Modifiquei {img} para {nova_largura}x{nova_altura}.")

            # Verifica o minimo
            if (valores[2] + valores[3]) != 0:
                if altura < valores[2]:
                    nova_altura = valores[2]
                    modificado = True
      
                if largura < valores[3]:
                    nova_largura = valores[3]
                    modificado = True

                if modificado:
                    imagem_mod = imagem_ver.resize((nova_largura,nova_altura), Image.LANCZOS)
                    imagem_mod.save(caminho_imagem)
                    alterados.append(f"Modifiquei {img} para {nova_largura}x{nova_altura}.")

        except Exception as e:
            logs(diretorio, f"Erro ao procesar o arquivo {img}: {e}")
    if alterados:
        logs(diretorio, alterados, "D", "Pixel_modificados.txt")
