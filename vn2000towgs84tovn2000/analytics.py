import sqlite3
import streamlit as st

def init_analytics():
    conn = sqlite3.connect("analytics.db", check_same_thread=False)
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS visits (ts TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS likes (id INTEGER PRIMARY KEY, count INTEGER)")
    c.execute("INSERT OR IGNORE INTO likes (id, count) VALUES (1, 0)")
    conn.commit()

    c.execute("INSERT INTO visits (ts) VALUES (datetime('now','localtime'))")
    conn.commit()

    c.execute("SELECT COUNT(*) FROM visits")
    visit_count = c.fetchone()[0]

    c.execute("SELECT count FROM likes WHERE id=1")
    like_count = c.fetchone()[0]

    st.sidebar.markdown("## 📊 Thống kê sử dụng")
    st.sidebar.markdown(f"- 🔍 **Lượt truy cập:** `{visit_count}`")
    st.sidebar.markdown(f"- 👍 **Lượt thích:** `{like_count}`")

    if st.sidebar.button("👍 Thích ứng dụng này"):
        like_count += 1
        c.execute("UPDATE likes SET count = ? WHERE id = 1", (like_count,))
        conn.commit()
        st.sidebar.success("💖 Cảm ơn bạn đã thích!")
        st.sidebar.markdown(f"- 👍 **Lượt thích:** `{like_count}`")
