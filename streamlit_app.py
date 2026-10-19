
import streamlit as st

import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "campusos.db"


def get_db():
    connection = sqlite3.connect(
        DATABASE,
        timeout=10,
    )
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def get_dashboard_stats():
    connection = get_db()
    try:
        return {
            "students": connection.execute(
                "SELECT COUNT(*) FROM users"
            ).fetchone()[0],
            "tasks": connection.execute(
                "SELECT COUNT(*) FROM tasks"
            ).fetchone()[0],
            "resources": connection.execute(
                "SELECT COUNT(*) FROM pdfs"
            ).fetchone()[0],
            "discussions": connection.execute(
                "SELECT COUNT(*) FROM discussions"
            ).fetchone()[0],
            "groups": connection.execute(
                "SELECT COUNT(*) FROM study_groups"
            ).fetchone()[0],
            "quizzes": connection.execute(
                "SELECT COUNT(*) FROM quiz_attempts"
            ).fetchone()[0],
        }
    finally:
        connection.close()


st.set_page_config(
    page_title="CampusOS | Student Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- SESSION STATE ----------
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# ---------- SIDEBAR ----------
with st.sidebar:
    st.title("🎓 CampusOS")
    st.caption("Your university, connected.")

    st.divider()

    pages = [
        "Dashboard",
        "Study Planner",
        "PDF Library",
        "Discussions",
        "Study Groups",
        "AI Study Assistant",
        "AI Quiz Generator",
    ]

    for page in pages:
        if st.button(
            page,
            key=f"nav_{page}",
            use_container_width=True,
            type="primary" if st.session_state.page == page else "secondary",
        ):
            st.session_state.page = page
            st.rerun()

    st.divider()
    st.caption("CampusOS • Student Learning Platform")

# ---------- MAIN CONTENT ----------
page = st.session_state.page


if page == "Dashboard":
    st.title("Welcome to CampusOS 👋")
    st.write(
        "Your space to learn, share resources and study together."
    )

    try:
        stats = get_dashboard_stats()

        st.subheader("Campus Overview")

        col1, col2, col3 = st.columns(3)
        col1.metric("Registered Students", stats["students"])
        col2.metric("Study Tasks", stats["tasks"])
        col3.metric("PDF Resources", stats["resources"])

        col4, col5, col6 = st.columns(3)
        col4.metric("Discussions", stats["discussions"])
        col5.metric("Study Groups", stats["groups"])
        col6.metric("Quiz Attempts", stats["quizzes"])

    except sqlite3.Error:
        st.error(
            "Could not read the CampusOS database. "
            "Check that campusos.db is in the project folder."
        )

    st.divider()
    st.subheader("Explore CampusOS")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📅 Study Planner", use_container_width=True):
            st.session_state.page = "Study Planner"
            st.rerun()

        if st.button("💬 Discussions", use_container_width=True):
            st.session_state.page = "Discussions"
            st.rerun()

        if st.button(
            "🤖 AI Study Assistant",
            use_container_width=True,
        ):
            st.session_state.page = "AI Study Assistant"
            st.rerun()

    with col2:
        if st.button("📚 PDF Library", use_container_width=True):
            st.session_state.page = "PDF Library"
            st.rerun()

        if st.button("👥 Study Groups", use_container_width=True):
            st.session_state.page = "Study Groups"
            st.rerun()

        if st.button(
            "📝 AI Quiz Generator",
            use_container_width=True,
        ):
            st.session_state.page = "AI Quiz Generator"
            st.rerun()


elif page == "Study Planner":
    st.title("📅 Study Planner")
    st.info("Next: connect your existing task database and planner features.")

elif page == "PDF Library":
    st.title("📚 PDF Library")
    st.info("Next: connect PDF uploads, search and downloads.")

elif page == "Discussions":
    st.title("💬 Discussions")
    st.info("Next: connect discussions and replies.")

elif page == "Study Groups":
    st.title("👥 Study Groups")
    st.info("Next: connect group creation, membership and messages.")

elif page == "AI Study Assistant":
    st.title("🤖 AI Study Assistant")
    st.info("Next: connect PDF question answering to a cloud-accessible AI service.")

elif page == "AI Quiz Generator":
    st.title("📝 AI Quiz Generator")
    st.info("Next: connect quiz generation, attempts and scoring.")
