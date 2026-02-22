from idlelib.outwin import file_line_pats

import flet as ft
from flet import AppBar, Text, View, Container, Column
from flet.core.colors import Colors
import requests
from flet.core.cupertino_app_bar import CupertinoAppBar
from flet.core.dropdown import Option
from flet.core.elevated_button import ElevatedButton
from flet.core.icons import Icons
from flet.core.types import CrossAxisAlignment
from teste_rotas import *
from rotas import *
from datetime import datetime
import math

id_usuario_global = 0
id_livro_global = 0
id_emprestimo_global = 0


def main(page: ft.Page):
    #
    # page.title = "Minha Biblioteca"
    # page.theme_mode = ft.ThemeMode.LIGHT
    #
    # page.add(
    #     ft.Text(
    #         "App rodando no celular 📱",
    #         size=20,
    #         weight=ft.FontWeight.BOLD
    #     )
    # )
    page.title = "Exemplo de Rotas"
    page.theme_mode = ft.ThemeMode.LIGHT  # ou ft.ThemeMode.DARK
    page.window.width = 375
    page.window.height = 667

    pagelet_user = ft.Pagelet(
        navigation_bar=ft.NavigationBar(
            destinations=[
                ft.NavigationBarDestination(icon=ft.Icons.BOOK, label="Livros"),
                ft.NavigationBarDestination(icon=ft.Icons.ADD_ALERT, label="Empréstimos"),
                ft.NavigationBarDestination(
                    icon=ft.Icons.HISTORY,
                    selected_icon=ft.Icons.HISTORY,
                    label="Ativos",
                ),

            ],
            bgcolor=Colors.BLUE_200,
            on_change=lambda e: page.go(
                ["/primeira_user", "/segunda_user", "/terceira_user"][e.control.selected_index]
            )
        ),
        content=ft.Container(),
        bgcolor=Colors.BLUE_200,
        height=200,
        expand=True,
    )

    # Funções
    def on_login_click(e):
        loading_indicator.visible = True
        page.update()

        resultado_usuarios = listar_usuario()
        print(f'Resultado: {resultado_usuarios}')

        # Verifica se os campos estão preenchidos
        if not input_email_login.value or not input_senha_login.value:
            snack_error('Erro: CPF e senha são obrigatórios.')
            page.update()
            return

        # Chama a função de login
        token, papel, nome, error = login(input_email_login.value, input_senha_login.value)

        print(f"Token: {token}, Papel: {papel}, Nome: {nome}, Erro: {error}")

        # Verifica se o usuário está inativo
        for usuario in resultado_usuarios:
            if usuario['cpf'] == input_cpf_login.value:  # Verifica se o CPF corresponde
                if usuario['status_user'] == "Inativo":
                    snack_error('Erro: usuário inativo.')
                    page.update()
                    return  # Sai da função se o usuário estiver inativo

        # Se o login foi bem-sucedido e o usuário está ativo
        if token:
            snack_sucesso(f'Login bem-sucedido, {nome} ({papel})!')
            print(f"Papel do usuário: {papel}, Nome: {nome}")

            for usuario in resultado_usuarios:
                if usuario['email'] == input_email_login.value:
                    page.client_storage.set("usuario_id", usuario["id_usuario"])
                    print("usuario_id salva na sessão:", usuario["id_usuario"])
                    break

            input_email_login.value = ""
            input_senha_login.value = ""

            if papel == "usuario":
                print("DEBUG CLIENT STORAGE:", page.client_storage.get("usuario_id"))

            if papel == "usuario":
                page.go("/primeira_user")  # Redireciona para a rota do usuário
            elif papel == "admin":
                page.go("/primeira")  # Redireciona para a rota do admin
            else:
                snack_error('Erro: Papel do usuário desconhecido.')
        else:
            snack_error(f'Erro: {error}')

        page.update()

    def on_cadastro_click(e):
        try:
            # Se não for admin, define como cliente
            papel = input_papel.value
            if papel != "admin":
                papel = "usuario"

            usuario, error = cadastrar_usuario(
                input_nome.value,
                input_cpf_cadastro.value,
                papel,  # papel já vem validado
                input_senha_cadastro.value,
                input_endereco.value,
                input_status_user.value,
                input_email_cadastro.value
            )
            if usuario:
                snack_sucesso(f'Usuário criado com sucesso! ID: {usuario["user_id"]}')
                page.overlay.append(msg_sucesso)
                page.go("/")
                page.update()

                input_nome.value = ""
                input_cpf_cadastro.value = ""
                input_papel.value = None
                input_senha_cadastro.value = ""
                input_endereco.value = ""
                input_email_cadastro.value = ""
                input_status_user.value = None
            else:
                snack_error(f'Erro: {error}')
                page.update()


        except Exception as e:
            snack_error(f'Erro: {e}')

        page.update()

    # //////////////////////////////////////////////////////////////////////////////////////////////

    def add_livros_lista(e):
        progress.visible = True
        lv_livros.controls.clear()
        resultado_lista = listar_livro()
        resultado_emprestimo = listar_emprestimos()
        resultado_usuario = listar_usuario()
        print(f'Resultado: {resultado_lista}')

        # Criar listas vazias para IDs de livros
        livros_emprestados_ids = []
        livros_atrasados_ids = []
        data_atual = datetime.now()

        # Cria um conjunto de IDs de livros emprestados
        for emprestimo in resultado_emprestimo:
            if emprestimo['status'] != 'Devolvido':
                livros_emprestados_ids.append(emprestimo['livro_emprestado_id'])
                # Verifica se a data de devolução é maior que a data atual
                data_devolucao = datetime.strptime(emprestimo['data_de_devolucao'], '%d-%m-%Y')
                if data_devolucao < data_atual:
                    livros_atrasados_ids.append(emprestimo['livro_emprestado_id'])

        # Usando ListView para permitir rolagem
        lv_livros.controls.append(
            ft.ListView(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                        title=ft.Text(f'Título - {livro["titulo"]}', color=Colors.WHITE),
                        subtitle=ft.Text(
                            'ATRASADO' if livro["id_livro"] in livros_atrasados_ids else
                            'EMPRESTADO' if livro["id_livro"] in livros_emprestados_ids else
                            f'ISBN - {livro["ISBN"]}',
                            color=Colors.WHITE
                        ),
                        bgcolor=(
                            Colors.RED_500 if livro["id_livro"] in livros_atrasados_ids else
                            Colors.ORANGE if livro["id_livro"] in livros_emprestados_ids else
                            Colors.BLUE_900
                        ),
                        height=80,  # Definindo uma altura fixa para cada item
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color=Colors.BLACK,
                            bgcolor=Colors.BLUE_700,
                            items=[
                                ft.PopupMenuItem(
                                    text='Detalhes',
                                    on_click=lambda _, l=livro: exibir_detalhes_livro_user(l)
                                ),
                                # ft.PopupMenuItem(
                                #     text='Editar',
                                #     on_click=lambda _, l=livro: editar_pagina_livro(e, l)
                                # ),
                                # ft.PopupMenuItem(text=f'Leitura',
                                #                  on_click=lambda _, l=livro: leitura_livro_titulo(l)),
                            ],
                        )
                    )
                    for livro in resultado_lista

                ],
                expand=True,  # Permite que o ListView ocupe o espaço disponível
            )
        )

        progress.visible = False  # Oculta o progresso após a atualização da lista
        page.update()

    def livros_emprestados(e):
        token = page.client_storage.get("token")
        if not token:
            snack_error('Usuário não logado')
            page.go("/")
            return

        usuario_id = page.client_storage.get("usuario_id")

        progress.visible = True
        page.update()

        # Buscar dados
        emprestimos = listar_emprestimos()
        livros = listar_livro()

        # 1️⃣ Filtrar empréstimos ATIVOS do usuário logado
        emprestimos_user_ativos = [
            emp for emp in emprestimos
            if emp.get("usuario_emprestado_id") == usuario_id
               and emp.get("status") == "Ativo"
        ]

        lv_livros.controls.clear()

        # Caso não exista nenhum livro emprestado
        if not emprestimos_user_ativos:
            lv_livros.controls.append(
                ft.Container(
                    alignment=ft.alignment.center,
                    expand=True,
                    content=ft.Column(
                        [
                            ft.Icon(
                                ft.Icons.MENU_BOOK,
                                size=60,
                                color=Colors.BLACK,
                            ),
                            ft.Text(
                                "Nenhum livro emprestado no momento",
                                font_family="Arial",
                                size=18,
                                weight="bold",
                                color=Colors.BLACK
                            ),
                            ft.Text(
                                "Quando você realizar um empréstimo, ele aparecerá aqui.",
                                font_family="Arial",
                                size=14,
                                weight="bold",
                                color=Colors.BLACK
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=10,
                    ),
                )
            )

            progress.visible = False
            page.update()
            return

        # 2️⃣ Criar dicionário de livros por ID
        livros_por_id = {livro["id_livro"]: livro for livro in livros}

        lv_livros.controls.clear()

        # 3️⃣ Criar ListView corretamente
        lv_livros.controls.append(
            ft.ListView(
                controls=[
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                        title=ft.Text(
                            f'Título - {livro["titulo"]}',
                            color=Colors.WHITE,
                            font_family="Arial"
                        ),
                        subtitle=ft.Text(
                            f'Devoulução - {emp["data_de_devolucao"]}',
                            color=Colors.WHITE,
                            font_family="Arial"
                        ),

                        bgcolor=Colors.BLUE_900,
                        height=80,
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color=Colors.BLACK,
                            bgcolor=Colors.BLUE_700,
                            items=[
                                ft.PopupMenuItem(
                                    text='Detalhes',
                                    on_click=lambda _, l=livro: exibir_detalhes_livro_user(l)
                                ),
                                ft.PopupMenuItem(
                                    text='Leitura',
                                    on_click=lambda _, l=livro: leitura_livro_titulo(l)
                                ),
                                ft.PopupMenuItem(
                                    text='Devolver livro',
                                    # PASSA O EMPRÉSTIMO CORRETO
                                    on_click=lambda _, emp=emp: editar_statuss_emprestimo(e, emp)
                                ),
                            ],
                        )
                    )
                    for emp in emprestimos_user_ativos
                    if (livro := livros_por_id.get(emp["livro_emprestado_id"])) is not None
                ],
                expand=True,
            )
        )

        progress.visible = False
        page.update()

    def add_historico_usuario(e):
        token = page.client_storage.get("token")
        if not token:
            snack_error("Usuário não logado")
            page.go("/")
            return

        usuario_id = page.client_storage.get("usuario_id")

        emprestimos = listar_emprestimos()

        # Filtrar empréstimos do usuário logado
        emprestimos = [e for e in emprestimos if e.get("usuario_emprestado_id") == usuario_id]

        emprestimos = [
            e for e in emprestimos
            if isinstance(e, dict) and e.get("usuario_emprestado_id") == usuario_id
        ]

        # Ordenar por data DESC
        emprestimos.sort(key=lambda e: e["data_de_emprestimo"])

        lv_emprestimos_geral.controls.clear()

        for emprestimo in emprestimos:

            status = emprestimo.get("status")

            if status == "Ativo":
                card_color = Colors.GREEN

            elif status == "Devolvido":
                card_color = Colors.RED_300

            # Formatar data
            data_formatada = emprestimo["data_de_emprestimo"]
            try:
                dt = datetime.strptime(data_formatada, "%Y-%m-%d %H:%M:%S")
                data_formatada = dt.strftime("%d/%m/%Y - %H:%M")
            except:
                pass

            # Card grande e estilizado
            card = ft.Container(
                padding=15,
                bgcolor=card_color,
                border_radius=20,
                shadow=ft.BoxShadow(
                    blur_radius=12,
                    spread_radius=1,
                    color=Colors.BLACK54,
                    offset=ft.Offset(0, 4)
                ),
                margin=10,
                width=350,
                content=ft.Column(
                    [
                        ft.Row(
                            [
                                ft.Icon(ft.Icons.RECEIPT_LONG, size=32, color=Colors.BLACK),
                                ft.Text(
                                    f"Empréstimo #{emprestimo['id_emprestimo']}",
                                    size=22,
                                    weight="bold",
                                    color=Colors.BLACK,
                                )
                            ]
                        ),

                        ft.Text(

                            size=17,
                            weight="bold",
                            color=Colors.BLACK,
                        ),

                        ft.Text(
                            data_formatada,
                            size=16,
                            color=Colors.BLACK,
                        ),

                        ft.Text(
                            f"Status: {status}",
                            size=18,
                            color=Colors.BLACK,
                            weight="bold"
                        ),

                    ],

                    spacing=8,
                ),

            )

            lv_emprestimos_geral.controls.append(card)

        page.update()

    def buscar_livro_id(e):
        lv_livros.controls.clear()
        resultado_lista = listar_livro()
        resultado_emprestimo = listar_emprestimos()
        print(f'Resultado: {resultado_lista}')

        # Opções ID
        options = [Option(key=livro['id_livro'], text=str(livro['id_livro'])) for livro in resultado_lista]

        def on_change_ID_filtrar(e):
            id_selecionado = input_get_livro.value
            print(f"ID selecionado: {id_selecionado}")

            # Filtra o livro pelo ID selecionado
            livro_filtrado = next((livro for livro in resultado_lista if str(livro['id_livro']) == id_selecionado),
                                  None)

            livros_emprestados_ids = []
            livros_atrasados_ids = []
            data_atual = datetime.now()

            # Cria um conjunto de IDs de livros emprestados e atrasados
            for emprestimo in resultado_emprestimo:
                if emprestimo['status'] != 'Devolvido':
                    livros_emprestados_ids.append(emprestimo['livro_emprestado_id'])
                    # Verifica se a data de devolução já passou
                    data_de_devolucao = datetime.strptime(emprestimo['data_de_devolucao'], '%d-%m-%Y')
                    if data_de_devolucao < data_atual:
                        livros_atrasados_ids.append(emprestimo['livro_emprestado_id'])

            if livro_filtrado:
                lv_livros.controls.clear()
                livro_id = livro_filtrado["id_livro"]
                titulo_livro = livro_filtrado["titulo"]
                isbn_livro = livro_filtrado["ISBN"]

                # Verifica se o livro está emprestado

                if livro_id in livros_emprestados_ids:
                    bgcolor = Colors.ORANGE  # Cor para livros emprestados
                    subtitle_text = 'EMPRESTADO'
                else:
                    bgcolor = Colors.BLUE_900  # Cor para livros disponíveis
                    subtitle_text = f'ISBN - {isbn_livro}'

                lv_livros.controls.append(
                    ft.ListTile(
                        leading=ft.Icon(ft.Icons.BOOK, color=Colors.BLACK),
                        title=ft.Text(f'Título - {titulo_livro}', color=Colors.WHITE),
                        subtitle=ft.Text(subtitle_text, color=Colors.WHITE),
                        bgcolor=bgcolor,
                        trailing=ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT, icon_color=Colors.BLACK,
                            bgcolor=Colors.BLUE_700,
                            items=[
                                ft.PopupMenuItem(text='Detalhes',
                                                 on_click=lambda _, l=livro_filtrado: exibir_detalhes_livro_user(l)),
                                # ft.PopupMenuItem(text='Editar',
                                #                  on_click=lambda _, l=livro_filtrado: editar_pagina_livro(e, l)),
                            ],
                        )
                    )
                )

            page.update()

        input_get_livro = ft.Dropdown(
            bgcolor=Colors.BLUE_300,
            width=page.window.width,
            options=options,
            label='Buscar por ID',
            on_change=on_change_ID_filtrar
        )
        lv_livros.controls.append(input_get_livro)
        page.update()

    def exibir_detalhes_livro(livroo):
        txt_resultado_livros.value = (f'Titulo - {livroo['titulo']}\n'
                                      f'Resumo - {livroo['resumo']}\n'
                                      f'Autor - {livroo['autor']}\n'
                                      f'ISBN - {livroo['ISBN']}\n'
                                      f'ID - {livroo['id_livro']}\n'
                                      )

        page.go('/exibir_detalhes_livro')

    def leitura_livro_titulo(livroo):
        txt_resultado_leitura.value = ({livroo['leitura']})
        page.go('/leitura_livro')

    def leitura_livro(livro_id):
        # Carrega a lista atualizada de livros
        lista_livros = listar_livro()

        # Procura o livro específico pelo ID
        livro_encontrado = None
        for livro in lista_livros:
            if livro.get('id_livro') == livro_id:
                livro_encontrado = livro
                break

        # Verifica se encontrou o livro e se tem a chave 'leitura'
        if livro_encontrado and 'leitura' in livro_encontrado:
            txt_resultado_leitura.value = {livro_encontrado["leitura"]}
        else:
            txt_resultado_leitura.value = "Informação de leitura não disponível"

        page.go('/leitura_livro')

    def exibir_detalhes_livro_user(livroo):
        txt_resultado_livros_user.value = (f'Titulo - {livroo['titulo']}\n'
                                           f'Resumo - {livroo['resumo']}\n'
                                           f'Autor - {livroo['autor']}\n'
                                           f'ISBN - {livroo['ISBN']}\n'
                                           f'ID - {livroo['id_livro']}\n')

        page.go('/exibir_detalhes_livro_user')

    def salvar_emprestimos(e):
        try:
            usuario_id = page.client_storage.get('usuario_id')
            if not usuario_id:
                snack_error("Usuário não logado")
                page.go('/login')
                return

            if input_get_livro_emprestimo.value == '':
                msg_error.open = True
                page.update()
                return

            novo_emprestimo = {

                "livro_emprestado_id": input_get_livro_emprestimo.value,
                "usuario_emprestado_id": usuario_id,
            }

            resposta = cadastrar_emprestimo_post(novo_emprestimo)

            if "error" in resposta:
                msg_error.open = True
            else:
                dlg_modal.open = False

                input_get_livro_emprestimo.value = ''
                page.overlay.append(msg_sucesso)  # overlay sob escreve a página
                msg_sucesso.open = True

            page.update()

        except Exception as e:
            print("Erro:", e)
            snack_error("Erro ao salvar empréstimo")

    def editar_statuss_emprestimo(e, emprestimo):
        resultado = editar_status_emprestimo_rota(emprestimo['id_emprestimo'])

        if "error" not in resultado:
            msg_sucesso_status.open = True
            livros_emprestados(e)

        page.overlay.append(msg_sucesso_status)
        msg_sucesso_status.open = True

        page.update()

    dlg_modal = ft.AlertDialog(
        title=ft.Text("ALERTA‼️"),
        content=ft.Text("Você realmente confirma esse cadastro, após cadastrado não terá como editar",
                        color=Colors.WHITE, font_family='Arial', size=18),
        actions=[
            ft.TextButton("SIM", on_click=salvar_emprestimos),
            ft.TextButton("NÃO", on_click=lambda e: fechar_dialogo(e)),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
        bgcolor=Colors.BLUE_700,
    )

    def fechar_dialogo(e):
        dlg_modal.open = False
        page.update()

    def click_logout(e):
        page.client_storage.remove("access_token")
        snack_sucesso("logout realizado com sucesso")
        page.go("/")

    def gerencia_rotas(e):
        input_cpf_login.value = ""
        input_senha_login.value = ""
        page.views.clear()
        if page.route == "/":
            page.views.append(
                View(
                    "/",

                    [
                        AppBar(title=Text("Login", size=24), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        Column(
                            [
                                Text("Bem-vindo!", size=30, color=Colors.BLUE_900),
                                Text("Por favor, faça login para continuar.", size=16, color=Colors.BLUE_700),
                                input_email_login,
                                input_senha_login,
                                ElevatedButton(
                                    "Entrar",
                                    on_click=lambda e: on_login_click(e),
                                    bgcolor=Colors.BLUE_800,
                                    color=Colors.WHITE,
                                ),
                            ],
                            spacing=20,
                        ),
                        Column(
                            [
                                Text("Caso não possuir um login, faça o seu cadastro", size=20, color=Colors.BLUE_900),
                                ElevatedButton(
                                    "Cadastro",
                                    on_click=lambda e: page.go("/cadastro_usuario_login"),
                                    bgcolor=Colors.BLUE_800,
                                    color=Colors.WHITE,
                                )
                            ],
                            spacing=20,
                        )
                    ],
                    bgcolor=Colors.BLUE_200,
                    padding=20,  # Adiciona padding ao redor da coluna
                )
            )

        if page.route == "/cadastro_usuario_login":
            input_nome.value = ""
            input_email_login.value = ""
            input_endereco.value = ""
            input_cpf_cadastro.value = ""
            input_senha_cadastro.value = ""

            page.views.append(
                View
                    (
                    "/cadastro_usuario_login",
                    [
                        AppBar(title=Text("Cadastro users", font_family="Arial", size=24), bgcolor=Colors.BLUE_ACCENT),

                        input_nome,
                        input_cpf_cadastro,
                        input_email_cadastro,
                        input_endereco,

                        input_senha_cadastro,

                        ElevatedButton(
                            "Cadastrar",
                            on_click=lambda e: on_cadastro_click(e),
                            bgcolor=Colors.BLUE_900,
                            color=Colors.WHITE,
                        ),
                        ElevatedButton(
                            "Voltar",
                            on_click=lambda e: page.go("/"),
                            bgcolor=Colors.BLUE_900,
                            color=Colors.WHITE,
                        ),
                    ],
                    bgcolor=Colors.BLUE_200,

                )
            )

        if page.route == "/primeira_user":
            page.views.append(
                View(
                    "/primeira_user",
                    [
                        AppBar(title=Text("Livros", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True, leading=ft.Icon(), actions=[btn_logout]),
                        Container(
                            Column(
                                [
                                    imagem,
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=10)
                        ),
                        Container(
                            Column(
                                [
                                    ft.Button(
                                        width=150,
                                        text='Exibir Livros',
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/exibir_livros_user'),
                                    )
                                ],
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=5)

                        ),
                        pagelet_user,
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/exibir_livros_user':
            add_livros_lista(e)
            page.views.append(
                View(
                    '/exibir_livros_user',
                    [
                        AppBar(title=Text("Livros", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True, actions=[btn_logout_exibir_livros]),
                        ft.Button(
                            text="Buscar Livro",
                            width=350,
                            height=40,
                            bgcolor=Colors.BLUE_800,
                            color=Colors.WHITE,
                            on_click=lambda _: buscar_livro_id(e),
                        ),

                        lv_livros,

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == '/exibir_detalhes_livro_user':
            page.views.append(
                View(
                    'exibir_detalhes_livros_user',
                    [
                        AppBar(title=Text("Detalhes", font_family="Consolas"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True, actions=[btn_logout_exibir_detalhes_livros]),
                        txt_resultado_livros_user,
                        # Botão de voltar
                        pagelet_user,
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/segunda_user":
            page.views.append(
                View(
                    "/segunda_user",
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
                                        on_click=lambda _: page.go('/cadastrar_emprestimos_user'),
                                    ),

                                ],
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=5)
                        ),
                        pagelet_user
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/cadastrar_emprestimos_user":
            page.views.append(
                View(
                    "/cadastrar_emprestimos_user",
                    [
                        AppBar(
                            title=Text("Cadastro de Empréstimos"),
                            bgcolor=Colors.BLUE_ACCENT,
                            center_title=True
                        ),

                        ft.Text(
                            "Prazo máximo de devolução: 20 dias",
                            font_family="Arial",
                            weight="bold",
                            size=18,
                            color=Colors.BLACK,
                        ),

                        # (Opcional)
                        txt_data_prevista,

                        input_get_livro_emprestimo,

                        ft.ElevatedButton("Salvar", on_click=lambda e: page.open(dlg_modal)),

                        pagelet_user
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/leitura_livro":

            # ================= CONFIGURAÇÕES =================
            caracteres_por_pagina = 800
            pagina_atual = 1
            tamanho_fonte = 18
            modo_noturno = False

            # ================= FUNÇÕES =================
            def dividir_texto_em_paginas(texto):
                if not isinstance(texto, str):
                    texto = str(texto)

                palavras = texto.split()
                paginas = []
                pagina = []
                contador = 0

                for palavra in palavras:
                    if contador + len(palavra) > caracteres_por_pagina and pagina:
                        paginas.append(" ".join(pagina))
                        pagina = []
                        contador = 0

                    pagina.append(palavra)
                    contador += len(palavra) + 1

                if pagina:
                    paginas.append(" ".join(pagina))

                return paginas

            # ================= CONTEÚDO =================
            conteudo = txt_resultado_leitura.value or "Nenhum conteúdo disponível"
            paginas = dividir_texto_em_paginas(conteudo)

            if not paginas:
                paginas = ["Nenhum conteúdo disponível"]

            # ================= TEXTO =================
            txt_display = ft.Text(
                value="",
                selectable=True,
                text_align=ft.TextAlign.JUSTIFY,
                font_family="Georgia",
                size=tamanho_fonte,
                style=ft.TextStyle(height=1.6),
                no_wrap=False
            )

            indicador = ft.Text(size=14)
            progresso = ft.ProgressBar(value=0)

            # ================= CONTAINERS =================
            area_leitura = ft.Container(
                content=txt_display,
                padding=30,
                width=800,
                bgcolor=Colors.WHITE,
                border_radius=12,
                shadow=ft.BoxShadow(
                    blur_radius=12,
                    color=Colors.BLACK12,
                    offset=ft.Offset(0, 4)
                )
            )

            fundo = ft.Container(expand=True)

            # ================= ATUALIZAÇÕES =================
            def atualizar_estilo():
                txt_display.size = tamanho_fonte
                txt_display.color = Colors.WHITE if modo_noturno else Colors.BLACK87
                area_leitura.bgcolor = Colors.BLACK87 if modo_noturno else Colors.WHITE
                fundo.bgcolor = Colors.BLACK if modo_noturno else Colors.BLUE_GREY_50

            def atualizar_pagina():
                nonlocal pagina_atual

                # 🔒 GARANTE QUE NÃO ESTOURE ÍNDICE
                if pagina_atual < 1:
                    pagina_atual = 1
                if pagina_atual > len(paginas):
                    pagina_atual = len(paginas)

                txt_display.value = paginas[pagina_atual - 1]
                indicador.value = f"Página {pagina_atual} de {len(paginas)}"
                progresso.value = pagina_atual / len(paginas)

                atualizar_estilo()
                page.update()

            def proxima(e):
                nonlocal pagina_atual
                if pagina_atual < len(paginas):
                    pagina_atual += 1
                    atualizar_pagina()

            def anterior(e):
                nonlocal pagina_atual
                if pagina_atual > 1:
                    pagina_atual -= 1
                    atualizar_pagina()

            def aumentar_fonte(e):
                nonlocal tamanho_fonte
                tamanho_fonte += 2
                atualizar_estilo()
                page.update()

            def diminuir_fonte(e):
                nonlocal tamanho_fonte
                if tamanho_fonte > 12:
                    tamanho_fonte -= 2
                    atualizar_estilo()
                    page.update()

            def alternar_modo(e):
                nonlocal modo_noturno
                modo_noturno = not modo_noturno
                atualizar_estilo()
                page.update()

            # ================= LAYOUT =================
            fundo.content = ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                ft.Icons.ARROW_BACK,
                                tooltip="Voltar",
                                on_click=lambda _: page.go("/emprestimos_ativos")
                            ),
                            indicador,
                            ft.Row(
                                [
                                    ft.IconButton(ft.Icons.REMOVE, on_click=diminuir_fonte),
                                    ft.IconButton(ft.Icons.ADD, on_click=aumentar_fonte),
                                    ft.IconButton(ft.Icons.DARK_MODE, on_click=alternar_modo)
                                ]
                            )
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                    ),

                    progresso,

                    ft.Row(
                        [area_leitura],
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    ),

                    ft.Row(
                        [
                            ft.IconButton(ft.Icons.ARROW_BACK_IOS, on_click=anterior),
                            ft.IconButton(ft.Icons.ARROW_FORWARD_IOS, on_click=proxima)
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=40
                    )
                ],
                expand=True,
                spacing=20
            )

            # ================= INICIALIZA =================
            atualizar_pagina()

            page.views.append(
                View(
                    "/leitura_livro",
                    [fundo],
                )
            )

        if page.route == "/terceira_user":
            page.views.append(
                View(
                    "/terceira_user",
                    [
                        AppBar(title=Text("Histórico", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True),
                        Container(
                            Column(
                                [
                                    imagem_4,
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
                                        text="Ativos",
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/emprestimos_ativos'),
                                    ),

                                    ft.Button(
                                        width=200,
                                        text="Histórico",
                                        bgcolor=Colors.BLUE_ACCENT,
                                        color=Colors.BLACK,
                                        on_click=lambda _: page.go('/historico_geral'),
                                    ),

                                ],
                            ),
                            alignment=ft.alignment.center,
                            padding=ft.padding.only(top=5)
                        ),

                        pagelet_user,
                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/emprestimos_ativos":
            livros_emprestados(e)
            page.views.append(
                View(
                    "/emprestimos_ativos",
                    [
                        AppBar(title=Text("Meus livros", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True, actions=[btn_logout_emprestimos_ativos]),

                        lv_livros,

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        if page.route == "/historico_geral":
            add_historico_usuario(None)
            page.views.append(
                View(
                    "/historico_geral",
                    [

                        AppBar(title=Text("Histórico", font_family="Arial"), bgcolor=Colors.BLUE_ACCENT,
                               center_title=True, actions=[btn_logout_historico_geral]),
                        ft.Text("Histórico de Empréstimos", font_family="Arial", size=22, color=Colors.BLUE_900,
                                weight="bold"),

                        lv_emprestimos_geral

                    ],
                    bgcolor=Colors.BLUE_200,
                )
            )

        page.update()

    # Componentes
    loading_indicator = ft.ProgressRing(visible=False, width=20, height=20, stroke_width=2)

    progress = ft.ProgressRing(visible=False)

    # Botoões saídas

    btn_logout_emprestimos_ativos = ft.TextButton(
        icon=Icons.LOGOUT,
        scale=1.5,
        icon_color=Colors.BLUE_700,
        on_click=lambda _: page.go("/terceira_user"),
    )

    btn_logout_historico_geral = ft.TextButton(
        icon=Icons.LOGOUT,
        scale=1.5,
        icon_color=Colors.BLUE_700,
        on_click=lambda _: page.go("/terceira_user"),
    )

    btn_logout_exibir_livros = ft.TextButton(
        icon=Icons.LOGOUT,
        scale=1.5,
        icon_color=Colors.BLUE_700,
        on_click=lambda _: page.go("/primeira_user"),
    )

    btn_logout_exibir_detalhes_livros = ft.TextButton(
        icon=Icons.LOGOUT,
        scale=1.5,
        icon_color=Colors.BLUE_700,
        on_click=lambda _: page.go("/emprestimos_ativos"),
    )

    msg_sucesso = ft.SnackBar(

        content=ft.Text("campos salvo com sucesso"),
        bgcolor=Colors.GREEN
    )

    msg_sucesso_status = ft.SnackBar(
        content=ft.Text("Livro devolvido com sucesso"),
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
        width=150,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,
    )

    imagem_3 = ft.Image(
        src='livros_em.jpg',
        width=200,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,

    )
    imagem_4 = ft.Image(
        src="livros_historico.png",
        width=200,
        fit=ft.ImageFit.CONTAIN,
        border_radius=10,
    )

    # LIVROS
    input_titulo = ft.TextField(label='Titulo', hint_text='insira titulo', col=4, hover_color=Colors.BLUE)
    input_resumo = ft.TextField(label='Resumo', hint_text='insira o resumo', col=4, hover_color=Colors.BLUE)
    input_ISBN = ft.TextField(label='ISBN', hint_text='insira o ISBN', col=4, hover_color=Colors.BLUE)
    input_autor = ft.TextField(label='Autor', hint_text='insira autor', col=4, hover_color=Colors.BLUE)
    input_leitura = ft.TextField(
        label='Leitura',
        hint_text='Insira a leitura',
        width=500,  # Largura aumentada
        # Altura aumentada (em pixels)
        hover_color=Colors.BLUE,
        cursor_width=5,
        multiline=True  # Permite múltiplas linhas de texto
    )

    lv_livros = ft.ListView(
        expand=True,
        height=700,
        spacing=5,
        divider_thickness=2,
        auto_scroll=False  # não rola sozinho
    )

    txt_resultado_livros = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)
    txt_resultado_livros_user = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)

    txt_resultado_leitura = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)
    # USUÁRIOS
    input_nome = ft.TextField(label='Nome', hint_text='insira nome', col=4, hover_color=Colors.BLUE)
    input_email = ft.TextField(label="Email", hint_text="insira seu email", col=4, hover_color=Colors.BLUE)
    input_cpf = ft.TextField(label='Cpf', hint_text='insira cpf', col=4, hover_color=Colors.BLUE)
    input_endereco = ft.TextField(label='endereço', hint_text='insira o endereço', col=4, hover_color=Colors.BLUE)

    lv_usuarios = ft.ListView(

    )

    txt_resultado_usuarios = ft.Text('', font_family="Arial", size=19, color=Colors.BLACK, )

    # EMPRÉSTIMOS
    txt_data_prevista = ft.Text(
        "Data prevista de devolução: --/--/----",
        size=14,
        color=Colors.BLACK87
    )

    input_data_emprestimo = ft.TextField(label='Data de empréstimo', hint_text='insira a data de empréstimo', col=4,
                                         hover_color=Colors.BLUE)

    lv_emprestimos = ft.ListView(
        height=700,
        spacing=5,
        divider_thickness=0
    )

    lv_emprestimos_geral = ft.ListView(
        expand=True,  # ocupa a tela
        spacing=10,
        padding=10,
        auto_scroll=False  # não rola sozinho
    )

    lv_emprestimos_devolvidos = ft.ListView(
        height=700,
        spacing=5,
        divider_thickness=0
    )

    lv_emprestimos_atrasados = ft.ListView(
        height=700,
        spacing=5,
        divider_thickness=0
    )

    txt_resultado_emprestimo = ft.Text('', font_family="Arial", size=18, color=Colors.BLACK)

    lv_livros.controls.clear()
    resultado_lista = listar_livro()
    resultado_emprestimo = listar_emprestimos()  # Obter lista de empréstimos ativos
    print(f'Resultado: {resultado_lista}')

    # Criar lista de IDs de livros emprestados
    livros_emprestados_ids = [emp['livro_emprestado_id'] for emp in resultado_emprestimo
                              if emp['status'] != 'Devolvido']

    options = [Option(key=l['id_livro'], text=f"{l['titulo']} (ID: {l['id_livro']})")
               for l in resultado_lista
               if l.get('id_livro') not in livros_emprestados_ids] or \
              [Option(key=None, text="Nenhum livro disponível", disabled=True)]

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

    usuarios_ativos = [user['id_usuario'] for user in resultado_usuario
                       if user['status_user'] != 'Ativo']

    options = [Option(key=u['id_usuario'], text=f"{u['nome']} (ID:{u['id_usuario']})")
               for u in resultado_usuario
               if u.get('id_usuario') not in usuarios_ativos] or \
              [Option(key=None, text="Nenhum usuário ativo", disabled=True)]

    input_get_usuario_emprestimo = ft.Dropdown(
        bgcolor=Colors.BLUE_200,
        width=page.window.width,
        fill_color=Colors.RED,
        options=options,
        label='Usuário emprestimo',
        color=Colors.BLACK,
    )

    lv_livros.controls.clear()
    resultado_emprestimo = listar_emprestimos()
    print(f'Resltuado: {resultado_emprestimo}')

    t = ft.Tabs(

        selected_index=1,
        animation_duration=300,
        tabs=[
            ft.Tab(
                text="Emprestado",
                content=ft.Container(
                    lv_emprestimos,

                ),
            ),
            ft.Tab(

                text="Devovlvidos",
                icon=ft.Icons.SETTINGS,
                content=ft.Container(
                    lv_emprestimos_devolvidos,

                ),

            ),

            ft.Tab(
                text="Atrasados",
                icon=ft.Icons.DANGEROUS_OUTLINED,
                content=ft.Container(
                    lv_emprestimos_atrasados,
                ),
            ),
        ],
        expand=1,
    )
    # ---------------------------------------#-------------------------------------

    # Elementos de Login

    btn_logout = ft.TextButton(
        icon=Icons.LOGOUT,
        scale=1.5,
        icon_color=Colors.RED_700,
        on_click=click_logout
    )

    input_cpf_login = ft.TextField(
        label='CPF',
        hint_text='Insira seu CPF',
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.BLUE_700,
        focused_border_color=Colors.BLUE_900,
        bgcolor=Colors.WHITE,

    )

    input_email_login = ft.TextField(
        label="Email",
        hint_text="Insira seu e-mail",
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.BLUE_700,
        focused_border_color=Colors.BLUE_900,
        bgcolor=Colors.WHITE,
    )

    input_senha_login = ft.TextField(
        label='Senha',
        hint_text='Insira sua senha',
        password=True,
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.BLUE_700,
        focused_border_color=Colors.BLUE_900,
        bgcolor=Colors.WHITE,

    )

    # Mensagem de login
    login_message = ft.Text('', color=Colors.RED_ACCENT_700, size=18, font_family="Arial", bgcolor=Colors.WHITE)

    # Campos de entrada
    input_nome = ft.TextField(
        label='Nome',
        hint_text='Insira seu nome',
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.GREY_400,
        focused_border_color=Colors.BLUE,
        bgcolor=Colors.WHITE,
        width=300,
    )

    input_cpf_cadastro = ft.TextField(
        label='CPF',
        hint_text='Insira seu CPF',
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.GREY_400,
        focused_border_color=Colors.BLUE,
        bgcolor=Colors.WHITE,
        width=300,

    )

    input_email_cadastro = ft.TextField(
        label='email',
        hint_text='Insira seu email',
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.GREY_400,
        focused_border_color=Colors.BLUE,
        bgcolor=Colors.WHITE,
        width=300,

    )

    input_senha_cadastro = ft.TextField(
        label='Senha',
        hint_text='Insira sua senha',
        password=True,
        col=4,
        hover_color=Colors.BLUE,
        border_color=Colors.GREY_400,
        focused_border_color=Colors.BLUE,
        bgcolor=Colors.WHITE,
        width=300,
    )

    input_papel = ft.Dropdown(
        label="Papel",
        width=300,
        fill_color=Colors.RED,
        options=[
            Option(key="admin", text="admin"),
            Option(key="usuario", text="usuario")

        ],
        border_color=Colors.GREY_400,
        focused_border_color=Colors.BLUE,
        bgcolor=Colors.WHITE,
    )

    input_status_user = ft.Dropdown(
        label="Status",
        width=300,
        fill_color=Colors.RED,
        options=[
            Option(key="Ativo", text="Ativo"),
            Option(key="Inativo", text="Inativo")
        ]
    )

    def snack_sucesso(texto: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=Colors.GREEN
        )
        page.snack_bar.open = True
        page.overlay.append(page.snack_bar)

    def snack_error(texto: str):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(texto),
            bgcolor=Colors.RED
        )
        page.snack_bar.open = True
        page.overlay.append(page.snack_bar)

    # Eventos
    def voltar(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = gerencia_rotas
    page.on_view_pop = voltar
    page.go(page.route)


# Comando que executa o aplicativo
# Deve estar sempre colado na linh
# ft.app(
#     target=main,
#     host="0.0.0.0",
#     port=8550,  # 🔥 OUTRA PORTA
#     view=ft.AppView.WEB_BROWSER  # 👈 MUITO IMPORTANTE
# )
ft.app(main)
