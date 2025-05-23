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
        print('hhhh3',dados_get_postagem)
    else:
        print(f'Erro: {response.status_code}')

# listar_usuario()


def listar_emprestimos():
    url = f'http://10.135.232.9:5000/emprestimo'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_emprestimos = response.json()
        print('hhhh3',dados_get_emprestimos)
    else:
        print(f'Erro: {response.status_code}')
listar_emprestimos()

def get_usuario(id):
    url = f'http://10.135.232.9:5000/get_usuario/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
    else:
        print(f'Erro: {response.status_code}')
# get_usuario(17)


def get_livro(id):
    url = f'http://10.135.232.9:5000/get_livro/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
    else:
        print(f'Erro: {response.status_code}')
# get_livro(12)

def cadastrar_livro_post(novo_livro):
    url = f'http://10.135.232.9:5000/novo_livro'

    response = requests.post(url, json=novo_livro)
    print(response.json())
    if response.status_code == 201:
        dados_post_livro = response.json()

        print(f'Titulo: {dados_post_livro["titulo"]}\n'
              f'Autor: {dados_post_livro["autor"]}\n'
              f'Resumo: {dados_post_livro["resumo"]}\n'
              f'ISBN: {dados_post_livro["ISBN"]}\n')
    else:
        print(f'Erro: {response.status_code}')


def cadastrar_emprestimo_post(novo_emprestimo):
    url = f'http://10.135.232.9:5000/novo_emprestimo'
    response = requests.post(url, json=novo_emprestimo)
    if response.status_code == 201:
        dados_post_emprestimo = response.json()

        print(f'Titulo: {dados_post_emprestimo["data_de_devolucao"]}\n'
              f'Autor: {dados_post_emprestimo["data_de_emprestimo"]}\n'
              f'Resumo: {dados_post_emprestimo["livro_emprestado_id"]}\n'
              f'ISBN: {dados_post_emprestimo["usuario_emprestado_id"]}')
    else:
        print(f'Erro: {response.status_code}')


def editar_usuario(novo_post_editar_usuario):
    url = f'http://10.135.232.9:5000/editar_usuario/{id}'

    antes = requests.get(url)
    response = requests.put(url, json=novo_post_editar_usuario)
    if response.status_code == 201:
        if antes.status_code == 201:
            dados_antes = antes.json()
            print(f'Nome antigo: {dados_antes["nome"]}\n'
                  f'Cpf antigo: {dados_antes["cpf"]}\n'
                  f'Endereço: {dados_antes["endereco"]}\n')
        else:
            print(f'Erro: {response.status_code}') # Ver se o antes deu certo
        dados = response.json()
        print(f'Nome: {dados["nome"]}\n'
              f'Cpf: {dados["endereco"]}\n'
              f'Endereço: {dados['endereco']}')
    else:
        print(f'Erro: {response.status_code}')
