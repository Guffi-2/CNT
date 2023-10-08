import flet as ft
import sqlite3 as sq

with sq.connect("users.db") as con:
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    id_space INTEGER NOT NULL,
    dolg INTEGER NOT NULL,
    chlenskie_vznos_nachislenno INTEGER NOT NULL,
    celevie_vznosi_nachislenno INTEGER NOT NULL,
    chlenskie_vznos_oplacheno INTEGER NOT NULL,
    celevie_vznosi_oplacheno INTEGER NOT NULL,
    itog_nachislenno INTEGER NOT NULL,
    itog_oplacheno INTEGER NOT NULL
    )""")

def new_persona(name, familiya, ochestwo):
    with sq.connect("users.db") as con:
        cur = con.cursor()

        cur.execute(f'INSERT INTO users (name, id_space, dolg, chlenskie_vznos_nachislenno,  celevie_vznosi_nachislenno,  chlenskie_vznos_oplacheno, celevie_vznosi_oplacheno,  itog_nachislenno, itog_oplacheno) VALUES("{str(name)} {str(familiya)} {str(ochestwo)}", 0000,  0, 0 , 0, 0 , 0 , 0, 0)')

def main(page: ft.Page):
    page.title = "СНТ Лаунчер"
    page.window_width = 1200
    page.window_height = 700
    page.window_resizable = True
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.theme_mode = ft.ThemeMode.LIGHT
    page.scroll=True
    page.window_center()

    def on_keyboard(e: ft.KeyboardEvent):
        if e.key == "S" and e.ctrl:
            page.show_semantics_debugger = not page.show_semantics_debugger
            page.update()

    def close_dlg(e):
        dlg_modal.open = False
        page.update()

    def save_yes(e):
        page.show_snack_bar(
            ft.SnackBar(ft.Text("Сохранено!"), open=True)
        )
        dlg_modal.open = False
        page.update()

    persona_name = ft.TextField(label="Имя")
    persona_familiya = ft.TextField(label="Фамилия")
    persona_ochestvo = ft.TextField(label="Очество")

    p_n = persona_name.value
    p_f = persona_familiya.value
    p_o = persona_ochestvo.value

    def close_dlg2(e):
        dlg_modal2.open = False
        page.update()

    def add_per_dlg(e):
        ponmega


    dlg_modal2 = ft.AlertDialog(
        modal=True,
        title=ft.Text("Please confirm"),
        content=ft.Text("Do you really want to delete all those files?"),
        actions=[
            persona_name,
            ft.Text(" "),
            persona_familiya,
            ft.Text(" "),
            persona_ochestvo,
            ft.Text(" "),
            ft.ElevatedButton(text="Добавить", on_click=add_per_dlg),
            ft.Text(" "),
            ft.ElevatedButton(text="Отмена", on_click=close_dlg2, autofocus=True)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )


    def open_dlg_modal_new_persona(e):
        page.dialog = dlg_modal2
        dlg_modal2.open = True
        page.update()

    def ponmega():
        if p_n == '' or p_n == ' ' or p_o == '' or p_o == ' ' or p_f == '' or p_f == ' ':
            page.show_snack_bar(
                ft.SnackBar(ft.Text("Одна из строк не заполнена!"), open=False)
            )
        else:
            dlg_modal2.open = False
            page.update()


    page.count = 0

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Вы уверены?"),
        content=ft.Text("Вы уверены что хотите сохранить изменения?"),
        actions=[
            ft.TextButton("Да", on_click=save_yes),
            ft.TextButton("Нет", on_click=close_dlg),
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )

    def open_dlg_modal(e):
        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    txt_number_of_space = ft.TextField(label="Номер", width=400)
    txt_name = ft.TextField(label="Владелец", autofocus=True, width=400)
    txt_space = ft.TextField(label="Участок", width=400, suffix_text="уч.")

    visit_nachisleniya = ft.ElevatedButton("Начисления", on_click=lambda _: page.go("/nachisleniya"))
    visit_pon = ft.ElevatedButton("text", on_click=lambda _: page.go("/pon"))
    txt_number = ft.TextField(value="0", text_align="center", width=60, height=40)

    ychastok = 0

    dolg = 0
    txt_dolg = ft.Text(value=f"Долг: {dolg}₽", size=15, color=ft.colors.RED, weight=ft.FontWeight.W_400)

    chlenskie_vznos_nachislenno = ft.DataCell(ft.TextField(label="Членские взносы начисленно", width=250, height=40, suffix_text="₽", value="0"))
    celevie_vznosi_nachislenno = ft.DataCell(ft.TextField(label="Целевые взносы начисленно", width=250, height=40, suffix_text="₽", value="0"))

    chlenskie_vznos_oplacheno = ft.DataCell(ft.TextField(label="Членские взносы оплачено", width=250, height=40, suffix_text="₽", value="0"))
    celevie_vznosi_oplacheno = ft.DataCell(ft.TextField(label="Целевые взносы оплачено", width=250, height=40, suffix_text="₽", value="0"))



    itog_nachislenno = ft.Text(value="-")
    itog_oplacheno = ft.Text(value="-")

    def sum_btn_func(e):
        a = chlenskie_vznos_nachislenno.content.value
        b = chlenskie_vznos_oplacheno.content.value

        c = celevie_vznosi_nachislenno.content.value
        d = celevie_vznosi_oplacheno.content.value

        txtDolg = txt_dolg

        ca = int(c) + int(a)
        bd = int(b) + int(d)

        itog_nachislenno.value = str(ca)
        itog_oplacheno.value = str(bd)

        txtDolg.value = f"Долг: {ca - bd}₽"
        page.update()

    sum_btn = ft.ElevatedButton("Подсчитать", on_click=sum_btn_func)

    def reset_dolg(e):
        txtDolg = txt_dolg
        txtDolg.value = f"Долг: 0₽"
        page.update()

    btn_reset_dolg = ft.ElevatedButton("обнулить долг", on_click=reset_dolg)

    def minus_click(e):
        txt_number.value = str(int(txt_number.value) - 1)
        page.update()

    def plus_click(e):
        txt_number.value = str(int(txt_number.value) + 1)
        page.update()

    def megapon(e):
        open_dlg_modal_new_persona(e)
        #cur.execute('INSERT INTO users (name, id_space, dolg, chlenskie_vznos_nachislenno,  celevie_vznosi_nachislenno,  chlenskie_vznos_oplacheno, celevie_vznosi_oplacheno,  itog_nachislenno, itog_oplacheno) VALUES("Иван Иванович Иванов", 0000,  0, 0 , 0, 0 , 0 , 0, 0)')
        """
        cl.controls.append(
            ft.Card(
                content=ft.Container(
                    content=ft.Column(
                        [
                            ft.ListTile(
                                leading=ft.Icon(ft.icons.HOME_ROUNDED),
                                title=ft.Text("The Enchanted Nightingale"),
                                subtitle=ft.Text(
                                    "Music by Julie Gable. Lyrics by Sidney Stein."
                                ),
                            ),
                            ft.Row(
                                [ft.TextButton("Открыть", on_click=lambda _: page.go("/pon"))],
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ]
                    ),
                    width=400,
                    height=130,
                    padding=10,
                )
            )
        )
        page.update()
        """

    ponbtn = ft.FloatingActionButton(
        icon=ft.icons.ADD, on_click=megapon, bgcolor=ft.colors.LIME_300
    )

    cl = ft.Column(
        spacing=10,
        height=600,
        width=1200,
        scroll=ft.ScrollMode.ALWAYS,
    )
    #for i in range(0, 50):
    #    cl.controls.append(ft.Text(f"Text line {i}", key=str(i)))

    c1 = ft.Container(
        content=ft.Column(
            controls=[
                txt_name,
                txt_space,
                txt_number_of_space,
            ],
        ),
        height=500,
        width=600,
        alignment=ft.alignment.top_left,
        padding=5,
    )

    c12 = ft.Container(
        content=ft.Row(
            controls=[
                c1,
                #btn_reset_dolg
            ],
        ),
        height=200,
        width=1000,
        alignment=ft.alignment.top_left,
        padding=5,
    )

    c2 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(value="Площадь участка:"),
                ft.IconButton(ft.icons.REMOVE, on_click=minus_click),
                txt_number,
                ft.IconButton(ft.icons.ADD, on_click=plus_click),
            ],
        ),
        height=50,
        width=500,
        alignment=ft.alignment.top_left,
        padding=5,
    )

    c3 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(value="Телефон:"),
                ft.TextField(label="телефон", prefix_text="+7", suffix_icon=ft.icons.LOCAL_PHONE, width=300, height=40)
            ],
        ),
        height=50,
        width=500,
        alignment=ft.alignment.top_left,
        padding=5,
    )

    c4 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(value="E-mail:    "),
                ft.TextField(label="e-mail", suffix_icon=ft.icons.ALTERNATE_EMAIL, width=300, height=40)
            ],
        ),
        height=50,
        width=500,
        alignment=ft.alignment.top_left,
        padding=5,
    )

    c5 = ft.Container(
        content=ft.Row(
            controls=[
                ft.Text(value="Адрес:    "),
                ft.TextField(label="адрес", suffix_icon=ft.icons.HOME_ROUNDED, width=300, height=40)
            ],
        ),
        height=50,
        width=500,
        alignment=ft.alignment.top_left,
        padding=5,
    )

    c = ft.Container(
        content=ft.Column(
            controls=[
                visit_nachisleniya,
                c2,
                ft.Divider(height=9, thickness=1),
                c3,
                c4,
                c5,
                txt_dolg,
            ],
        ),
        height=340,
        width=500,
        border=ft.border.all(1, "grey"),
        alignment=ft.alignment.top_left,
        padding=5,
        border_radius=10,
    )

    qwqwq = ft.Container(
        content=ft.Column(
            controls=[
                c12,
                ft.ElevatedButton("записать", on_click=open_dlg_modal),
                c
            ],
        ),
        alignment=ft.alignment.top_left,
        padding=5,
        height=900,
        width=1000,
        border_radius=10,
    )

    def route_change(route):
        page.views.clear()

        page.views.append(
            ft.View(
                "/menu",
                [
                    ft.AppBar(title=ft.Text('СНТ "мечта" Главное меню'), bgcolor=ft.colors.SURFACE_VARIANT),
                    ponbtn,
                    cl
                ],
            )
        )
        if page.route == "/pon":
            page.views.append(
                ft.View(
                    "/pon",
                    [
                        ft.AppBar(title=ft.Text('СНТ "мечта"'), bgcolor=ft.colors.SURFACE_VARIANT),
                        qwqwq,
                    ],
                )
            )
        if page.route == "/nachisleniya":
            page.views.append(
                ft.View(
                    "/nachisleniya",
                    [
                        ft.AppBar(title=ft.Text("Начисления"), bgcolor=ft.colors.SURFACE_VARIANT),
                        #ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                        ft.DataTable(
                            columns=[
                                ft.DataColumn(ft.Text("Услуга"), numeric=True),
                                ft.DataColumn(ft.Text("Начисоленно"), numeric=True),
                                ft.DataColumn(ft.Text("Оплачено"), numeric=True),
                            ],
                            rows=[
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Членские взносы")),
                                        chlenskie_vznos_nachislenno,
                                        chlenskie_vznos_oplacheno,
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Целевые взносы(по площади)")),
                                        celevie_vznosi_nachislenno,
                                        celevie_vznosi_oplacheno,
                                    ],
                                ),
                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text("Итог")),
                                        ft.DataCell(itog_nachislenno),
                                        ft.DataCell(itog_oplacheno),
                                    ],
                                ),
                            ],
                            width=1200
                        ),
                        sum_btn,
                        ft.ElevatedButton("назад к участку", on_click=lambda _: page.go("/pon")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[0]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)



    page.on_keyboard_event = on_keyboard
    page.add(txt_name, txt_space, txt_number_of_space, c)
    page.update()

ft.app(target=main)