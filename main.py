from flet import *
import google.generativeai as gene

############# gemini ai code ############

gene.configure(api_key='AIzaSyDZ03TfP3k5YrulLWOV5rE5NhFZvbYbitE')

model = gene.GenerativeModel('gemini-pro')
def display_message(chat_container, role, message_text):
    if role == 'user':
        role_color = colors.RED_300
        role_text = 'User'
    else:
        role_color = colors.BLUE_300
        role_text = 'Gemini-AI-'
    
    message_area = SelectionArea(
        content=Column([
            Text(role_text, weight='bold', color=role_color),
            Text(message_text)
        ])
    )
    chat_container.controls.append(message_area)
    chat_container.update()

def update_chat(page, chat_container, chat, prompt):
    display_message(chat_container, 'user', prompt)
    
    response = chat.send_message(prompt)

    display_message(chat_container, 'bot', response.parts[0].text)
    page.update()
##########################  login page  ##############

def main(page: Page):
    page.window_width = 400
    page.window_height = 700
    page.bgcolor = colors.WHITE
    page.title = 'First App'
    page.horizontal_alignment = "center"
    page.vertical_alignment = "center"
    page.bgcolor=Theme
    
    def go_home(e):
        page.clean()
        main(page)
    ####################appbar######################
    page.appbar = AppBar(
        bgcolor=colors.BLUE_ACCENT_200,
        title=Text('Gemini-Pro'),
        center_title=True,
        leading=Icon(icons.HOME  ),
        leading_width=40,
        actions=[
            IconButton(icons.NOTIFICATIONS, disabled=False),
            PopupMenuButton(
                items=[
                    PopupMenuItem('home' , on_click=go_home),
                    PopupMenuItem('login'),
                    PopupMenuItem('exit')
                ]
            )
        ]
    )

    #####################center############
    image = Image(src="ai.png", width=200, height=170)
    text = Text('Welcome To My App ', color=colors.random_color, font_family='Elephant', size=20 )
    
    #in1 = TextField(label='Nom dutilisateur', icon=icons.ADMIN_PANEL_SETTINGS_SHARP)
    in2 = TextField(label='Activation code', password=True, can_reveal_password=True, icon=icons.PASSWORD)
    
    def navigate_to_ai_page(e):
        if  in2.value == '2112':
            page.clean()
            ai_chat_page(page)
        else:
            error = Text('Error: try again', color=colors.RED)
            #in1.value = ''
            in2.value = ''
            page.clean()
            page.add(image, text , in2, b1, error)
            page.update()

    b1 = ElevatedButton('Enter /الدخول ', color=colors.BLUE_100, bgcolor=colors.GREEN, on_click=navigate_to_ai_page)
    
    page.navigation_bar = CupertinoNavigationBar (
        bgcolor=colors.BLUE_ACCENT_200,
        inactive_color=colors.BLACK26 ,
        destinations=[
            NavigationDestination(icon=icons.CONTACT_MAIL , label='Email'),
            NavigationDestination(icon=icons.FACEBOOK , label='Facebook'),
            NavigationDestination(icon=icons.EXIT_TO_APP , label='Exit')
        ]
    )

    page.add(image, text, in2, b1)
    page.update()

 ################### chat_page for gemini  ########

def ai_chat_page(page: Page):
    page.title = 'IMAD FIRST APP'
    page.window_width = 400
    page.window_height = 700

    if not hasattr(page, 'chat'):
        page.chat = model.start_chat(history=[])
    
    user_input = TextField(hint_text='Ecrit...', expand=True)
    chat_container = Column(scroll='always', expand=True, auto_scroll=True)
    
    def send_message(e):
        if user_input.value.strip() != "":
            update_chat(page, chat_container, page.chat, user_input.value)
            user_input.value = ''
            page.update()
    
    send_button = ElevatedButton(text='Send', on_click=send_message)
    
    page.add(
        chat_container,
        Row([
            user_input,
            send_button
        ])
    )
    page.update()

app(target=main)
