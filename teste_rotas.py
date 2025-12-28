
import requests
base_url = "http://192.168.0.17:5000"

def login(email, senha):
    url = f"{base_url}/login"
    try:
        # Verifica se os campos estão preenchidos
        if not email or not senha:
            return None, None, None, "Email e senha são obrigatórios"

        response = requests.post(
            url,
            json={'email': email, 'senha': senha},
            timeout=10  # Timeout de 10 segundos
        )

        # Tratamento dos códigos de status
        if response.status_code == 200:
            dados = response.json()
            print(f"Dados retornados: {dados}")  # Adicione este print para depuração
            token = dados.get('access_token')
            papel = dados.get('papel')
            nome = dados.get('nome')  # Captura o nome

            # Verifica se o nome está presente
            if nome is None:
                print("Nome não encontrado na resposta da API.")
                nome = "Nome não disponível"  # Ou qualquer valor padrão que você queira

            return token, papel, nome, None
        elif response.status_code == 401:
            return None, None, None, "Email ou senha incorretos"
        elif response.status_code == 400:
            return None, None, None, "Credenciais inválidas"
        else:
            return None, None, None, f"Erro no servidor: {response.status_code}"

    except requests.exceptions.RequestException as e:
        return None, None, None, f"Erro de conexão: {str(e)}"
    except Exception as e:
        return None, None, None, f"Erro inesperado: {str(e)}"


def cadastrar_usuario(nome, cpf, papel, senha, endereco,status_user, email):
    url = f"{base_url}/cadastro"
    nova_pessoa = {
        'nome': nome,
        'cpf': cpf,

        'papel': papel,  # O papel pode ser 'Admin' ou 'usuario', conforme a API
        'senha': senha,
        'endereco': endereco,
        'status_user': status_user,
        'email': email,
    }

    try:
        response = requests.post(url, json=nova_pessoa)

        if response.status_code == 201:
            return response.json(), None  # Cadastro bem-sucedido
        else:
            return None, response.json().get('msg', 'Erro desconhecido')  # Mensagem de erro da API
    except requests.exceptions.RequestException as e:
        return None, f'Erro de conexão: {str(e)}'


def cadastrar_livro_post(novo_livro):
    url = f'{base_url}/novo_livro'

    response = requests.post(url, json=novo_livro)
    print(response.json())
    if response.status_code == 201:
        dados_post_livro = response.json()

        print(f'Titulo: {dados_post_livro["titulo"]}\n'
              f'Autor: {dados_post_livro["autor"]}\n'
              f'Resumo: {dados_post_livro["resumo"]}\n'
              f'ISBN: {dados_post_livro["ISBN"]}\n'
              f'Leitura {dados_post_livro["leitura"]}\n')
    else:
        print(f'Erro: {response.status_code}')


def listar_livro():
    url = f'{base_url}/livro'
    response = requests.get(url)

    if response.status_code == 200:
        dados_get_livro = response.json()
        print(dados_get_livro)
        return dados_get_livro['lista_livro']
    else:
        print(f'Erro: {response.status_code}')
        return response.json()

def listar_usuario():
    url = f'{base_url}/usuario'
    response = requests.get(url)

    if response.status_code == 200:
        dados_get_usuario = response.json()
        print(dados_get_usuario)
        return dados_get_usuario['lista_usuario']
    else:
        print(f'Erro: {response.status_code}')
        return response.json()



def listar_emprestimos():
    url = f'{base_url}/emprestimo'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_emprestimos = response.json()
        print(dados_get_emprestimos)
        return dados_get_emprestimos['lista_emprestimo']
    else:
        print(f'Erro: {response.status_code}')

def historio_emprestimo_usuario(id):
    url = f'{base_url}/historico_emprestimos/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
        return dados_get_postagem
    else:
        print(f'Erro: {response.status_code}')
        return response.json()

def editar_usuario_rota(id_usuario, novo_post_editar_usuario):
    url = f'{base_url}/editar_usuario/{id_usuario}'

    response = requests.put(url, json=novo_post_editar_usuario)
    if response.status_code == 200:

        dados = response.json()
        print(f'id {dados["id_usuario"]}'
              f'Nome: {dados["nome"]}\n'
              f'Cpf: {dados["cpf"]}\n'
              f'Endereço: {dados["endereco"]}\n'
              f'Email: {dados["email"]}\n'
              f'status_user: {dados["status_user"]}'
              )
        return dados
    else:
        print(f'Erro: {response.status_code}')
        print(f'Erro: {response.json()}')
        return response.json()

def editar_livro_rota(id_livro, novo_post_editar_livro):
    url = f'{base_url}/editar_livro/{id_livro}'

    response = requests.put(url, json=novo_post_editar_livro)
    if response.status_code == 200:

        dados = response.json()
        print(f'id {dados["id_livro"]}'
              f'Titulo: {dados["titulo"]}\n'
              f'Autor: {dados["autor"]}\n'
              f'Resumo: {dados["resumo"]}\n'
              f'ISBN: {dados["ISBN"]}\n')
        return dados
    else:
        print(f'Erro: {response.status_code}')
        print(f'Erro: {response.json()}')
        return response.json()

def editar_status_emprestimo_rota(id):
    url = f'{base_url}/editar_emprestimo/{id}'

    dados_atualizados = {
        'status': 'Devolvido',
    }

    response = requests.put(url, json=dados_atualizados)
    if response.status_code == 200:

        dados = response.json()
        print(f'status {dados}')

        return dados
    else:
        print(f'Erro: {response.status_code}')
        print(f'Erro: {response.json()}')
        return response.json()

def get_livro(id):
    url = f'{base_url}/get_livro/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
        return dados_get_postagem
    else:
        print(f'Erro: {response.status_code}')
        return response.json()

def get_usuario(id):
    url = f'{base_url}/get_usuario/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
        return dados_get_postagem
    else:
        print(f'Erro: {response.status_code}')
        return response.json()

def cadastrar_emprestimo_post(novo_emprestimo):
    url = f'{base_url}/novo_emprestimo'
    response = requests.post(url, json=novo_emprestimo)
    if response.status_code == 201:
        dados_post_emprestimo = response.json()

        print(f'Data de Empréstimo: {dados_post_emprestimo}')
        return dados_post_emprestimo
    else:
        print(f'Erro: {response.json()}')
        return {'error': response.json()}



