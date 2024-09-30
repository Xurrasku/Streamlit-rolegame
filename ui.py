import streamlit as st
from main import *
import time


#API_KEY = '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'

def clear_all(apikey):
    st.session_state['game'] = MyGame(apikey)
    st.session_state['context_created'] = False
    st.session_state['game_started'] = False
    st.session_state['messages'] = []
    st.session_state['actions'] = []


if 'api_connection' not in st.session_state:
    st.session_state['api_connection'] = False

with st.sidebar:
    API_KEY = st.text_input("gorq API Key", type="password")
    print(API_KEY)
    "[Get a gorq API key](https://console.groq.com/keys)"
    st.button(':red[Clear all]', on_click=clear_all, args=(API_KEY,))
    if len(API_KEY) > 50:
        st.session_state['api_connection'] = True



if 'game' not in st.session_state:
    st.session_state['game'] = MyGame(API_KEY)

if 'context_created' not in st.session_state:
    st.session_state['context_created'] = False

if 'game_started' not in st.session_state:
    st.session_state['game_started'] = False

if 'messages' not in st.session_state:
    st.session_state['messages'] = []

if 'actions' not in st.session_state:
    st.session_state['actions'] = []






if not st.session_state['game_started']:

    st.title(":rainbow[Role Game] powered by AI ✨")



    c0 = st.container(height= 60, border = False)

    with c0:
        user_prompt = st.chat_input(placeholder="Describe the context of your story...", disabled= not st.session_state['api_connection'])

    if not st.session_state['api_connection']:
        st.write(':red[***Insert FREE groq API in sidebar***]')

    if user_prompt: #the user has prompted for a new world
        st.session_state['context_created'] = True
        st.session_state['game'].create_context(user_prompt)
        st.session_state['game'].create_character()

    if st.session_state['context_created']: #after refresh but with no new prompt
        context = st.session_state['game'].context
        st.write(context)
        characteristics = st.session_state['game'].caracteristics
        st.header("Let's configurate :blue[your] character :fire:")

        name = st.text_input("What's your name?")
        for char in characteristics:
            selected_option = st.radio("Select a " + char, characteristics[char])
            st.session_state['game'].character[char] = selected_option
        st.session_state['game'].character['name'] = name

        def setstate():
            st.session_state['game_started'] = True


        button = st.button(':rainbow[Start Game]', on_click=setstate)
 
else:
    js = '''
<script>
    var body = window.parent.document.querySelector(".main");
    console.log(body);
    body.scrollTop = 0;
</script>
'''

    st.components.v1.html(js)

    if len(st.session_state['game'].character['name']) > 0:
        st.title(f":rainbow[{st.session_state['game'].character['name']}]'s story ✨")
    else:
        st.title(':rainbow[The story begins]')

    st.session_state['messages'].append(st.session_state['game'].run_game())
    options = st.session_state['game'].generate_options()
    st.session_state['actions'].append(options['actions'])

    
    
    def set_action(i):
        #save the action
        st.session_state['game'].save_actions_choice(st.session_state['actions'][-1][i]['action'])

        #we define which action has been chosen
        for j in range(4):
            st.session_state['actions'][-1][j]['choosen'] = False
        st.session_state['actions'][-1][i]['choosen'] = True

    for i in range(len(st.session_state['messages'])):
        #write model message
        st.write(st.session_state['messages'][i])
        
        #deply buttons
        button0 = st.button(st.session_state['actions'][i][0]['action'], use_container_width=True, on_click=set_action, args=(0,))
        button1 = st.button(st.session_state['actions'][i][1]['action'], use_container_width=True, on_click=set_action, args=(1,))
        button2 = st.button(st.session_state['actions'][i][2]['action'], use_container_width=True, on_click=set_action, args=(2,))
        button3 = st.button(st.session_state['actions'][i][3]['action'], use_container_width=True, on_click=set_action, args=(3,))


