import streamlit as st
import bcrypt
from database import c, conn

# ユーザーを追加する関数
def add_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed_password))
    conn.commit()

# 管理者ユーザーを追加する関数
def add_admin_user(username, password):
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, 1)", (username, hashed_password))
    conn.commit()

# ユーザーを認証する関数
def authenticate_user(username, password):
    c.execute("SELECT password FROM users WHERE username = ?", (username,))
    stored_password = c.fetchone()
    if stored_password and bcrypt.checkpw(password.encode('utf-8'), stored_password[0]):
        return True
    return False

# ユーザーが管理者かどうかをチェックする関数
def is_admin(username):
    c.execute("SELECT is_admin FROM users WHERE username = ?", (username,))
    return c.fetchone()[0] == 1

# ログイン画面
def login():
    st.title('掲示板ログイン')

    username = st.text_input('ユーザー名', key='login_username')
    password = st.text_input('パスワード', type='password', key='login_password')
    if st.button('ログイン', key='login_button'):
        if authenticate_user(username, password):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.rerun()
        else:
            st.error('ユーザー名またはパスワードが間違っています')

# サインアップ画面
def signup():
    st.title('新規登録')

    username = st.text_input('ユーザー名', key='signup_username')
    password = st.text_input('パスワード', type='password', key='signup_password')
    if st.button('登録', key='signup_button'):
        add_user(username, password)
        st.success('登録が完了しました。ログインしてください')
        st.session_state['page'] = 'login'
