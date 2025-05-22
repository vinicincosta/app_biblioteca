import requests


def listar_livro():
    url = f'http://10.135.232.9:5000/livro'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
    #     print(f'Titulo: {dados_get_postagem["titulo"]}\n'
    #           f'Autor: {dados_get_postagem["autor"]}\n'
    #           f'Resumo: {dados_get_postagem["Resumo"]}\n'
    #           f'ISBN: {dados_get_postagem["ISbn"]}\n')
    else:
        print(f'Erro: {response.status_code}')
# listar_livro()


def listar_usuario():
    url = f'http://10.135.232.9:5000/usuario'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
    else:
        print(f'Erro: {response.status_code}')

# listar_usuario()


def get_usuario(id):
    url = f'http://10.135.232.9:5000/get_usuario/{8}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
    else:
        print(f'Erro: {response.status_code}')
get_usuario(8)


def get_livro(id):
    url = f'http://10.135.232.9:5000/get_livro/{7}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
    else:
        print(f'Erro: {response.status_code}')
get_livro(7)

