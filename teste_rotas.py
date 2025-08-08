
import requests


def historio_emprestimo_usuario(id):
    url = f'http://10.135.235.29:5000/historico_emprestimos/{id}'
    response = requests.get(url)
    if response.status_code == 200:
        dados_get_postagem = response.json()
        print(dados_get_postagem)
        return dados_get_postagem
    else:
        print(f'Erro: {response.status_code}')
        return response.json()

historio_emprestimo_usuario(2)
