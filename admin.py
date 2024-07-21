import streamlit as st
from database import c, conn

# ユーザーを削除する関数
def delete_user(user_id):
    c.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()

# ユーザー管理画面（管理者用）
def user_management():
    st.title('ユーザー管理（管理者用）')

    c.execute("SELECT id, username FROM users")
    users = c.fetchall()
    for user_id, username in users:
        st.write(f'ユーザー名: {username}')
        if st.button('削除', key=f'delete_user_{user_id}'):
            delete_user(user_id)
            st.rerun()
