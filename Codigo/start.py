'''
Start onde começa o programa e onde faz pequenas verificações.
'''
from pacotes import back as bk 
from pacotes import front as ft 

dados = ft.entrada()
if len(dados) != 0:
    dados_lista = list(dados.values())
    caminho = dados_lista[0]
    extensao = dados_lista[5]
    tamanho = dados_lista[1:5]

    lista_alterar = bk.listar_imagens(caminho, extensao, tamanho)
    if not lista_alterar == False: 
        # Verificando se tem aluma imagem para alterar extensão
        if len(lista_alterar) > 0:
            bk.conversor_img(lista_alterar, extensao, caminho)
        
        # Verificando se tem aluma imagem para alterar pixel
        if sum(tamanho) != 0:
            alterar_px = bk.listar_px(caminho, tamanho)
            bk.conversor_px(alterar_px,tamanho,caminho)
        ft.mensagem("Programa finalizado\nImagens alteradas com sucesso!!")
    else:
        ft.mensagem("Programa finalizado!\nNão teve imagens para alterar")
