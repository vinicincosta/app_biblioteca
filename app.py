import flet as ft
from flet import AppBar, Text, View, Container, Column
from flet.core.colors import Colors
import requests
from flet.core.elevated_button import ElevatedButton

from rotas import *


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    page.navigation_bar = ft.NavigationBar(
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Regras"),
            ft.NavigationBarDestination(icon=ft.Icons.REPORT, label="Simulação"),
            ft.NavigationBarDestination(
                icon=ft.Icons.ACCOUNT_BOX,
                selected_icon=ft.Icons.BOOKMARK,
                label="Explorer",

            ),

        ],
        bgcolor=Colors.BLUE_200,
    )

    pagelet = ft.Pagelet(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.BOOK, label="Livros", ),
                ft.NavigationBarDestination(icon=ft.Icons.ACCOUNT_BOX, label="Usuários"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.EMAIL_SHARP,
                    selected_icon=ft.Icons.EMAIL_SHARP,
                    label="Empréstimos",

                ),

            ],
            bgcolor=Colors.BLUE_300,
            on_change=lambda e: page.go(
                ["/", "/segunda", "/terceira"][
                    e.control.selected_index])
        ), content=ft.Container(),
        bgcolor=Colors.BLUE_200,
        height=500, expand=True, )

    # Funções
    def cadastrar_livro_post(novo_livro):
        url = f'http://10.135.232.9:5000/novo_livro'

        response = requests.post(url, json=novo_livro)
        if response.status_code == 201:
            dados_postagem = response.json()

            print(f'Titulo: {dados_postagem["titulo"]}\n'
                  f'Autor: {dados_postagem["autor"]}\n'
                  f'Resumo: {dados_postagem["resumo"]}\n'
                  f'ISBN: {dados_postagem["ISBN"]}\n')
        else:
            print(f'Erro: {response.status_code}')

    def cadastrar_usuario_post(novo_usuario):
        url = "http://10.135.232.9:5000/novo_usuario"

        response = requests.post(url, json=novo_usuario)
        if response.status_code == 201:
            dados_postagem = response.json()

            print(f'Nome: {dados_postagem["nome"]}\n'
                  f'Cpf: {dados_postagem["cpf"]}\n'
                  f'Endereço: {dados_postagem["endereco"]}')
        else:
            print(f'Erro: {response.status_code}')

    def listar_livro():
        url = f'http://10.135.232.9:5000/livro'
        response = requests.get(url)
        if response.status_code == 200:
            dados_get_postagem = response.json()
            print(f'Titulo: {dados_get_postagem["titulo"]}\n'
                  f'Autor: {dados_get_postagem["autor"]}\n'
                  f'Resumo: {dados_get_postagem["Resumo"]}\n'
                  f'ISBN: {dados_get_postagem["ISbn"]}\n')
        else:
            print(f'Erro: {response.status_code}')

    def listar_usuario():
        url = f'http://10.135.232.9:5000/usuario'
        response = requests.get(url)
        if response.status_code == 200:
            dados_get_postagem = response.json()
            print(dados_get_postagem)
        else:
            print(f'Erro: {response.status_code}')

    # //////////////////////////////////////////////////////////////////////////////////////////////

    # def add_titulo_lista(e):
    #     lv_livros.controls.clear()
    #     lv_resultado = select(Livro)
    #     resul_livros = db_session.execute(lv_resultado).scalars().all()
    #
    #     for livro in resul_livros:
    #         lv_livros.controls.append(
    #             ft.ListTile(
    #                 leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
    #                 title=ft.Text(f'Título - {livro.titulo}', color=Colors.BLACK),
    #                 subtitle=ft.Text(f'Categoria - {livro.categoria}',color=Colors.BLACK),
    #                 trailing=ft.PopupMenuButton(
    #                     icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
    #                     items=[
    #                         ft.PopupMenuItem(text=f'Detalhes',
    #                                          on_click=lambda _, l=livro: exibir_detalhes(l)),
    #
    #                     ],
    #                 )
    #             )
    #         )
    #     page.update()

    # def exibir_detalhes(livro):
    #     txt_resultado.value = (f'Titulo: {livro.titulo}\n'
    #                            f'Categoria: {livro.categoria}\n'
    #                            f'Autor: {livro.autor}\n'
    #                            f'Descrição: {livro.descricao}')
    #     page.go('/terceira')

    def salvar_livros(e):
        if (input_titulo.value == '' or input_autor.value == ''
                or input_ISBN.value == '' or input_resumo.value == ''):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()

        else:
            novo_livro = {
                'titulo': input_titulo.value,
                'resumo': input_resumo.value,
                'autor': input_autor.value,
                'ISBN': input_ISBN.value,
            }
            cadastrar_livro_post(novo_livro)
            input_ISBN.value = ''
            input_resumo.value = ''
            input_autor.value = ''
            input_titulo.value = ''
            page.overlay.append(msg_sucesso)  # overlay sob escreve a página
            msg_sucesso.open = True
            page.update()

    def salvar_usuarios(e):
        if (input_nome.value == '' or input_cpf.value == ''
                or input_endereco.value == ''):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_usuario = {
                'nome': input_nome.value,
                'cpf': input_cpf.value,
                'endereco': input_endereco.value,

            }
            cadastrar_usuario_post(novo_usuario)
            input_ISBN.value = ''
            input_resumo.value = ''
            input_autor.value = ''
            input_titulo.value = ''
            page.overlay.append(msg_sucesso)  # overlay sob escreve a página
            msg_sucesso.open = True
            page.update()

    def gerencia_rotas(e):
        page.views.clear()
        page.views.append(

            View(
                "/",
                [
                    AppBar(title=Text("Livros", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT, center_title=True),

                    Container(
                        Column(
                            [
                                imagem,
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=10)),

                    Container(
                        Column(
                            [
                                ft.Button(
                                    text="Cadastrar Livro",
                                    bgcolor=Colors.BLUE_ACCENT,
                                    color=Colors.BLACK,
                                    on_click=lambda _: page.go('/cadastrar_livro'),

                                ),
                            ],

                        ),
                    alignment = ft.alignment.center,
                    padding = ft.padding.only(top=5)
                    ),


                    pagelet,
                ],
                bgcolor=Colors.BLUE_200,

            )
        )

        if page.route == '/cadastrar_livro':
            page.views.append(
                View(
                    "/cadastrar_livro",
                    [
                        AppBar(title=Text("Cadastro Livros", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        input_titulo,
                        input_autor,
                        input_resumo,
                        input_ISBN,

                        ft.Button(
                            text="Salvar",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: salvar_livros(e),
                        ),

                        ft.Button(
                            text="Exibir livros",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,

                        )
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/segunda":
            page.views.append(
                View(
                    "/segunda",
                    [
                        AppBar(title=Text("Usuários", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        Container(
                            Column(
                                [
                                    imagem_2,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(top=10)),

                        Container(
                            Column(
                                [
                                    ft.Button(
                                        text="Cadastrar Usuários",
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/cadastar_usuarios'),

                                    ),
                                ],

                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=5)
                        ),
                        pagelet
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/cadastar_usuarios":
            page.views.append(
                View(
                    "/cadastar_usuarios",
                    [
                        AppBar(title=Text("Cadastro", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        input_nome,
                        input_cpf,
                        input_endereco,

                        ft.Button(
                            text="Salvar",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: salvar_usuarios(e),
                        )

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/terceira":
            page.views.append(
                View(
                    "/terceira",
                    [
                        AppBar(title=Text("Empréstimos", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),

                        Container(
                            Column(
                                [
                                    imagem_3,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=10)),

                        pagelet

                    ],
                    bgcolor=Colors.BLUE_200,

                )
            )
        if page.route == "/cadastrar_emprestimos":
            page.views.append(
                View(
                    "/cadastrar_emprestimos",
                    [
                        AppBar(title=Text("Cadastro Empéstimos", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),

                    ]
                )
            )
        page.update()

    # Componentes
    msg_sucesso = ft.SnackBar(

        content=ft.Text("campos salvo com sucesso"),
        bgcolor=Colors.GREEN
    )

    msg_error = ft.SnackBar(
        content=ft.Text('campos não podem estar vazios'),
        bgcolor=Colors.RED
    )

    imagem = ft.Image(
        src='biblioteca.jpg',
        width=300,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,  # Bordas arredondadas
    )

    imagem_2 = ft.Image(
        src='usuarios.png',
        width=200,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,
    )

    imagem_3 = ft.Image(
        src='emprestimos.jpg',
        width=200,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,
    )

    # LIVROS
    input_titulo = ft.TextField(label='Titulo', hint_text='insira titulo', col=4, hover_color=Colors.BLUE)
    input_resumo = ft.TextField(label='Resumo', hint_text='insira o resumo', col=4, hover_color=Colors.BLUE)
    input_ISBN = ft.TextField(label='ISBN', hint_text='insira o ISBN', col=4, hover_color=Colors.BLUE)
    input_autor = ft.TextField(label='Autor', hint_text='insira autor', col=4, hover_color=Colors.BLUE)

    # USUÁRIOS
    input_nome = ft.TextField(label='Nome', hint_text='insira nome', col=4, hover_color=Colors.BLUE)
    input_cpf = ft.TextField(label='Cpf', hint_text='insira cpf', col=4, hover_color=Colors.BLUE)
    input_endereco = ft.TextField(label='endereço', hint_text='insira o endereço', col=4, hover_color=Colors.BLUE)

    # EMPRÉSTIMOS

    # Eventos
    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.on_route_change = gerencia_rotas
    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)
