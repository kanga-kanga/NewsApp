import flet as ft
import time
import threading
from database.maindb import DataBase
import database.maindb as ODB


def main(page: ft.Page):
    theme = DataBase().get_themedata_mode()[0][0]
    page.theme_mode = theme
    def toggle_theme_mode(e):
        theme_updated = "dark" if page.theme_mode == "light" else "light"
        DataBase().Update_ThemeData(theme_updated)
        page.theme_mode = "dark" if page.theme_mode == "light" else "light"
        lightMode.icon = (
            ft.icons.WB_SUNNY_OUTLINED if page.theme_mode == "light" else ft.icons.WB_SUNNY
        )
        page.update()
    lightMode = ft.IconButton(
        ft.icons.WB_SUNNY_OUTLINED if page.theme_mode == "light" else ft.icons.WB_SUNNY,
        on_click=toggle_theme_mode,
    )
    # --------------------------- Initialization ----------------------------------------
    home_view = ft.View()
    home_view.route = "/"
    home_view.scroll = ft.ScrollMode.ADAPTIVE
    
    view_details_news = ft.View()
    view_details_news.route = "/news_opened"
    view_details_news.scroll = ft.ScrollMode.ADAPTIVE

    login_view = ft.View()
    login_view.route = "/login_view"
    login_view.scroll = ft.ScrollMode.ADAPTIVE
    login_view.appbar = ft.AppBar(
        title=ft.Text(
            value=""
        )
    )

    about_view = ft.View()
    about_view.route = "/about"
    about_view.appbar = ft.AppBar(
        title=ft.Text(
            value="A Propos",
            style=ft.TextThemeStyle.TITLE_LARGE
        )
    )
    about_view.scroll = ft.ScrollMode.ADAPTIVE

    about_view.controls = [
        ft.Container(
            height=150,
            expand_loose=True,
        ),
        ft.Divider(thickness=2),
        ft.Text(
            value="Bienvenue sur l'application des actualites de l'Universite.",
            size=18,
            color="#2874A6",
            italic=True,
            style=ft.TextThemeStyle.TITLE_MEDIUM
        ),
        ft.Text(
            value = "Nous sommes ravis de vous accueillir sur cette plateforme dédiée à vous tenir informés des dernières nouvelles et événements de notre université.",
            size=18,
            color="#2874A6",
            italic=True,
            style=ft.TextThemeStyle.BODY_MEDIUM
        ),
        ft.Text(
            value = "Nous avons devellopé cette application en vue faciliter l'accès aux informations importantes et pour renforcer la communication au sein de notre communauté universitaire. Nous travaillons en étroite collaboration avec la PRESSE ESI pour vous offrir des informations précises et à jour. Cette application est encore en cours de développement..., et nous travaillons constamment à l'améliorer. Vos retours et suggestions sont précieux pour nous aider à offrir une meilleure expérience utilisateur. N'hésitez pas à nous contacter via WhatsApp pour partager vos idées ou signaler des problèmes.",
            size=14,
            # color="#2874A6",
            style=ft.TextThemeStyle.BODY_MEDIUM,
            italic=True,
            weight=ft.FontWeight.W_300
        ),
        ft.Text(
            value = "Merci de votre soutien ! 🤩",
            size=16,
            color="#2874A6",
            italic=True,
            text_align=ft.TextAlign.CENTER
        ),
        ft.Text(
            value="\u00A9 heritierkangakanga@gmail.com",
            size=11,
            # weight=ft.FontWeight.BOLD
            italic=True
        ),
        ft.Text(
            value="\u00A9 +243825481430",
            size=11,
            # weight=ft.FontWeight.BOLD
            italic=True
        ),
        ft.Text(
            value="\u00A9 KANGA-KANGA MFUNI Heritier, Bouffeur des Code, Dieta Startup, Presse ESI",
            size=11,
            weight=ft.FontWeight.BOLD

        ),
    ]

    # -------------------------- function for change image and updating new image ---------------------------------
    image_geted = ['img.jpg']
    current_index = 0

    def get_image_affiche():
        liste_image = ODB.DataBaseOnlineAgain().get_image_affiche()
        image_geted.clear()
        for i in liste_image :
            image_geted.append(i)

    image = ft.Image(
        src=image_geted[current_index], 
        fit=ft.ImageFit.COVER,
        error_content=ft.CupertinoActivityIndicator(
            radius = 180,
            color = ft.colors.BLUE,
            animating = True,
            ))

    container_image_upd = ft.Container(
            height = 250,
            border_radius=10,
            width=450,
            expand_loose=True,
            content=image,
    )

    def update_image():
        nonlocal current_index
        while True:
            time.sleep(5)
            for_listen_change()
            try :
                current_index = (current_index + 1) % len(image_geted)
                image.src = image_geted[current_index]
                page.update()
            except Exception as e :
                print(e)

    # -------------------------- view of see the details for news ------------------------------------

    def container_news_clicked(e):
        content_news = e.control.data
        view_details_news.appbar = ft.AppBar(
            title=ft.Text()
        )
        c = ft.Container(
            height=250,
            expand_loose=True,
            width=400,
            border_radius=10,
            content = ft.Image(
                src=content_news[0],
                fit=ft.ImageFit.CONTAIN,
                error_content=ft.CupertinoActivityIndicator(
                    radius = 180,
                    color = ft.colors.BLUE,
                    animating = True,
                    expand=True
                )
            ),
            scale=ft.transform.Scale(scale=2),
            animate_scale=ft.animation.Animation(duration=1000, curve=ft.AnimationCurve.BOUNCE_OUT)
    
        
            )
        texte = ft.Text(
            value = content_news[2],
            # style=ft.TextThemeStyle.LABEL_MEDIUM,
            font_family='Times new roman',
            max_lines=150,
            overflow=ft.TextOverflow.ELLIPSIS,
            size=16,
            italic=True,
            opacity=0,
            animate_opacity=ft.animation.Animation(duration=1000)
            # weight=ft.FontWeight.W_400
        )

        view_details_news.controls = [
            ft.Container(
                expand_loose=True,
                content=ft.Text(
                    font_family='RobotoSlab',
                    weight=ft.FontWeight.W_400,
                    max_lines=10,
                    overflow=ft.TextOverflow.ELLIPSIS,
                    value = content_news[1],
                    size=22
                )
            ),
            c,
            ft.Column(
                height=40,
                expand_loose=True,
                alignment=ft.MainAxisAlignment.CENTER,
                controls=[
                    ft.Text(
                        value=(f"{content_news[3]}  {content_news[4]}"),
                        weight=ft.FontWeight.W_100,
                        size=25
                    ),
                ]
            ),
            ft.Container(
                # height=250,
                expand_loose=True,
                # height = 250,
                border_radius=10,
                content=texte
            )

        ]

        page.go("/news_opened")

        def animate():
            # for i in range(20) :
            time.sleep(0.3)
            c.scale = 1 #if c.scale == 1.1 else 1.1
            page.update()
            time.sleep(0.5)
            texte.opacity = 1 if texte.opacity == 0 else 0
            page.update()

        animate()
        
    # -------------------------- content in home view ------------------------------------------------

    def get_news(img_path, title_content, subtitle_content, date, heure):

        image_news = ft.Image(
            # src='assets/img.jpg',
            fit=ft.ImageFit.COVER,
            error_content=ft.CupertinoActivityIndicator(
                            radius = 50,
                            color = ft.colors.BLUE,
                            animating = True,
                            )
        )

        title_news = ft.Text(
            opacity=0,
            animate_opacity=ft.animation.Animation(duration=1000),
            font_family='RobotoSlab',
            weight=ft.FontWeight.W_900,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        subtitle_news = ft.Text(
            opacity=0,
            animate_opacity=ft.animation.Animation(duration=1500),
            style=ft.TextThemeStyle.LABEL_MEDIUM,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        card_content_news = ft.Card(
            content=ft.Container(
                width=400,
                padding=10,
                height=150,
                content=ft.Row(
                    controls=[
                        ft.Container(
                            height=150,
                            width=100,
                            border_radius=10,
                            data = [img_path, title_content, subtitle_content, date, heure],
                            content=image_news,
                            on_click = container_news_clicked
                        ),
                        ft.Column(
                            controls=[
                                ft.Container(
                                    width=200,
                                    height=50,
                                    content=title_news
                                ),
                                ft.Container(
                                    width=200,
                                    height=75,
                                    content = subtitle_news
                                )
                            ]
                        )
                    ]
                )
            )
        )
    
        # get all values for image, title and subtitle

        path_img_source = img_path
        title = title_content
        content = subtitle_content

        # insert that values on correspondantes place
        image_news.src = path_img_source
        title_news.value = title
        subtitle_news.value = content

        # Add card content news in home view
        home_view.controls.append(card_content_news)
        home_view.update()
        time.sleep(0.5)
        title_news.opacity = 1 #if card_content_news.opacity == 0 else 0
        subtitle_news.opacity = 1
        home_view.update()
        page.update()

    home_view.controls = [
        container_image_upd
    ]

    def update_content_news():
        time.sleep(0.1)
        all_news = DataBase().get_data_on_local_database()
        for i in all_news:
            get_news(i[2],  i[1], i[3], i[4], i[5])
    
    def insert_to_home_view(liste_to_insert):

        title = ft.Text(
            value=liste_to_insert[1],
            opacity=0,
            animate_opacity=ft.animation.Animation(duration=1000),
            font_family='RobotoSlab',
            weight=ft.FontWeight.W_900,
            max_lines=2,
            overflow=ft.TextOverflow.ELLIPSIS
        )
        subtitle = ft.Text(
            value=liste_to_insert[3],
            opacity=0,
            animate_opacity=ft.animation.Animation(duration=1500),
            style=ft.TextThemeStyle.LABEL_MEDIUM,
            max_lines=4,
            overflow=ft.TextOverflow.ELLIPSIS
        )

        home_view.controls.insert(1, 
            ft.Card(
                content=ft.Container(
                    width=400,
                    padding=10,
                    height=150,
                    content=ft.Row(
                        controls=[
                            ft.Container(
                                height=150,
                                width=100,
                                border_radius=10,
                                data = [liste_to_insert[2], liste_to_insert[1], liste_to_insert[3], liste_to_insert[4], liste_to_insert[5]],
                                content=ft.Image(
                                    fit = ft.ImageFit.COVER,
                                    src = liste_to_insert[2],
                                    ),
                                on_click = container_news_clicked
                            ),
                            ft.Column(
                                controls=[
                                    ft.Container(
                                        width=200,
                                        height=50,
                                        content=title,
                                    ),
                                    ft.Container(
                                        width=200,
                                        height=75,
                                        content = subtitle,
                                        )
                                    ]
                                )
                            ]
                        )
                    )
                )
            )
        home_view.update()
        page.update()

        # Animate texte for adding (title and subtitle)
        time.sleep(0.5)
        title.opacity = 1
        subtitle.opacity = 1
        home_view.update()
        page.update()
    
    def for_listen_change():
        DataBase().listen_change_in_local_database(insert_to_home_view)


    # ------------------------ Login View --------------------------------------------------
    def Login_view_fonction():
        page.go("/login_view")
  
        def open_submit_button(e):
            if name_field.value != "" and email_field.value != "" and password_field.value != "" :
                time.sleep(0.1)
                submit_button.opacity = 1
        
        name_field = ft.TextField(
            label="Entrer votre nom",
            height=50,
            expand_loose=True,
            on_change=open_submit_button
        )
        email_field = ft.TextField(
            label="Entrer votre adresse email",
            height=50,
            expand_loose=True,
            on_change=open_submit_button
        )
        password_field = ft.TextField(
            label="Creer un mot de pass",
            height=50,
            expand_loose=True,
            on_change=open_submit_button
        )
        
        def send_information_Submit(e):
            request = ODB.DataBaseOnlineAgain().create_a_new_user_compte(email_field.value, name_field.value, password_field.value)
            # time.sleep(5)
            print("On nous as retourne : ", request)

            if request == "NoConnection" :
                snack_bar = ft.SnackBar(
                    content= ft.Text(
                        value="Pas des connexion internet 😥",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    dismiss_direction=ft.DismissDirection.END_TO_START,
                    duration=5000,
                    behavior=ft.SnackBarBehavior.FLOATING
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                login_view.update()
                page.update()

            elif request == "succes" :
                page.go("/")
                page.update()

            else :
                snack_bar = ft.SnackBar(
                    content= ft.Text(
                        value="Pas des connexion internet 😥",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    dismiss_direction=ft.DismissDirection.END_TO_START,
                    duration=5000,
                    behavior=ft.SnackBarBehavior.FLOATING
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                login_view.update()
                page.update()
                
        def have_a_compte(e):
            request = ODB.DataBaseOnlineAgain().have_a_count(email_field.value, password_field.value)
            # time.sleep(5)
            print("Request returned : ", request)
            if request == "Goodpassword" : 
                page.go("/")
                page.update()

            elif request == "Badpassword" :
                snack_bar = ft.SnackBar(
                    content= ft.Text(
                        value="mot de passe incorrect 😥",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    dismiss_direction=ft.DismissDirection.END_TO_START,
                    duration=5000,
                    behavior=ft.SnackBarBehavior.FLOATING
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                login_view.update()
                page.update()

            elif request == "NoEmail" :
                snack_bar = ft.SnackBar(
                    content= ft.Text(
                        value="Pas d'email trouvé 😥",
                        text_align=ft.TextAlign.CENTER,
                    ),
                    dismiss_direction=ft.DismissDirection.END_TO_START,
                    duration=5000,
                    behavior=ft.SnackBarBehavior.FLOATING
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                login_view.update()
                page.update()
        
        submit_button = ft.ElevatedButton(
            text="Valider",
            color=ft.colors.CYAN_400,
            icon=ft.icons.SEND,
            on_click=send_information_Submit,
            # expand_loose=True,
            width=350,
            opacity=0,
            animate_opacity=ft.Animation(1000)
        )
        I_already_have_a_compte = ft.TextButton(
            text="Cliquez ici, après avoir inserer votre email et votre mot de pase si vous avez déjà un compte !",
            icon=ft.icons.LOCK_OPEN,
            icon_color=ft.colors.GREEN,
            on_click=have_a_compte
        )
        lost_password = ft.TextButton(
            text="Cliquez ici, après inserer votre adresse email si vous avez oubliez votre mot de passe !",
            icon=ft.icons.LOCK_CLOCK,
            icon_color=ft.colors.RED
        )
        container_for_login = ft.Container(
            height=550,
            expand_loose=True,
            padding=10,
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_AROUND,
                controls=[
                    name_field,
                    email_field,
                    password_field,
                    ft.Divider(),
                    submit_button,
                    I_already_have_a_compte,
                    lost_password
                ]
            ),
            offset=ft.transform.Offset(x=0, y=10),
            animate_offset=ft.animation.Animation(duration=5000, curve=ft.AnimationCurve.BOUNCE_IN_OUT),
    
        )

        login_view.controls = [
            ft.Container(
                height=50,
                expand_loose=True,
                content=ft.Text(
                    value="Creer un Compte pour Utiliser en toutes Quietudes nos services !",
                    style= ft.TextThemeStyle.TITLE_MEDIUM,
                    color=ft.colors.CYAN_400,
                    max_lines=4,
                    text_align=ft.TextAlign.CENTER
                )
            ),
            container_for_login,
            ft.Text(
                value="Le button valider apparaitra 5 secondes après avoir inserer toutes vos informations",
                max_lines=3,
                size=11,
                font_family='times new roman',
                text_align=ft.TextAlign.CENTER
            ),
            
        ]

        page.update()
        # def animer_le_container () :
        time.sleep(0.2)
        container_for_login.offset = ft.transform.Offset(x=0,y=0) #if container_for_login.offset == ft.transform.Offset(0,0) else ft.transform.Offset(0,0)
        page.update()

        # animer_le_container()

    def open_about_fonction(e):
        page.go('/about')

    # ------------------------ System of navigation ----------------------------------------
    
    home_view.appbar = ft.AppBar(
        title=ft.Text(
            value="Daily News ESI",
            size=24,
            font_family='Arial',
            weight=ft.FontWeight.BOLD
        ),
        center_title=True,
        actions=[
            lightMode
        ],
        leading=ft.IconButton(icon=ft.icons.INFO_OUTLINE, on_click=open_about_fonction),
        adaptive=True
        
    )

    
    def route_change(e):
        user_existe = DataBase().get__email_on_Login_Database()[0][0]
        page.views.clear()
        page.views.append(
        home_view
            )
        if user_existe == "Aucun" :
            Login_view_fonction()
        if page.route == "/news_opened":
            page.views.append(
                view_details_news
            )
        if page.route == "/login_view" :
            page.views.append(
                login_view
            )
        if page.route == "/about" :
            page.views.append(
                about_view
            )
        page.update()

    def view_pop(e):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route)

    threading.Thread(target=get_image_affiche, daemon=True).start()
    threading.Thread(target=update_image, daemon=True).start()
    update_content_news()
    threading.Thread(target=ODB.DataBaseOnline, daemon=True).start()
    
ft.app(target = main)

