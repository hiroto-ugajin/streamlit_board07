import streamlit as st
from database import c, conn
from auth import is_admin

# メッセージを追加する関数
def add_message(username, message):
    c.execute("INSERT INTO messages (username, message) VALUES (?, ?)", (username, message))
    conn.commit()

# メッセージを取得する関数
def get_messages():
    c.execute("SELECT id, username, message, timestamp FROM messages ORDER BY timestamp DESC")
    return c.fetchall()

# メッセージを削除する関数
def delete_message(message_id):
    c.execute("DELETE FROM messages WHERE id = ?", (message_id,))
    conn.commit()

# 掲示板画面
def message_board():
    st.title('掲示板')

    st.write(f'こんにちは、{st.session_state["username"]}さん！')

    message = st.text_area('メッセージ', key='message_area')
    if st.button('投稿', key='post_button'):
        add_message(st.session_state['username'], message)
        st.rerun()

    # メッセージを表示
    messages = get_messages()
    for message_id, username, message, timestamp in messages:
        st.write(f'**{username}**: {message} ({timestamp})')
        if username == st.session_state['username'] or is_admin(st.session_state['username']):
            if st.button('削除', key=f'delete_{message_id}'):
                delete_message(message_id)
                st.rerun()

    if st.button('ログアウト', key='logout_button'):
        st.session_state['logged_in'] = False
        st.rerun()
