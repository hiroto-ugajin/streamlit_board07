import streamlit as st
from auth import login, signup, authenticate_user, is_admin
from message_board import message_board
from admin import user_management

# メイン画面
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if 'page' not in st.session_state:
    st.session_state['page'] = 'login'

if st.session_state['logged_in']:
    if st.session_state['page'] == 'message_board':
        message_board()
    elif st.session_state['page'] == 'user_management':
        user_management()
else:
    if st.session_state['page'] == 'login':
        login()
    elif st.session_state['page'] == 'signup':
        signup()

# サイドバーでページを切り替える
if not st.session_state['logged_in']:
    st.sidebar.title('メニュー')
    if st.sidebar.button('ログイン', key='sidebar_login'):
        st.session_state['page'] = 'login'
        st.rerun()
    if st.sidebar.button('新規登録', key='sidebar_signup'):
        st.session_state['page'] = 'signup'
        st.rerun()
else:
    if is_admin(st.session_state['username']):
        st.sidebar.title('管理者メニュー')
        if st.sidebar.button('ユーザー管理', key='sidebar_user_management'):
            st.session_state['page'] = 'user_management'
            st.rerun()

    if st.sidebar.button('掲示板', key='sidebar_message_board'):
        st.session_state['page'] = 'message_board'
        st.rerun()
