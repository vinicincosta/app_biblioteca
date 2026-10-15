# App Biblioteca

Aplicativo em Python ([Flet](https://flet.dev)) para os leitores da biblioteca digital: consultar o acervo, pegar livros emprestados e acompanhar devoluções. Consome a [API Biblioteca](https://github.com/vinicincosta/API_biblioteca), que também atende a [interface web](https://github.com/vinicincosta/Biblioteca_Web).

## Funcionalidades

- Login por e-mail e senha e cadastro de novos usuários
- Catálogo em cards com status do livro: **Disponível** ou **Emprestado**
- Busca de livro por ID e tela de detalhes (título, resumo, autor, ISBN)
- Novo empréstimo com confirmação; o prazo máximo de devolução é de 20 dias
- Navegação inferior: Livros · Empréstimos · Ativos

### Implementadas, em ajuste

Estas telas existem no código, mas dependem de o token de sessão ser gravado após o login (veja os próximos passos):

- **Meus livros**: empréstimos ativos do usuário, com devolução pelo menu do card
- **Leitor integrado**: texto paginado, ajuste de tamanho da fonte, modo noturno e troca de página por botões ou gesto de arrastar
- **Histórico** de empréstimos do usuário
- Selo **Atrasado** no catálogo: está no código, mas a API marca como `Devolvido` os empréstimos vencidos antes de responder, então ele não chega a aparecer

## Tecnologias

- Python 3
- Flet 0.27 (versão fixada no `requirements.txt`)
- Requests (comunicação com a API)

## Estrutura

```
app_biblioteca/
├── app.py             # interface, navegação e telas
├── teste_rotas.py     # funções de acesso à API (login, livros, usuários, empréstimos) e base_url
├── rotas/rotas.py     # versão anterior das funções de acesso, com IPs fixos
├── requirements.txt
└── *.jpg / *.png      # ilustrações usadas nas telas
```

## Como rodar

1. Suba a [API Biblioteca](https://github.com/vinicincosta/API_biblioteca).

2. Instale as dependências do app:

```bash
git clone https://github.com/vinicincosta/app_biblioteca.git
cd app_biblioteca

python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Aponte o app para a API editando `base_url` em `teste_rotas.py`:

```python
base_url = "http://192.168.0.177:5000"   # troque pelo endereço da sua API
```

   Use `http://localhost:5000` se a API roda na mesma máquina, ou o IP da máquina na rede local para testar em um celular.

4. Inicie o app:

```bash
python app.py
```

Por padrão ele abre em uma janela de 375×667 (proporção de celular). Para abrir no navegador, por exemplo para testar pelo celular na mesma rede Wi-Fi, troque a última linha de `app.py` por:

```python
ft.app(
    target=main,
    host="0.0.0.0",
    port=8550,
    view=ft.AppView.WEB_BROWSER,
)
```



## Projetos relacionados

- [API_biblioteca](https://github.com/vinicincosta/API_biblioteca): backend REST em Flask
- [Biblioteca_Web](https://github.com/vinicincosta/Biblioteca_Web): interface web
