import flet as ft

from backend.voicera_backend import (
    register_user,
    login_user,
    load_session_user,
    clear_session_user,
)


# ============================================================
# VOICERA
# Cross-platform application
# ============================================================

def main(page: ft.Page):

    page.title = "VOICERA"
    page.padding = 0
    page.bgcolor = "#F6F3FB"

    current_user = load_session_user()

    # --------------------------------------------------------
    # Helpers
    # --------------------------------------------------------

    def show_message(text):
        page.show_dialog(
            ft.SnackBar(
                content=ft.Text(text)
            )
        )

    def open_login():
        username.value = ""
        password.value = ""
        message.value = ""
        page.clean()
        page.add(login_view())
        page.update()

    def open_register():
        reg_username.value = ""
        reg_password.value = ""
        reg_confirm.value = ""
        reg_message.value = ""
        page.clean()
        page.add(register_view())
        page.update()

    # --------------------------------------------------------
    # Login
    # --------------------------------------------------------

    username = ft.TextField(
        label="Username",
        width=330,
    )

    password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=330,
    )

    message = ft.Text(
        "",
        color="#B04A5A"
    )

    def do_login(e):

        ok, result = login_user(
            username.value,
            password.value
        )

        if ok:
            show_dashboard(username.value.strip())
        else:
            message.value = result
            page.update()

    def login_view():

        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                [
                    ft.Text(
                        "V",
                        size=64,
                        weight=ft.FontWeight.BOLD,
                        color="#7667A8"
                    ),

                    ft.Text(
                        "VOICERA",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="#29243A"
                    ),

                    ft.Text(
                        "Your Voice, Your Word.",
                        size=14,
                        color="#777180"
                    ),

                    ft.Container(height=25),

                    username,
                    password,

                    message,

                    ft.Button(
                        "Login",
                        width=330,
                        on_click=do_login
                    ),

                    ft.TextButton(
                        "Create an account",
                        on_click=lambda e: open_register()
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            )
        )

    # --------------------------------------------------------
    # Register
    # --------------------------------------------------------

    reg_username = ft.TextField(
        label="Username",
        width=330,
    )

    reg_password = ft.TextField(
        label="Password",
        password=True,
        can_reveal_password=True,
        width=330,
    )

    reg_confirm = ft.TextField(
        label="Confirm Password",
        password=True,
        can_reveal_password=True,
        width=330,
    )

    reg_message = ft.Text(
        "",
        color="#B04A5A"
    )

    def do_register(e):

        if reg_password.value != reg_confirm.value:
            reg_message.value = "Passwords do not match."
            page.update()
            return

        ok, result = register_user(
            reg_username.value,
            reg_password.value
        )

        if ok:
            reg_message.color = "#5B8065"
            reg_message.value = result
        else:
            reg_message.color = "#B04A5A"
            reg_message.value = result

        page.update()

    def register_view():

        return ft.Container(
            expand=True,
            alignment=ft.Alignment.CENTER,
            content=ft.Column(
                [
                    ft.Text(
                        "Create Account",
                        size=30,
                        weight=ft.FontWeight.BOLD,
                        color="#29243A"
                    ),

                    ft.Text(
                        "Start your VOICERA journey.",
                        size=14,
                        color="#777180"
                    ),

                    ft.Container(height=20),

                    reg_username,
                    reg_password,
                    reg_confirm,

                    reg_message,

                    ft.Button(
                        "Create Account",
                        width=330,
                        on_click=do_register
                    ),

                    ft.TextButton(
                        "Back to Login",
                        on_click=lambda e: open_login()
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=12,
            )
        )

    # --------------------------------------------------------
    # Dashboard
    # --------------------------------------------------------

    def show_dashboard(user):

        page.clean()

        page.add(
            ft.Container(
                expand=True,
                padding=40,
                content=ft.Column(
                    [
                        ft.Text(
                            "VOICERA",
                            size=32,
                            weight=ft.FontWeight.BOLD,
                            color="#29243A"
                        ),

                        ft.Text(
                            f"Welcome, {user}",
                            size=18,
                            color="#7667A8"
                        ),

                        ft.Container(height=20),

                        ft.Text(
                            "Your Voice, Your Word.",
                            size=15,
                            color="#777180"
                        ),

                        ft.Container(height=30),

                        ft.Button(
                            "Speech → Text"
                        ),

                        ft.Button(
                            "Text → Speech"
                        ),

                        ft.Button(
                            "History"
                        ),

                        ft.Button(
                            "Logout",
                            on_click=lambda e: logout()
                        ),
                    ],
                    spacing=15
                )
            )
        )

        page.update()

    # --------------------------------------------------------
    # Logout
    # --------------------------------------------------------

    def logout():

        clear_session_user()
        open_login()

    # --------------------------------------------------------
    # Start
    # --------------------------------------------------------

    if current_user:
        show_dashboard(current_user)
    else:
        page.add(login_view())


ft.run(main)
