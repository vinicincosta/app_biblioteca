import flet as ft
from flet import AppBar, Text, View, Container, Column
from flet.core.colors import Colors
import requests
from flet.core.dropdown import Option
from flet.core.elevated_button import ElevatedButton
from rotas import *

id_usuario_global = 0
id_livro_global = 0


def main(page: ft.Page):
    # Configurações
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    # page.navigation_bar = ft.NavigationBar(
    #     destinations=[
    #         ft.NavigationBarDestination(icon=ft.Icons.EXPLORE, label="Regras"),
    #         ft.NavigationBarDestination(icon=ft.Icons.REPORT, label="Simulação"),
    #         ft.NavigationBarDestination(
    #             icon=ft.Icons.ACCOUNT_BOX,
    #             selected_icon=ft.Icons.BOOKMARK,
    #             label="Explorer",
    #
    #         ),
    #
    #     ],
    #     bgcolor=Colors.BLUE_200,
    # )

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
        print(response.json())
        if response.status_code == 201:
            dados_post_livro = response.json()

            print(f'Titulo: {dados_post_livro["titulo"]}\n'
                  f'Autor: {dados_post_livro["autor"]}\n'
                  f'Resumo: {dados_post_livro["resumo"]}\n'
                  f'ISBN: {dados_post_livro["ISBN"]}\n')
        else:
            print(f'Erro: {response.status_code}')

    def cadastrar_usuario_post(novo_usuario):
        url = "http://10.135.232.9:5000/novo_usuario"

        response = requests.post(url, json=novo_usuario)
        print(response.json())
        if response.status_code == 201:
            dados_post_usuario = response.json()

            print(f'Nome: {dados_post_usuario["nome"]}\n'
                  f'Cpf: {dados_post_usuario["cpf"]}\n'
                  f'Endereço: {dados_post_usuario["endereco"]}')
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
            return dados_post_emprestimo
        else:
            print(f'Erro: {response.json()}')
            return {'error': response.json()}

    def listar_livro():
        url = f'http://10.135.232.9:5000/livro'
        response = requests.get(url)

        if response.status_code == 200:
            dados_get_livro = response.json()
            print(dados_get_livro)
            return dados_get_livro['lista_livro']
        else:
            print(f'Erro: {response.status_code}')
            return response.json()

    def listar_usuario():
        url = f'http://10.135.232.9:5000/usuario'
        response = requests.get(url)
        if response.status_code == 200:
            dados_get_usuario = response.json()
            print(dados_get_usuario)
            return dados_get_usuario['lista_usuario']
        else:
            print(f'Erro: {response.status_code}')
            return response.json()

    def listar_emprestimos():
        url = f'http://10.135.232.9:5000/emprestimo'
        response = requests.get(url)
        if response.status_code == 200:
            dados_get_emprestimos = response.json()
            print(dados_get_emprestimos)
            return dados_get_emprestimos['lista_emprestimo']
        else:
            print(f'Erro: {response.status_code}')

    def editar_usuario_rota(id, novo_post_editar_usuario):
        url = f'http://10.135.232.9:5000/editar_usuario/{id}'

        response = requests.put(url, json=novo_post_editar_usuario)
        if response.status_code == 200:

            dados = response.json()
            print(f'id {dados["id_usuario"]}'
                  f'Nome: {dados["nome"]}\n'
                  f'Cpf: {dados["cpf"]}\n'
                  f'Endereço: {dados["endereco"]}')
            return dados
        else:
            print(f'Erro: {response.status_code}')
            print(f'Erro: {response.json()}')
            return response.json()

    def editar_livro_rota(id, novo_post_editar_livro):
        url = f'http://10.135.232.9:5000/editar_livro/{id}'

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

    def get_livro(id):
        url = f'http://10.135.232.9:5000/get_livro/{id}'
        response = requests.get(url)
        if response.status_code == 200:
            dados_get_postagem = response.json()
            print(dados_get_postagem)
            return dados_get_postagem
        else:
            print(f'Erro: {response.status_code}')
            return response.json()

    def get_usuario(id):
        url = f'http://10.135.232.9:5000/get_usuario/{id}'
        response = requests.get(url)
        if response.status_code == 200:
            dados_get_postagem = response.json()
            print(dados_get_postagem)
            return dados_get_postagem
        else:
            print(f'Erro: {response.status_code}')
            return response.json()

    # //////////////////////////////////////////////////////////////////////////////////////////////
    def add_titulo_lista(e):
        lv_livros.controls.clear()
        resultado_lista = listar_livro()
        print(f'Resultado: {resultado_lista}')

        # Lista de todos os livros
        for livro in resultado_lista:
            lv_livros.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                    title=ft.Text(f'Título - {livro["titulo"]}', color=Colors.WHITE),
                    subtitle=ft.Text(f'ISBN - {livro["ISBN"]}', color=Colors.WHITE),
                    bgcolor=Colors.BLUE_900,
                    expand=True,

                    trailing=ft.PopupMenuButton(
                        icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
                        bgcolor=Colors.BLUE_700,
                        items=[
                            ft.PopupMenuItem(text='Detalhes',
                                             on_click=lambda _, l=livro: exibir_detalhes_livro(l)),
                            ft.PopupMenuItem(text='Editar',
                                             on_click=lambda _, l=livro: editar_pagina_livro(e, l)),
                        ],
                    )
                )
            )
            page.update()

    def buscar_livro_id(e):
        lv_livros.controls.clear()
        resultado_lista = listar_livro()
        print(f'Resultado: {resultado_lista}')

        # Opções ID
        options = [Option(key=livro['id_livro'], text=livro['id_livro']) for livro in resultado_lista]

        def on_change_ID_filtrar(e):
            id_selecionado = input_get_livro.value
            print(f"ID selecionado: {id_selecionado}")

            # Filtra o livro pelo ID selecionado
            livro_filtrado = next((livro for livro in resultado_lista if str(livro['id_livro']) == id_selecionado))
            # O next é utilizado para encontrar um item especifico, (id)

            if livro_filtrado:
                lv_livros.controls.clear()
                lv_livros.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                        title=ft.Text(f'Título - {livro_filtrado["titulo"]}', color=Colors.WHITE),
                        subtitle=ft.Text(f'ISBN - {livro_filtrado["ISBN"]}', color=Colors.WHITE),
                        bgcolor=Colors.BLUE_900,
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
                            bgcolor=Colors.BLUE_700,
                            items=[
                                ft.PopupMenuItem(text='Detalhes',
                                                 on_click=lambda _, l=livro_filtrado: exibir_detalhes_livro(l)),
                                ft.PopupMenuItem(text='Editar',
                                                 on_click=lambda _, l=livro_filtrado: editar_pagina_livro(e, l)),
                            ],
                        )
                    )
                )

            page.update()

        input_get_livro = ft.Dropdown(
            bgcolor=Colors.BLUE_300,
            width=page.window.width,
            fill_color=Colors.RED,
            options=options,
            label='Buscar por ID',
            on_change=on_change_ID_filtrar
        )
        lv_livros.controls.append(input_get_livro)
        page.update()

    def add_usuario_lista(e):
        lv_livros.controls.clear()
        resultado_usuario = listar_usuario()
        print(f'Resltuado: {resultado_usuario}')

        for usuario in resultado_usuario:
            # lv_usuarios.dados_postagem = usuario
            lv_usuarios.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                    title=ft.Text(f'Nome - {usuario['nome']}', color=Colors.WHITE),
                    subtitle=ft.Text(f'cpf - {usuario["cpf"]}', color=Colors.WHITE),
                    bgcolor=Colors.BLUE_900,
                    expand=True,
                    trailing=ft.PopupMenuButton(
                        bgcolor=Colors.BLUE_700,
                        icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
                        items=[
                            ft.PopupMenuItem(text=f'Detalhes',
                                             on_click=lambda _, u=usuario: exibir_detalhes_usuarios(u)),

                            ft.PopupMenuItem(text=f'Editar',
                                             on_click=lambda _, u=usuario: editar_pagina_usuario(e, u)),

                        ],
                    )
                )
            )

    def buscar_usuario_id(e):
        lv_usuarios.controls.clear()
        resultado_lista = listar_usuario()
        print(f'Resultado: {resultado_lista}')

        # Opções ID
        options = [Option(key=usuario['id_usuario'], text=usuario['id_usuario']) for usuario in resultado_lista]

        def on_change_ID_filtrar(e):
            id_selecionado = input_get_usuario.value
            print(f"ID selecionado: {id_selecionado}")

            # Filtra o livro pelo ID selecionado
            usuario_filtrado = next(
                (usuario for usuario in resultado_lista if str(usuario['id_usuario']) == id_selecionado))
            # O next é utilizado para encontrar um item especifico, (id)

            if usuario_filtrado:
                lv_usuarios.controls.clear()
                lv_usuarios.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                        title=ft.Text(f'Título - {usuario_filtrado["nome"]}', color=Colors.WHITE),
                        subtitle=ft.Text(f'ISBN - {usuario_filtrado["cpf"]}', color=Colors.WHITE),
                        bgcolor=Colors.BLUE_900,
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
                            bgcolor=Colors.BLUE_700,
                            items=[
                                ft.PopupMenuItem(text='Detalhes',
                                                 on_click=lambda _, l=usuario_filtrado: exibir_detalhes_usuarios(l)),
                                ft.PopupMenuItem(text='Editar',
                                                 on_click=lambda _, l=usuario_filtrado: editar_pagina_usuario(e, l)),
                            ],
                        )
                    )
                )

            page.update()

        input_get_usuario = ft.Dropdown(
            bgcolor=Colors.BLUE_300,
            width=page.window.width,
            fill_color=Colors.RED,
            options=options,
            label='Buscar por ID',
            on_change=on_change_ID_filtrar
        )
        lv_usuarios.controls.append(input_get_usuario)
        page.update()

    def add_emprestimo_lista(e):
        lv_emprestimos.controls.clear()
        resultado_emprestimo = listar_emprestimos()
        print(f'Resltuado: {resultado_emprestimo}')

        for emprestimo in resultado_emprestimo:
            lv_emprestimos.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                    title=ft.Text(f'Data de empréstimo - {emprestimo["data_de_emprestimo"]}', color=Colors.WHITE),
                    bgcolor=Colors.BLUE_900,
                    trailing=ft.PopupMenuButton(
                        bgcolor=Colors.BLUE_700,
                        icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
                        items=[
                            ft.PopupMenuItem(text=f'Detalhes',
                                             on_click=lambda _, m=emprestimo: exibir_detalhes_emprestimos(m))
                        ]
                    )
                )
            )

    def exibir_detalhes_emprestimos(emprestimo):
        usuario_emprestimo = get_usuario(emprestimo["usuario_emprestado_id"])
        livro_emprestimo = get_livro(emprestimo["livro_emprestado_id"])

        txt_resultado_emprestimo.value = (f'Data de devolução - {emprestimo["data_de_devolucao"]}\n'
                                          f''
                                          f'Data de empréstimo - {emprestimo["data_de_emprestimo"]}\n'
                                          f''
                                          f'Usuário empréstimo - {usuario_emprestimo["nome"]}\n'
                                          f''
                                          f'Livro empréstimo - {livro_emprestimo['Titulo']}\n')
        page.go("/exibir_detalhes_emprestimos")

    def exibir_detalhes_usuarios(usuario):
        txt_resultado_usuarios.value = (f'Nome - {usuario['nome']}\n'
                                        f'CPf - {usuario['cpf']}\n'
                                        f'Endereço - {usuario['endereco']}\n'
                                        f'Id - {usuario["id_usuario"]}\n')

        page.go('/exibir_detalhes_usuarios')

    def editar_pagina_usuario(e, usuario):
        input_nome.value = usuario['nome']
        input_cpf.value = usuario['cpf']
        input_endereco.value = usuario['endereco']

        global id_usuario_global
        id_usuario_global = usuario['id_usuario']
        print(id_usuario_global)
        page.go('/editar_usuario')

    def editar_pagina_livro(e, livro):
        input_titulo.value = livro['titulo']
        input_resumo.value = livro['resumo']
        input_autor.value = livro['autor']
        input_ISBN.value = livro['ISBN']

        global id_livro_global
        id_livro_global = livro['id_livro']
        print(id_livro_global)
        page.go('/editar_livro')

    def exibir_detalhes_livro(livroo):
        txt_resultado_livros.value = (f'Titulo - {livroo['titulo']}\n'
                                      f'Resumo - {livroo['resumo']}\n'
                                      f'Autor - {livroo['autor']}\n'
                                      f'ISBN - {livroo['ISBN']}\n'
                                      f'ID - {livroo['id_livro']}\n')

        page.go('/exibir_detalhes_livro')

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
                'ISBN': input_ISBN.value
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
                'endereco': input_endereco.value
            }

            cadastrar_usuario_post(novo_usuario)
            input_endereco.value = ''
            input_cpf.value = ''
            input_nome.value = ''
            page.overlay.append(msg_sucesso)  # overlay sob escreve a página
            msg_sucesso.open = True
            page.update()

    def salvar_emprestimos(e):
        if (input_data_emprestimo.value == '' or input_data_devoulucao.value == ''
                or input_get_usuario_emprestimo.value == '' or input_get_livro_emprestimo == ''):
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            novo_emprestimo = {
                'data_de_emprestimo': input_data_emprestimo.value,
                'data_de_devolucao': input_data_devoulucao.value,
                'livro_emprestado_id': input_get_livro_emprestimo.value,
                'usuario_emprestado_id': input_get_usuario_emprestimo.value,
            }

            print("menu ", input_get_livro_emprestimo)

            resposta_emprestimo = cadastrar_emprestimo_post(novo_emprestimo)

            if 'error' in resposta_emprestimo:
                msg_error.open = True
            else:
                input_data_emprestimo.value = ''
                input_data_devoulucao.value = ''
                input_get_usuario_emprestimo.value = ''
                input_get_livro_emprestimo.value = ''
                page.overlay.append(msg_sucesso)  # overlay sob escreve a página
                msg_sucesso.open = True
            page.update()

    def editar_usuario(e):
        # try:
        print(input_nome.value)
        if input_nome.value == '' or input_cpf.value == '' or input_endereco.value == '':
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()
        else:
            print('teste else')
            dados_atualizados = {
                'nome': input_nome.value,
                'cpf': input_cpf.value,
                'endereco': input_endereco.value
            }
            global id_usuario_global

            print(id_usuario_global, "oi")
            resultado = editar_usuario_rota(id_usuario_global, dados_atualizados)
            print(resultado)

            if "error" in resultado:
                msg_error.content = ft.Text(resultado["error"])
                msg_error.open = True

            else:
                id_usuario_global = 0
                input_nome.value = ''
                input_cpf.value = ''
                input_endereco.value = ''
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
            page.update()

    def editar_livro(e):
        print(input_titulo.value)
        if input_titulo.value == '' or input_resumo.value == '' or input_autor.value == '' or input_ISBN.value == '':
            page.overlay.append(msg_error)
            msg_error.open = True
            page.update()

        else:
            print('teste')
            dados_atualizados = {
                'titulo': input_titulo.value,
                'resumo': input_resumo.value,
                'autor': input_autor.value,
                'ISBN': input_ISBN.value
            }
            global id_livro_global

            print(id_livro_global, "oi")
            resultado = editar_livro_rota(id_livro_global, dados_atualizados)
            print(resultado)

            if "error" in resultado:
                msg_error.content = ft.Text(resultado["error"])
                msg_error.open = True

            else:
                id_livro_global = 0
                input_titulo.value = ''
                input_resumo.value = ''
                input_autor.value = ''
                input_ISBN.value = ''
                page.overlay.append(msg_sucesso)
                msg_sucesso.open = True
            page.update()

        # except Exception as exc:
        #     page.overlay.append(msg_error)
        #     msg_error.open = True
        #     print(f"Erro ao editar usuário: {exc}")  # Log do erro para depuração
        #     page.update()

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
                                    width=150,
                                    text="Cadastrar Livro",
                                    bgcolor=Colors.BLUE_ACCENT,
                                    color=Colors.BLACK,
                                    on_click=lambda _: page.go('/cadastrar_livro'),

                                ),
                                ft.Button(
                                    width=150,
                                    text='Exibir Livros',
                                    bgcolor=Colors.BLUE_ACCENT,
                                    color=Colors.BLACK,
                                    on_click=lambda _: page.go('/exibir_livros'),
                                )
                            ],

                        ),
                        alignment=ft.alignment.center,
                        padding=ft.padding.only(top=5)
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
                            width=100,
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: salvar_livros(e),
                        ),

                        ft.Button(
                            width=100,
                            text="Exibir livros",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: page.go('/exibir_livros'),

                        )
                    ],
                    bgcolor=Colors.BLUE_200,

                )
            )

        if page.route == '/exibir_livros':
            add_titulo_lista(e)
            page.views.append(
                View(
                    '/exibir_livros',
                    [
                        AppBar(title=Text("Listar", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        ft.Button(
                            text="Buscar Livro",
                            width=350,
                            height=40,
                            bgcolor=Colors.BLUE_800,
                            color=Colors.WHITE,
                            on_click=lambda _: buscar_livro_id(e)

                        ),
                        lv_livros,

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/exibir_detalhes_livro':
            page.views.append(
                View(
                    'exibir_detalhes_livros',
                    [
                        AppBar(title=Text("Detalhes", font_family="Consolas"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        txt_resultado_livros
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/editar_livro':
            page.views.append(
                View(
                    '/editar_livro',
                    [
                        AppBar(title=Text('Editar', font_family="Consolas"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),

                        input_titulo,
                        input_autor,
                        input_resumo,
                        input_ISBN,

                        ft.Button(
                            text="Salvar",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: editar_livro(e),
                        ),

                    ],
                    bgcolor=Colors.BLUE_900
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
                                        width=200,
                                        text="Cadastrar Usuários",
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/cadastar_usuarios'),

                                    ),
                                    ft.Button(
                                        width=200,
                                        text='Exibir Usuarios',
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/exibir_usuarios'),
                                    )
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
                        ),
                        ft.Button(
                            text="Exibir usuários",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: page.go('/exibir_usuarios'),

                        )

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/exibir_usuarios':
            add_usuario_lista(e)
            page.views.append(
                View(
                    'exibir_usuarios',
                    [
                        AppBar(title=Text("Exibir lista", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        ft.Button(
                            text="Buscar Usuário",
                            width=350,
                            height=40,
                            bgcolor=Colors.BLUE_800,
                            color=Colors.WHITE,
                            on_click=lambda _: buscar_usuario_id(e)

                        ),
                        lv_usuarios
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/exibir_detalhes_usuarios':
            page.views.append(
                View(
                    'exibir_detalhes_usuarios',
                    [
                        AppBar(title=Text("Detalhes", font_family="Consolas"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        txt_resultado_usuarios,

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/editar_usuario':
            page.views.append(
                View('/editar_usuario',
                     [
                         AppBar(title=Text('Editar', font_family='Consolas'), bgcolor=Colors.BLUE_ACCENT,
                                center_title=True),

                         input_nome,
                         input_cpf,
                         input_endereco,

                         ft.Button(
                             text="Salvar",
                             bgcolor=Colors.BLUE_ACCENT,
                             color=Colors.BLACK,
                             on_click=lambda _: editar_usuario(e),
                         ),
                     ],
                     bgcolor=Colors.BLUE_900
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

                        Container(
                            Column(
                                [
                                    ft.Button(
                                        width=200,
                                        text="Cadastrar Empréstimos",
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/cadastrar_emprestimos'),

                                    ),
                                    ft.Button(
                                        width=200,
                                        text='Exibir Emprestimos',
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/exibir_emprestimos'),
                                    )
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

        if page.route == "/cadastrar_emprestimos":
            page.views.append(
                View(
                    "/cadastrar_emprestimos",
                    [
                        AppBar(title=Text("Cadastro Empéstimos", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        input_data_emprestimo,
                        input_data_devoulucao,
                        input_get_livro_emprestimo,
                        input_get_usuario_emprestimo,

                        ft.Button(
                            text="Salvar",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: salvar_emprestimos(e),
                        ),

                        # ft.ElevatedButton("Você realmente quer enviar esse cadastro?", on_click=lambda e: page.open(dlg_modal)),

                        ft.Button(
                            text="Exibir Emprestimos",
                            bgcolor=Colors.BLUE_ACCENT,
                            color=Colors.BLACK,
                            on_click=lambda _: page.go('/exibir_emprestimos'),
                        )

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/exibir_emprestimos":
            add_emprestimo_lista(e)
            page.views.append(
                View(
                    "/exibir_emprestimos",
                    [
                        AppBar(title=Text("Lista", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        lv_emprestimos,
                    ],
                    bgcolor=Colors.BLUE_900,
                )
            )

        if page.route == "/exibir_detalhes_emprestimos":
            page.views.append(
                View(
                    "/exibir_detalhes_emprestimos",
                    [
                        AppBar(title=Text("Detalhes", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        txt_resultado_emprestimo
                    ],
                    bgcolor=Colors.BLUE_200,
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
        width=200,

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
        src='emoti.png',
        width=200,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,

    )

    # LIVROS
    input_titulo = ft.TextField(label='Titulo', hint_text='insira titulo', col=4, hover_color=Colors.BLUE)
    input_resumo = ft.TextField(label='Resumo', hint_text='insira o resumo', col=4, hover_color=Colors.BLUE)
    input_ISBN = ft.TextField(label='ISBN', hint_text='insira o ISBN', col=4, hover_color=Colors.BLUE)
    input_autor = ft.TextField(label='Autor', hint_text='insira autor', col=4, hover_color=Colors.BLUE, )

    lv_livros = ft.ListView(
        height=700,
        spacing=5,
        divider_thickness=2
    )

    txt_resultado_livros = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)

    # USUÁRIOS
    input_nome = ft.TextField(label='Nome', hint_text='insira nome', col=4, hover_color=Colors.BLUE)
    input_cpf = ft.TextField(label='Cpf', hint_text='insira cpf', col=4, hover_color=Colors.BLUE)
    input_endereco = ft.TextField(label='endereço', hint_text='insira o endereço', col=4, hover_color=Colors.BLUE)

    lv_usuarios = ft.ListView(
        height=700,
        spacing=5,
        divider_thickness=2
    )

    txt_resultado_usuarios = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)

    # EMPRÉSTIMOS
    input_data_devoulucao = ft.TextField(label='Data de devolução', hint_text='insira a data de devoulucao', col=4,
                                         hover_color=Colors.BLUE)
    input_data_emprestimo = ft.TextField(label='Data de empréstimo', hint_text='insira a data de empréstimo', col=4,
                                         hover_color=Colors.BLUE)

    lv_emprestimos = ft.ListView(
        height=700,
        spacing=5,
        divider_thickness=2
    )

    txt_resultado_emprestimo = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)

    lv_livros.controls.clear()
    resultado_lista = listar_livro()
    print(f'Resultado: {resultado_lista}')

    options = [Option(key=livro['id_livro'], text=livro['titulo']) for livro in resultado_lista]

    input_get_livro_emprestimo = ft.Dropdown(
        bgcolor=Colors.BLUE_200,
        width=page.window.width,
        fill_color=Colors.RED,
        options=options,
        label='Livro empréstimo',
        color=Colors.BLACK,
        # on_change=on_change_id_livro_filtrar
    )

    lv_livros.controls.clear()
    resultado_usuario = listar_usuario()
    print(f'Resltuado: {resultado_usuario}')

    input_get_usuario_emprestimo = ft.Dropdown(
        bgcolor=Colors.BLUE_200,
        width=page.window.width,
        fill_color=Colors.RED,
        options=[Option(key=usuario['id_usuario'], text=usuario['nome']) for usuario in resultado_usuario],
        label='Usuário emprestimo',
        color=Colors.BLACK,
    )

    # Eventos
    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linha
ft.app(main)

# def salvar_emprestimos(e):
#     Dicionario livro
#     lv_livros.controls.clear()
#     resultado_lista = listar_livro()
#     print(f'Resultado: {resultado_lista}')
#
#     if (input_data_emprestimo.value == '' or input_data_devoulucao.value == ''
#             or input_get_usuario_emprestimo.value == '' or input_get_livro_emprestimo == ''):
#         page.overlay.append(msg_error)
#         msg_error.open = True
#         page.update()
#         return
#
#
#
#     Função de confirmação dentro do escopo principal
#     def confirmar_salvar(e):
#         novo_emprestimo = {
#             'data_de_emprestimo': input_data_emprestimo.value,
#             'data_de_devolucao': input_data_devoulucao.value,
#             'livro_emprestado_id': input_get_livro_emprestimo.value,
#             'usuario_emprestado_id': input_get_usuario_emprestimo.value,
#         }
#         cadastrar_emprestimo_post(novo_emprestimo)
#         input_data_emprestimo.value = ''
#         input_data_devoulucao.value = ''
#         input_get_usuario_emprestimo.value = ''
#         input_get_livro_emprestimo.value = ''
#         dlg_modal.open = False
#         page.overlay.append(msg_sucesso)
#         msg_sucesso.open = True
#         page.update()
#
#     def cancelar(e):
#         dlg_modal.open = False
#         page.update()
#
#     dlg_modal = ft.AlertDialog(
#         modal=True,
#         title=ft.Text("Confirmação"),
#         content=ft.Text("Deseja mesmo salvar esse cadastro? Pois depois de salvo não tem como mais editar."),
#         actions=[
#             ft.TextButton("Confirmar", on_click=lambda _: confirmar_salvar(e)),
#             ft.TextButton("Cancelar", on_click=lambda _: cancelar(e)),
#         ],
#         actions_alignment=ft.MainAxisAlignment.END,
#         on_dismiss=lambda e: print("Diálogo fechado sem confirmação."),
#     )
#     page.dialog = dlg_modal
#     dlg_modal.open = True
#     page.update()
