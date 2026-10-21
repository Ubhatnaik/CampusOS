
import re
import sqlite3
from datetime import date
from pathlib import Path

import requests
import fitz

import streamlit as st
from werkzeug.security import check_password_hash, generate_password_hash

BASE_DIR = Path(__file__).resolve().parent
DATABASE = BASE_DIR / "campusos.db"


st.set_page_config(
    page_title="CampusOS | Student Hub",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded",
)



st.markdown(
    """
    <style>
    /* ==========================================
       CAMPUSOS — COMPLETE VISUAL THEME
       ========================================== */

    :root {
        --navy: #172554;
        --navy-dark: #111C36;
        --blue: #2563EB;
        --blue-hover: #1D4ED8;
        --page-bg: #F3F6FC;
        --card-bg: #FFFFFF;
        --text-main: #1E293B;
        --text-muted: #64748B;
        --border: #DCE4F0;
    }

    /* MAIN PAGE */
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"] {
        background: var(--page-bg) !important;
        color: var(--text-main) !important;
    }

    [data-testid="stMain"] .block-container {
        max-width: 1350px;
        padding: 2rem 2.5rem 3rem;
    }

    /* TOP HEADER — remove black strip */
    [data-testid="stHeader"] {
        background: var(--page-bg) !important;
        color: var(--navy) !important;
    }

    [data-testid="stToolbar"] {
        background: transparent !important;
    }

    [data-testid="stHeader"] button {
        color: var(--navy) !important;
    }

    [data-testid="stHeader"] svg {
        fill: var(--navy) !important;
        color: var(--navy) !important;
    }

    [data-testid="stDecoration"] {
        background: var(--page-bg) !important;
    }

    /* MAIN HEADINGS */
    [data-testid="stMain"] h1,
    [data-testid="stMain"] h2,
    [data-testid="stMain"] h3,
    [data-testid="stMain"] h4 {
        color: var(--navy) !important;
        font-weight: 750 !important;
    }

    [data-testid="stMain"] p,
    [data-testid="stMain"] li,
    [data-testid="stMain"] label {
        color: var(--text-main);
    }

    [data-testid="stMain"] [data-testid="stMarkdownContainer"] {
        color: var(--text-main);
    }

    [data-testid="stMain"] [data-testid="stCaptionContainer"],
    [data-testid="stMain"] [data-testid="stCaptionContainer"] p {
        color: var(--text-muted) !important;
    }

    /* SIDEBAR */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {
        background: var(--navy-dark) !important;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] strong {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] [data-testid="stCaptionContainer"],
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        color: #CBD5E1 !important;
    }

    [data-testid="stSidebar"] hr {
        border-color: #34415B !important;
    }

    /* SIDEBAR NAVIGATION BUTTONS */
    [data-testid="stSidebar"] .stButton > button {
        background: #1B2945 !important;
        color: #F8FAFC !important;
        border: 1px solid #344563 !important;
        border-radius: 10px !important;
        min-height: 44px;
        font-weight: 600;
        box-shadow: none !important;
    }

    [data-testid="stSidebar"] .stButton > button p {
        color: #F8FAFC !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background: #293B5D !important;
        color: #FFFFFF !important;
        border-color: #60A5FA !important;
    }

    [data-testid="stSidebar"] .stButton > button[kind="primary"],
    [data-testid="stSidebar"] .stButton > button[kind="primary"] p {
        background: var(--blue) !important;
        color: #FFFFFF !important;
        border-color: #60A5FA !important;
    }

    /* DASHBOARD METRIC CARDS */
    [data-testid="stMetric"] {
        background: var(--card-bg) !important;
        border: 1px solid var(--border) !important;
        border-radius: 15px !important;
        padding: 20px !important;
        box-shadow: 0 3px 12px rgba(23, 37, 84, 0.05);
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] p {
        color: var(--text-muted) !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] div {
        color: var(--navy) !important;
        font-weight: 750 !important;
    }

    /* CARDS AND CONTAINERS */
    [data-testid="stVerticalBlockBorderWrapper"] {
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
    }

    /* FORMS */
    [data-testid="stForm"] {
        background: #FFFFFF !important;
        border: 1px solid var(--border) !important;
        border-radius: 14px !important;
        padding: 22px !important;
    }

    /* INPUT FIELDS */
    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input,
    .stDateInput input {
        background: #FFFFFF !important;
        color: #1E293B !important;
        border: 1px solid #CBD5E1 !important;
        border-radius: 9px !important;
        -webkit-text-fill-color: #1E293B !important;
    }

    .stTextInput input::placeholder,
    .stTextArea textarea::placeholder {
        color: #94A3B8 !important;
        -webkit-text-fill-color: #94A3B8 !important;
    }

    /* DROPDOWNS */
    [data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border-color: #CBD5E1 !important;
        border-radius: 9px !important;
    }

    /* MAIN PAGE BUTTONS */
    [data-testid="stMain"] .stButton > button,
    [data-testid="stMain"] .stFormSubmitButton > button {
        background: #FFFFFF !important;
        color: var(--blue) !important;
        border: 1px solid #B8CCF2 !important;
        border-radius: 9px !important;
        min-height: 40px;
        font-weight: 600;
        box-shadow: none !important;
    }

    [data-testid="stMain"] .stButton > button p,
    [data-testid="stMain"] .stFormSubmitButton > button p {
        color: var(--blue) !important;
    }

    [data-testid="stMain"] .stButton > button:hover,
    [data-testid="stMain"] .stFormSubmitButton > button:hover {
        background: #EFF6FF !important;
        border-color: #60A5FA !important;
    }

    [data-testid="stMain"] .stButton > button[kind="primary"],
    [data-testid="stMain"] .stFormSubmitButton > button[kind="primary"] {
        background: var(--blue) !important;
        color: #FFFFFF !important;
        border-color: var(--blue) !important;
    }

    [data-testid="stMain"] .stButton > button[kind="primary"] p,
    [data-testid="stMain"] .stFormSubmitButton > button[kind="primary"] p {
        color: #FFFFFF !important;
    }

    /* RADIO BUTTONS AND CHECKBOXES */
    [data-testid="stMain"] [data-testid="stRadio"] label,
    [data-testid="stMain"] [data-testid="stCheckbox"] label {
        color: var(--text-main) !important;
    }

    /* DIVIDERS AND LINKS */
    [data-testid="stMain"] hr {
        border-color: var(--border) !important;
    }

    [data-testid="stMain"] a {
        color: var(--blue) !important;
    }

    /* ALERTS */
    [data-testid="stAlert"] {
        border-radius: 10px;
    }

    /* TABLES */
    [data-testid="stMain"] [data-testid="stDataFrame"] {
        border: 1px solid var(--border);
        border-radius: 10px;
    }
    
    
/* ===== CampusOS: Compact dashboard and readable text ===== */

/* Reduce overall spacing */
[data-testid="stMain"] .block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 1rem !important;
    max-width: 1200px;
}

/* Smaller headings */
[data-testid="stMain"] h1 {
    font-size: 1.8rem !important;
    margin-bottom: 0.35rem !important;
}

[data-testid="stMain"] h2 {
    font-size: 1.35rem !important;
    margin-top: 0.5rem !important;
    margin-bottom: 0.4rem !important;
}

[data-testid="stMain"] h3 {
    font-size: 1.05rem !important;
    margin-bottom: 0.3rem !important;
}

/* Reduce gaps between Streamlit elements */
[data-testid="stMain"] [data-testid="stVerticalBlock"] {
    gap: 0.65rem;
}

/* Compact metric cards */
[data-testid="stMain"] [data-testid="stMetric"] {
    background: #FFFFFF !important;
    border: 1px solid #DCE4F0 !important;
    border-radius: 10px !important;
    padding: 10px 12px !important;
    gap: 3px !important;
}

[data-testid="stMain"] [data-testid="stMetricLabel"],
[data-testid="stMain"] [data-testid="stMetricLabel"] p {
    color: #475569 !important;
    font-size: 0.82rem !important;
}

[data-testid="stMain"] [data-testid="stMetricValue"] {
    color: #172554 !important;
    font-size: 1.5rem !important;
}

/* Compact bordered profile and task cards */
[data-testid="stMain"] [data-testid="stVerticalBlockBorderWrapper"] {
    border: 1px solid #DCE4F0 !important;
    border-radius: 10px !important;
    padding: 0.65rem 0.8rem !important;
    background-color: #FFFFFF !important;
}

/* Improve normal text contrast */
[data-testid="stMain"] p,
[data-testid="stMain"] label,
[data-testid="stMain"] li,
[data-testid="stMain"] [data-testid="stMarkdownContainer"] {
    color: #1E293B;
}

/* Make captions readable */
[data-testid="stMain"] [data-testid="stCaptionContainer"],
[data-testid="stMain"] [data-testid="stCaptionContainer"] p {
    color: #475569 !important;
    font-size: 0.82rem !important;
}

/* Make white text visible on dark buttons and sidebar */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
[data-testid="stSidebar"] [data-testid="stCaptionContainer"] {
    color: #FFFFFF !important;
}

[data-testid="stSidebar"] .stButton button[kind="primary"] p,
[data-testid="stSidebar"] .stButton button[kind="primary"] span {
    color: #FFFFFF !important;
}

/* Ensure primary buttons have strong contrast */
[data-testid="stMain"] .stButton button[kind="primary"],
[data-testid="stMain"] .stFormSubmitButton button[kind="primary"] {
    background-color: #1D4ED8 !important;
    border-color: #1D4ED8 !important;
    color: #FFFFFF !important;
}

/* Keep button text visible */
[data-testid="stMain"] .stButton button,
[data-testid="stMain"] .stFormSubmitButton button {
    font-weight: 600 !important;
}

/* Reduce divider spacing */
[data-testid="stMain"] hr {
    margin-top: 0.6rem !important;
    margin-bottom: 0.6rem !important;
}


    </style>
    """,
    unsafe_allow_html=True,
)



def initialize_database():
    """Create CampusOS tables if they do not already exist."""
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.execute("PRAGMA foreign_keys = ON")

    try:
        connection.executescript("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE COLLATE NOCASE,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                registration_id TEXT,
                bio TEXT,
                department TEXT,
                semester TEXT
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                due_date TEXT,
                completed INTEGER DEFAULT 0,
                user_id INTEGER REFERENCES users(id),
                priority TEXT DEFAULT 'Medium',
                subject TEXT DEFAULT ''
            );

            CREATE TABLE IF NOT EXISTS pdfs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                filename TEXT NOT NULL,
                uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                title TEXT,
                subject TEXT,
                description TEXT,
                stored_filename TEXT,
                uploader_id INTEGER,
                semester TEXT,
                category TEXT NOT NULL DEFAULT 'Other'
            );

            CREATE TABLE IF NOT EXISTS discussions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                body TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                category TEXT NOT NULL DEFAULT 'General Questions',
                FOREIGN KEY (author_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS replies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                discussion_id INTEGER NOT NULL,
                body TEXT NOT NULL,
                author_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (discussion_id) REFERENCES discussions(id),
                FOREIGN KEY (author_id) REFERENCES users(id)
            );

            CREATE TABLE IF NOT EXISTS study_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                subject TEXT,
                creator_id INTEGER NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS group_members (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                joined_at TEXT DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(group_id, user_id)
            );

            CREATE TABLE IF NOT EXISTS group_messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                group_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                message TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS quiz_attempts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                pdf_id INTEGER NOT NULL,
                score INTEGER NOT NULL DEFAULT 0,
                total_questions INTEGER NOT NULL DEFAULT 0,
                submitted INTEGER NOT NULL DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS quiz_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                attempt_id INTEGER NOT NULL,
                question TEXT NOT NULL,
                option_a TEXT NOT NULL,
                option_b TEXT NOT NULL,
                option_c TEXT NOT NULL,
                option_d TEXT NOT NULL,
                correct_answer TEXT NOT NULL,
                explanation TEXT NOT NULL,
                selected_answer TEXT,
                FOREIGN KEY (attempt_id)
                    REFERENCES quiz_attempts(id)
            );
        """)
        connection.commit()
    finally:
        connection.close()


def get_db():
    connection = sqlite3.connect(DATABASE, timeout=10)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


initialize_database()



def table_columns(connection, table_name):
    return {
        row["name"]
        for row in connection.execute(
            f"PRAGMA table_info({table_name})"
        )
    }


def get_dashboard_stats(user_id):
    connection = get_db()

    try:
        tables = {
            row["name"]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }

        counts = {}

        for key, table in [
            ("students", "users"),
            ("tasks", "tasks"),
            ("resources", "pdfs"),
            ("discussions", "discussions"),
            ("groups", "study_groups"),
            ("quizzes", "quiz_attempts"),
        ]:
            if table in tables:
                counts[key] = connection.execute(
                    f"SELECT COUNT(*) FROM {table}"
                ).fetchone()[0]
            else:
                counts[key] = 0

        # Task deadlines for the currently logged-in student
        if "tasks" in tables:
            today = date.today().isoformat()

            
            overdue = connection.execute(
                """
                SELECT COUNT(*) FROM tasks
                WHERE user_id = ?
                  AND COALESCE(completed, 0) = 0
                  AND due_date IS NOT NULL
                  AND TRIM(due_date) != ''
                  AND substr(TRIM(due_date), 1, 10) < ?
                """,
                (user_id, today),
            ).fetchone()[0]

            upcoming = connection.execute(
                """
                SELECT COUNT(*) FROM tasks
                WHERE user_id = ?
                  AND COALESCE(completed, 0) = 0
                  AND due_date IS NOT NULL
                  AND TRIM(due_date) != ''
                  AND substr(TRIM(due_date), 1, 10) >= ?
                """,
                (user_id, today),
            ).fetchone()[0]


            counts["overdue"] = overdue
            counts["upcoming"] = upcoming
        else:
            counts["overdue"] = 0
            counts["upcoming"] = 0

        return counts

    finally:
        connection.close()



def register_user(name, registration_id, password):
    connection = get_db()

    try:
        columns = table_columns(connection, "users")

        required = {"name", "registration_id", "password_hash"}

        if not required.issubset(columns):
            return False, (
                "The users table is missing required columns. "
                "Your database has not been changed."
            )

        existing = connection.execute(
            """
            SELECT id FROM users
            WHERE registration_id = ? COLLATE NOCASE
            """,
            (registration_id,),
        ).fetchone()

        if existing:
            return False, (
                "This registration ID is already registered. "
                "Please log in instead."
            )

        password_hash = generate_password_hash(password)

        if "email" in columns:
            connection.execute(
                """
                INSERT INTO users
                    (name, email, password_hash, registration_id)
                VALUES (?, ?, ?, ?)
                """,
                (
                    name,
                    f"{registration_id}@campusos.invalid",
                    password_hash,
                    registration_id,
                ),
            )
        else:
            connection.execute(
                """
                INSERT INTO users
                    (name, registration_id, password_hash)
                VALUES (?, ?, ?)
                """,
                (name, registration_id, password_hash),
            )

        connection.commit()

        return True, "Account created! You can now log in."

    except sqlite3.Error as error:
        connection.rollback()
        return False, f"Could not create account: {error}"

    finally:
        connection.close()


def authenticate_user(registration_id, password):
    connection = get_db()

    try:
        columns = table_columns(connection, "users")

        required = {
            "id",
            "name",
            "registration_id",
            "password_hash",
        }

        if not required.issubset(columns):
            return None

        user = connection.execute(
            """
            SELECT id, name, registration_id, password_hash
            FROM users
            WHERE registration_id = ? COLLATE NOCASE
            """,
            (registration_id,),
        ).fetchone()

        if user and check_password_hash(
            user["password_hash"], password
        ):
            return {
                "id": user["id"],
                "name": user["name"],
                "registration_id": user["registration_id"],
            }

        return None

    finally:
        connection.close()


def show_auth_page():
    st.title("🎓 Welcome to CampusOS")
    st.write("Sign in or create your student account.")

    login_tab, register_tab = st.tabs(
        ["Log in", "Create account"]
    )

    with login_tab:
        with st.form("login_form"):
            registration_id = st.text_input(
                "Registration ID"
            ).strip().upper()

            password = st.text_input(
                "Password", type="password"
            )

            submitted = st.form_submit_button(
                "Log in", use_container_width=True
            )

        if submitted:
            if not registration_id or not password:
                st.error(
                    "Enter both your registration ID and password."
                )
            else:
                try:
                    user = authenticate_user(
                        registration_id, password
                    )

                    if user:
                        st.session_state.user = user
                        st.session_state.page = "Dashboard"
                        st.rerun()
                    else:
                        st.error(
                            "Incorrect registration ID or password."
                        )

                except sqlite3.Error as error:
                    st.error(f"Database error: {error}")

    with register_tab:
        with st.form("register_form"):
            name = st.text_input(
                "Full name", max_chars=100
            ).strip()

            registration_id = st.text_input(
                "Choose registration ID", max_chars=50
            ).strip().upper()

            password = st.text_input(
                "Create password (at least 8 characters)",
                type="password",
            )

            confirm_password = st.text_input(
                "Confirm password", type="password"
            )

            submitted = st.form_submit_button(
                "Create account", use_container_width=True
            )

        if submitted:
            if not name or not registration_id or not password:
                st.error("Please complete all fields.")

            elif not re.fullmatch(
                r"[A-Z0-9][A-Z0-9/_-]{1,49}",
                registration_id,
            ):
                st.error(
                    "Registration ID must be 2–50 characters "
                    "and use letters, numbers, /, _ or -."
                )

            elif len(password) < 8:
                st.error(
                    "Password must contain at least 8 characters."
                )

            elif password != confirm_password:
                st.error("The passwords do not match.")

            else:
                try:
                    success, message = register_user(
                        name, registration_id, password
                    )

                    if success:
                        st.success(message)
                    else:
                        st.error(message)

                except sqlite3.Error as error:
                    st.error(f"Database error: {error}")



def show_planner(user_id):
    st.title("📅 Study Planner")
    st.write("Add tasks, track deadlines, and manage your studies.")

    connection = get_db()

    try:
        columns = table_columns(connection, "tasks")

        required = {
            "id", "title", "due_date", "completed",
            "user_id", "priority", "subject",
        }

        if not required.issubset(columns):
            st.error(
                "The tasks table is missing required columns. "
                "Your database has not been changed."
            )
            return

        # Add a task
        with st.form("add_task_form", clear_on_submit=True):
            st.subheader("➕ Add a study task")

            title = st.text_input("Task title", max_chars=200)
            col1, col2, col3 = st.columns(3)

            with col1:
                subject = st.text_input("Subject", max_chars=100)

            with col2:
                due_date = st.date_input("Due date", value=date.today())

            with col3:
                priority = st.selectbox(
                    "Priority", ["Low", "Medium", "High"], index=1
                )

            add_clicked = st.form_submit_button(
                "Add task", use_container_width=True
            )

        if add_clicked:
            if not title.strip():
                st.error("Please enter a task title.")
            else:
                connection.execute(
                    """
                    INSERT INTO tasks
                        (title, due_date, completed, user_id, priority, subject)
                    VALUES (?, ?, 0, ?, ?, ?)
                    """,
                    (
                        title.strip(), due_date.isoformat(),
                        user_id, priority, subject.strip(),
                    ),
                )
                connection.commit()
                st.success("Task added successfully.")
                st.rerun()

        tasks = connection.execute(
            """
            SELECT id, title, due_date, completed, priority, subject
            FROM tasks
            WHERE user_id = ?
            ORDER BY completed ASC, due_date ASC, id DESC
            """,
            (user_id,),
        ).fetchall()

        st.divider()

        if not tasks:
            st.info("No tasks yet. Add your first task above.")
            return

        today = date.today()
        completed_tasks = [t for t in tasks if t["completed"]]
        pending_tasks = [t for t in tasks if not t["completed"]]

        overdue_tasks = []
        upcoming_tasks = []

        for task in pending_tasks:
            try:
                deadline = date.fromisoformat(str(task["due_date"])[:10])
                if deadline < today:
                    overdue_tasks.append(task)
                else:
                    upcoming_tasks.append(task)
            except (ValueError, TypeError):
                upcoming_tasks.append(task)

        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Tasks", len(tasks))
        col2.metric("Upcoming", len(upcoming_tasks))
        col3.metric("Overdue", len(overdue_tasks))
        col4.metric("Completed", len(completed_tasks))

        completed_count = len(completed_tasks)
        st.progress(
            completed_count / len(tasks),
            text=f"Progress: {completed_count} of {len(tasks)} tasks completed",
        )

        def render_task(task):
            with st.container(border=True):
                left, right = st.columns([3, 1])

                with left:
                    if task["completed"]:
                        st.markdown(f"~~**{task['title']}**~~")
                        st.success("Completed")
                    else:
                        st.markdown(f"**{task['title']}**")

                        try:
                            deadline = date.fromisoformat(
                                str(task["due_date"])[:10]
                            )
                            if deadline < today:
                                st.error("🔴 OVERDUE")
                            elif deadline == today:
                                st.warning("🟠 DUE TODAY")
                            else:
                                st.info("🟢 UPCOMING")
                        except (ValueError, TypeError):
                            st.caption("Deadline not set")

                    details = []
                    if task["subject"]:
                        details.append(f"Subject: {task['subject']}")
                    if task["due_date"]:
                        details.append(f"Deadline: {task['due_date']}")
                    details.append(
                        f"Priority: {task['priority'] or 'Medium'}"
                    )
                    st.caption(" • ".join(details))

                with right:
                    if task["completed"]:
                        if st.button(
                            "Undo", key=f"undo_{task['id']}",
                            use_container_width=True,
                        ):
                            connection.execute(
                                """
                                UPDATE tasks SET completed = 0
                                WHERE id = ? AND user_id = ?
                                """,
                                (task["id"], user_id),
                            )
                            connection.commit()
                            st.rerun()
                    elif st.button(
                        "Complete", key=f"complete_{task['id']}",
                        use_container_width=True,
                    ):
                        connection.execute(
                            """
                            UPDATE tasks SET completed = 1
                            WHERE id = ? AND user_id = ?
                            """,
                            (task["id"], user_id),
                        )
                        connection.commit()
                        st.rerun()

                    if st.button(
                        "✏️ Edit", key=f"edit_{task['id']}",
                        use_container_width=True,
                    ):
                        st.session_state["editing_task_id"] = task["id"]

                    if st.button(
                        "Delete", key=f"delete_{task['id']}",
                        use_container_width=True,
                    ):
                        connection.execute(
                            "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                            (task["id"], user_id),
                        )
                        connection.commit()

                        if st.session_state.get("editing_task_id") == task["id"]:
                            st.session_state.pop("editing_task_id", None)

                        st.rerun()

                # Edit form for the selected task
                if st.session_state.get("editing_task_id") == task["id"]:
                    with st.form(f"edit_task_form_{task['id']}"):
                        st.subheader("Edit task")

                        edited_title = st.text_input(
                            "Task title", value=task["title"]
                        )
                        edited_subject = st.text_input(
                            "Subject", value=task["subject"] or ""
                        )

                        try:
                            current_date = date.fromisoformat(
                                str(task["due_date"])[:10]
                            )
                        except (ValueError, TypeError):
                            current_date = today

                        edited_date = st.date_input(
                            "Due date", value=current_date,
                            key=f"edit_date_{task['id']}",
                        )
                        priorities = ["Low", "Medium", "High"]
                        current_priority = task["priority"] or "Medium"
                        priority_index = (
                            priorities.index(current_priority)
                            if current_priority in priorities else 1
                        )
                        edited_priority = st.selectbox(
                            "Priority", priorities,
                            index=priority_index,
                            key=f"edit_priority_{task['id']}",
                        )

                        save_edit = st.form_submit_button("Save changes")
                        cancel_edit = st.form_submit_button("Cancel")

                        if save_edit:
                            if not edited_title.strip():
                                st.error("Task title cannot be empty.")
                            else:
                                connection.execute(
                                    """
                                    UPDATE tasks
                                    SET title = ?, subject = ?, due_date = ?,
                                        priority = ?
                                    WHERE id = ? AND user_id = ?
                                    """,
                                    (
                                        edited_title.strip(),
                                        edited_subject.strip(),
                                        edited_date.isoformat(),
                                        edited_priority,
                                        task["id"],
                                        user_id,
                                    ),
                                )
                                connection.commit()
                                st.session_state.pop("editing_task_id", None)
                                st.success("Task updated.")
                                st.rerun()

                        if cancel_edit:
                            st.session_state.pop("editing_task_id", None)
                            st.rerun()

        # Separate task categories
        st.divider()
        st.subheader("🔴 Overdue Tasks")
        if overdue_tasks:
            for task in overdue_tasks:
                render_task(task)
        else:
            st.success("No overdue tasks!")

        st.divider()
        st.subheader("📅 Upcoming Tasks")
        if upcoming_tasks:
            for task in upcoming_tasks:
                render_task(task)
        else:
            st.info("No upcoming tasks.")

        st.divider()
        st.subheader("✅ Completed Tasks")
        if completed_tasks:
            for task in completed_tasks:
                render_task(task)
        else:
            st.info("No completed tasks yet.")

    finally:
        connection.close()



# Initialize Streamlit session state
if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

if "user" not in st.session_state:
    st.session_state.user = None


# Require login before opening the platform
if st.session_state.user is None:
    try:
        if not DATABASE.exists():
            st.error(
                "campusos.db was not found in your Campus OS folder. "
                "Run your existing Flask app first and check the folder."
            )
            st.stop()

        show_auth_page()

    except sqlite3.Error as error:
        st.error(f"Could not open the database: {error}")

    st.stop()


user = st.session_state.user

pages = [
    "Dashboard",
    "Study Planner",
    "PDF Library",
    "Discussions",
    "Study Groups",
    "AI Study Assistant",
    "AI Quiz Generator",
]

if st.session_state.page not in pages:
    st.session_state.page = "Dashboard"


# Sidebar navigation
with st.sidebar:
    st.title("🎓 CampusOS")
    st.caption("Your university, connected.")

    st.write(f"Signed in as **{user['name']}**")
    st.caption(f"Registration ID: {user['registration_id']}")

    st.divider()

    for page_name in pages:
        if st.button(
            page_name,
            key=f"nav_{page_name}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.page == page_name
                else "secondary"
            ),
        ):
            st.session_state.page = page_name
            st.rerun()

    st.divider()

    if st.button("Log out", use_container_width=True):
        st.session_state.user = None
        st.session_state.page = "Dashboard"
        st.rerun()

    st.caption("CampusOS • Student Learning Platform")


# Dashboard and feature pages
page = st.session_state.page



if page == "Dashboard":
    st.title(f"Welcome to CampusOS, {user['name']} 👋")
    st.write("Your space to learn, share resources and study together.")

    try:
        stats = get_dashboard_stats(user["id"])

        # 1. CAMPUS OVERVIEW
        st.markdown("### 📊 Campus Overview")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("🎓 Registered Students", stats["students"])

        with col2:
            st.metric("📝 Study Tasks", stats["tasks"])

        with col3:
            st.metric("📚 PDF Resources", stats["resources"])

        col4, col5, col6 = st.columns(3)

        with col4:
            st.metric("💬 Discussions", stats["discussions"])

        with col5:
            st.metric("👥 Study Groups", stats["groups"])

        with col6:
            st.metric("🧠 Quiz Attempts", stats["quizzes"])

        st.divider()

        # 2. MY STUDENT PROFILE
        st.markdown("### 👤 My Student Profile")

        profile = get_db().execute(
            """
            SELECT name, registration_id, bio, department, semester
            FROM users
            WHERE id = ?
            """,
            (user["id"],),
        ).fetchone()

        if profile:
            with st.container(border=True):
                st.markdown(f"## 🎓 {profile['name'] or 'Student'}")

                st.caption(
                    f"Registration ID: {profile['registration_id'] or 'Not specified'}"
                )

                profile_col1, profile_col2 = st.columns(2)

                with profile_col1:
                    st.caption("DEPARTMENT")
                    st.write(profile["department"] or "Not specified")

                with profile_col2:
                    st.caption("SEMESTER")
                    st.write(profile["semester"] or "Not specified")

                st.divider()
                st.markdown("**About Me**")
                st.write(profile["bio"] or "No bio added yet.")

                if st.button(
                    "✏️ Edit My Profile",
                    key="edit_profile",
                    use_container_width=True,
                ):
                    st.session_state["editing_profile"] = True

            if st.session_state.get("editing_profile", False):
                st.markdown("#### Edit Your Profile")

                semester_options = [
                    "1st Semester", "2nd Semester", "3rd Semester",
                    "4th Semester", "5th Semester", "6th Semester",
                    "7th Semester", "8th Semester", "Other",
                ]

                current_semester = profile["semester"]
                semester_index = (
                    semester_options.index(current_semester)
                    if current_semester in semester_options
                    else 8
                )

                with st.form("profile_edit_form"):
                    name = st.text_input(
                        "Full Name",
                        value=profile["name"] or "",
                    )

                    department = st.text_input(
                        "Department",
                        value=profile["department"] or "",
                    )

                    semester = st.selectbox(
                        "Semester",
                        semester_options,
                        index=semester_index,
                    )

                    bio = st.text_area(
                        "About Me",
                        value=profile["bio"] or "",
                        max_chars=500,
                        placeholder="Tell other students a little about yourself...",
                    )

                    save_col, cancel_col = st.columns(2)

                    with save_col:
                        save = st.form_submit_button(
                            "Save Profile",
                            use_container_width=True,
                        )

                    with cancel_col:
                        cancel = st.form_submit_button(
                            "Cancel",
                            use_container_width=True,
                        )

                    if save:
                        if not name.strip():
                            st.error("Name cannot be empty.")
                        else:
                            db = get_db()
                            db.execute(
                                """
                                UPDATE users
                                SET name = ?, bio = ?, department = ?, semester = ?
                                WHERE id = ?
                                """,
                                (
                                    name.strip(),
                                    bio.strip(),
                                    department.strip(),
                                    semester,
                                    user["id"],
                                ),
                            )
                            db.commit()

                            st.session_state["editing_profile"] = False
                            st.success("Profile updated successfully!")
                            st.rerun()

                    if cancel:
                        st.session_state["editing_profile"] = False
                        st.rerun()

        st.divider()

        # 3. STUDY PROGRESS
        st.markdown("### 📅 Your Study Progress")

        progress_col1, progress_col2 = st.columns(2)

        with progress_col1:
            st.metric(
                "🔴 Overdue Tasks",
                stats["overdue"],
                delta=(
                    "Needs attention"
                    if stats["overdue"] > 0
                    else "All clear"
                ),
                delta_color=(
                    "inverse" if stats["overdue"] > 0 else "normal"
                ),
            )

        with progress_col2:
            st.metric(
                "📆 Upcoming Tasks",
                stats["upcoming"],
            )

        st.divider()

        # 4. YOUR TASK DEADLINES
        st.markdown("### 📌 Your Task Deadlines")
        st.caption("Keep track of pending work and upcoming submissions.")

        task_connection = get_db()

        try:
            today = date.today()

            deadline_tasks = task_connection.execute(
                """
                SELECT title, subject, due_date, priority
                FROM tasks
                WHERE user_id = ?
                  AND COALESCE(completed, 0) = 0
                  AND due_date IS NOT NULL
                  AND TRIM(due_date) != ''
                ORDER BY due_date ASC
                LIMIT 10
                """,
                (user["id"],),
            ).fetchall()

            if not deadline_tasks:
                st.success(
                    "🎉 No pending tasks with deadlines. You're all caught up!"
                )

            for task in deadline_tasks:
                try:
                    deadline = date.fromisoformat(
                        str(task["due_date"])[:10]
                    )
                except (ValueError, TypeError):
                    deadline = None

                with st.container(border=True):
                    task_col, status_col = st.columns([3, 2])

                    with task_col:
                        st.markdown(f"**{task['title']}**")

                        if task["subject"]:
                            st.caption(f"📘 {task['subject']}")

                        st.caption(
                            f"Priority: {task['priority'] or 'Medium'}"
                        )

                    with status_col:
                        if deadline is None:
                            st.warning("⚠️ Invalid deadline")

                        elif deadline < today:
                            st.error(
                                f"🔴 OVERDUE\n\n"
                                f"{deadline.strftime('%d %b %Y')}"
                            )

                        elif deadline == today:
                            st.warning(
                                f"🟠 DUE TODAY\n\n"
                                f"{deadline.strftime('%d %b %Y')}"
                            )

                        else:
                            days_left = (deadline - today).days

                            st.success(
                                f"🟢 {deadline.strftime('%d %b %Y')}"
                            )

                            st.caption(
                                f"{days_left} day(s) remaining"
                            )

        finally:
            task_connection.close()

        st.divider()

        # 5. EXPLORE CAMPUSOS
        st.markdown("### 🌐 Explore CampusOS")
        st.write(
            "Your all-in-one student platform for sharing study resources, "
            "joining discussions, collaborating in study groups, planning "
            "your work, and learning with AI."
        )

    except sqlite3.Error as error:
        st.warning(f"Dashboard data unavailable: {error}")


elif page == "Study Planner":
    try:
        show_planner(user["id"])
    except sqlite3.Error as error:
        st.error(f"The planner could not access the database: {error}")


elif page == "PDF Library":
    import uuid

    st.title("📚 PDF Library")
    st.write("Share and discover study materials with your classmates.")

    UPLOAD_FOLDER = BASE_DIR / "uploads"
    UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)

    connection = get_db()

    try:
        pdf_columns = table_columns(connection, "pdfs")

        required_columns = {
            "id", "filename", "uploaded_at", "title",
            "subject", "description", "stored_filename",
            "uploader_id", "semester"
        }

        if not required_columns.issubset(pdf_columns):
            st.error(
                "The existing PDFs table does not have all "
                "the required columns. No database changes were made."
            )
        else:
            st.subheader("Upload a study resource")

            with st.form("upload_pdf_form", clear_on_submit=True):
                uploaded_file = st.file_uploader(
                    "Choose a PDF file",
                    type=["pdf"],
                )

                title = st.text_input("Resource title")
                subject = st.text_input("Subject")
                semester = st.selectbox(
                    "Semester",
                    [
                        "Semester 1", "Semester 2",
                        "Semester 3", "Semester 4",
                        "Semester 5", "Semester 6",
                        "Semester 7", "Semester 8",
                        "Other",
                    ],
                )
                description = st.text_area("Description")

                upload_clicked = st.form_submit_button(
                    "Upload PDF",
                    use_container_width=True,
                )

            if upload_clicked:
                if not uploaded_file:
                    st.error("Please select a PDF file.")
                elif not title.strip() or not subject.strip():
                    st.error("Please enter the title and subject.")
                elif uploaded_file.size > 10 * 1024 * 1024:
                    st.error("The PDF must be 10 MB or smaller.")
                elif not uploaded_file.getvalue().startswith(b"%PDF-"):
                    st.error("This file does not appear to be a valid PDF.")
                else:
                    stored_filename = f"{uuid.uuid4().hex}.pdf"
                    file_path = UPLOAD_FOLDER / stored_filename

                    try:
                        file_path.write_bytes(uploaded_file.getvalue())

                        connection.execute(
                            """
                            INSERT INTO pdfs (
                                filename, uploaded_at, title,
                                subject, description, stored_filename,
                                uploader_id, semester
                            )
                            VALUES (
                                ?, CURRENT_TIMESTAMP, ?, ?, ?, ?, ?, ?
                            )
                            """,
                            (
                                uploaded_file.name,
                                title.strip(),
                                subject.strip(),
                                description.strip(),
                                stored_filename,
                                user["id"],
                                semester,
                            ),
                        )
                        connection.commit()
                        st.success("PDF uploaded successfully!")
                        st.rerun()

                    except Exception as error:
                        connection.rollback()

                        if file_path.exists():
                            file_path.unlink()

                        st.error(f"Could not save the PDF: {error}")

            st.divider()
            st.subheader("Browse study resources")

            search = st.text_input(
                "Search by title, subject, or description",
                key="pdf_search",
            )

            if search.strip():
                search_term = f"%{search.strip()}%"
                resources = connection.execute(
                    """
                    SELECT p.*, u.name AS uploader_name
                    FROM pdfs p
                    LEFT JOIN users u ON p.uploader_id = u.id
                    WHERE p.title LIKE ?
                       OR p.subject LIKE ?
                       OR p.description LIKE ?
                    ORDER BY p.id DESC
                    """,
                    (search_term, search_term, search_term),
                ).fetchall()
            else:
                resources = connection.execute(
                    """
                    SELECT p.*, u.name AS uploader_name
                    FROM pdfs p
                    LEFT JOIN users u ON p.uploader_id = u.id
                    ORDER BY p.id DESC
                    """
                ).fetchall()

            if not resources:
                st.info("No PDF resources found. Upload the first one!")

            for resource in resources:
                with st.container(border=True):
                    st.markdown(f"### {resource['title']}")
                    st.write(f"**Subject:** {resource['subject']}")
                    st.write(
                        f"**Semester:** {resource['semester'] or 'Not specified'}"
                    )

                    if resource["description"]:
                        st.write(resource["description"])

                    st.caption(
                        f"Uploaded by: {resource['uploader_name'] or 'Unknown'}"
                    )

                    stored_filename = resource["stored_filename"]
                    pdf_path = UPLOAD_FOLDER / stored_filename

                    if (
                        stored_filename
                        and pdf_path.exists()
                        and pdf_path.is_file()
                        and pdf_path.parent.resolve()
                        == UPLOAD_FOLDER.resolve()
                    ):
                        st.download_button(
                            "⬇️ Download PDF",
                            data=pdf_path.read_bytes(),
                            file_name=resource["filename"],
                            mime="application/pdf",
                            key=f"download_pdf_{resource['id']}",
                        )
                    else:
                        st.warning(
                            "The PDF file is not available on this computer."
                        )

                    if resource["uploader_id"] == user["id"]:
                        if st.button(
                            "🗑️ Delete my PDF",
                            key=f"delete_pdf_{resource['id']}",
                        ):
                            connection.execute(
                                "DELETE FROM pdfs WHERE id = ? AND uploader_id = ?",
                                (resource["id"], user["id"]),
                            )
                            connection.commit()

                            if (
                                stored_filename
                                and pdf_path.exists()
                                and pdf_path.is_file()
                                and pdf_path.parent.resolve()
                                == UPLOAD_FOLDER.resolve()
                            ):
                                pdf_path.unlink()

                            st.success("PDF deleted.")
                            st.rerun()

    except sqlite3.Error as error:
        st.error(f"PDF Library database error: {error}")

    finally:
        connection.close()



elif page == "Discussions":
    st.title("💬 Student Discussions")
    st.write("Ask questions, share ideas, and learn together.")

    connection = get_db()

    try:
        discussion_columns = table_columns(
            connection, "discussions"
        )
        reply_columns = table_columns(
            connection, "replies"
        )

        if not {
            "id", "title", "body", "author_id",
            "created_at", "category"
        }.issubset(discussion_columns):
            st.error(
                "The discussions table is missing required columns."
            )

        elif not {
            "id", "discussion_id", "body",
            "author_id", "created_at"
        }.issubset(reply_columns):
            st.error(
                "The replies table is missing required columns."
            )

        else:
            st.subheader("➕ Start a discussion")

            with st.form("create_discussion_form", clear_on_submit=True):
                title = st.text_input(
                    "Discussion title", max_chars=200
                )

                category = st.selectbox(
                    "Category",
                    [
                        "General",
                        "AI/ML",
                        "IOT",
                        "Programming",
                        "Examinations",
                        "Projects",
                        "Assignments",
                    ],
                )

                body = st.text_area(
                    "Write your question or discussion",
                    max_chars=5000,
                )

                create_clicked = st.form_submit_button(
                    "Post discussion",
                    use_container_width=True,
                )

            if create_clicked:
                if not title.strip() or not body.strip():
                    st.error(
                        "Please enter both a title and discussion text."
                    )
                else:
                    connection.execute(
                        """
                        INSERT INTO discussions
                            (title, body, author_id, created_at, category)
                        VALUES (?, ?, ?, CURRENT_TIMESTAMP, ?)
                        """,
                        (
                            title.strip(),
                            body.strip(),
                            user["id"],
                            category,
                        ),
                    )

                    connection.commit()
                    st.success("Discussion posted!")
                    st.rerun()

            st.divider()
            st.subheader("🔎 Explore discussions")

            search_text = st.text_input(
                "Search discussions",
                key="discussion_search",
                placeholder="Search by title or content...",
            )

            category_filter = st.selectbox(
                "Filter by category",
                [
                    "All categories",
                    "AI/ML",
                    "IOT",
                    "Programming",
                    "Examinations",
                    "Projects",
                    "Assignments",
                ],
                key="discussion_category_filter",
            )

            query = """
                SELECT d.*, u.name AS author_name
                FROM discussions d
                LEFT JOIN users u ON d.author_id = u.id
                WHERE 1 = 1
            """
            parameters = []

            if search_text.strip():
                query += " AND (d.title LIKE ? OR d.body LIKE ?)"
                search_term = f"%{search_text.strip()}%"
                parameters.extend([search_term, search_term])

            if category_filter != "All categories":
                query += " AND d.category = ?"
                parameters.append(category_filter)

            query += " ORDER BY d.id DESC"

            discussions = connection.execute(
                query, parameters
            ).fetchall()

            if not discussions:
                st.info(
                    "No discussions found. Try another search "
                    "or create the first discussion."
                )

            for discussion in discussions:
                with st.container(border=True):
                    st.subheader(discussion["title"])

                    st.caption(
                        f"Category: {discussion['category'] or 'General'}"
                        f" • By {discussion['author_name'] or 'Unknown'}"
                        f" • {discussion['created_at'] or ''}"
                    )

                    st.write(discussion["body"])

                    replies = connection.execute(
                        """
                        SELECT r.*, u.name AS author_name
                        FROM replies r
                        LEFT JOIN users u ON r.author_id = u.id
                        WHERE r.discussion_id = ?
                        ORDER BY r.id ASC
                        """,
                        (discussion["id"],),
                    ).fetchall()

                    with st.expander(
                        f"💬 Replies ({len(replies)})"
                    ):
                        if not replies:
                            st.write("No replies yet.")

                        for reply in replies:
                            st.markdown(
                                f"**{reply['author_name'] or 'Unknown'}**"
                            )
                            st.write(reply["body"])
                            st.caption(reply["created_at"] or "")
                            st.divider()

                        with st.form(
                            f"reply_form_{discussion['id']}",
                            clear_on_submit=True,
                        ):
                            reply_text = st.text_area(
                                "Write a reply",
                                key=f"reply_text_{discussion['id']}",
                                max_chars=3000,
                            )

                            reply_clicked = st.form_submit_button(
                                "Post reply",
                                use_container_width=True,
                            )

                        if reply_clicked:
                            if not reply_text.strip():
                                st.error("Please enter a reply.")
                            else:
                                connection.execute(
                                    """
                                    INSERT INTO replies
                                        (discussion_id, body, author_id, created_at)
                                    VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                                    """,
                                    (
                                        discussion["id"],
                                        reply_text.strip(),
                                        user["id"],
                                    ),
                                )

                                connection.commit()
                                st.success("Reply posted!")
                                st.rerun()

                    if discussion["author_id"] == user["id"]:
                        if st.button(
                            "🗑️ Delete my discussion",
                            key=f"delete_discussion_{discussion['id']}",
                        ):
                            connection.execute(
                                """
                                DELETE FROM replies
                                WHERE discussion_id = ?
                                """,
                                (discussion["id"],),
                            )

                            connection.execute(
                                """
                                DELETE FROM discussions
                                WHERE id = ? AND author_id = ?
                                """,
                                (discussion["id"], user["id"]),
                            )

                            connection.commit()
                            st.success("Discussion deleted.")
                            st.rerun()

    except sqlite3.Error as error:
        st.error(f"Discussions database error: {error}")

    finally:
        connection.close()



elif page == "Study Groups":
    st.title("👥 Study Groups")
    st.write("Find classmates, collaborate, and study together.")

    connection = get_db()

    try:
        group_columns = table_columns(connection, "study_groups")
        member_columns = table_columns(connection, "group_members")
        message_columns = table_columns(connection, "group_messages")

        if not {
            "id", "name", "description", "subject",
            "creator_id", "created_at"
        }.issubset(group_columns):
            st.error("The study_groups table is missing required columns.")

        elif not {
            "id", "group_id", "user_id", "joined_at"
        }.issubset(member_columns):
            st.error("The group_members table is missing required columns.")

        elif not {
            "id", "group_id", "user_id", "message", "created_at"
        }.issubset(message_columns):
            st.error("The group_messages table is missing required columns.")

        else:
            st.subheader("➕ Create a study group")

            with st.form("create_group_form", clear_on_submit=True):
                group_name = st.text_input("Group name", max_chars=100)
                subject = st.text_input("Subject", max_chars=100)
                description = st.text_area(
                    "Description",
                    max_chars=2000,
                    placeholder="What will your group study?",
                )

                create_clicked = st.form_submit_button(
                    "Create group",
                    use_container_width=True,
                )

            if create_clicked:
                if not group_name.strip() or not subject.strip():
                    st.error("Please enter a group name and subject.")
                else:
                    
                    cursor = connection.execute(
                        """
                        INSERT INTO study_groups
                            (name, description, subject, creator_id, created_at)
                        VALUES (?, ?, ?, ?, CURRENT_TIMESTAMP)
                        """,
                        (
                            group_name.strip(),
                            description.strip(),
                            subject.strip(),
                            user["id"],
                        ),
                    )

                    new_group_id = cursor.lastrowid

                    # Automatically add the creator as a member.
                    connection.execute(
                        """
                        INSERT INTO group_members (group_id, user_id, joined_at)
                        VALUES (?, ?, CURRENT_TIMESTAMP)
                        """,
                        (new_group_id, user["id"]),
                    )

                    connection.commit()
                    st.success("Study group created! You are automatically a member.")
                    st.rerun()

            st.divider()
            st.subheader("🔎 Find study groups")

            search_group = st.text_input(
                "Search by group name or subject",
                key="group_search",
            )

            if search_group.strip():
                term = f"%{search_group.strip()}%"
                groups = connection.execute(
                    """
                    SELECT g.*, u.name AS creator_name,
                           (SELECT COUNT(*) FROM group_members gm
                            WHERE gm.group_id = g.id) AS member_count
                    FROM study_groups g
                    LEFT JOIN users u ON u.id = g.creator_id
                    WHERE g.name LIKE ? OR g.subject LIKE ?
                       OR g.description LIKE ?
                    ORDER BY g.id DESC
                    """,
                    (term, term, term),
                ).fetchall()
            else:
                groups = connection.execute(
                    """
                    SELECT g.*, u.name AS creator_name,
                           (SELECT COUNT(*) FROM group_members gm
                            WHERE gm.group_id = g.id) AS member_count
                    FROM study_groups g
                    LEFT JOIN users u ON u.id = g.creator_id
                    ORDER BY g.id DESC
                    """
                ).fetchall()

            if not groups:
                st.info("No study groups found. Create the first one!")

            for group in groups:
                group_id = group["id"]

                membership = connection.execute(
                    """
                    SELECT id FROM group_members
                    WHERE group_id = ? AND user_id = ?
                    """,
                    (group_id, user["id"]),
                ).fetchone()

                is_creator = group["creator_id"] == user["id"]

                with st.container(border=True):
                    st.subheader(f"📚 {group['name']}")
                    st.write(f"**Subject:** {group['subject']}")
                    st.write(
                        group["description"] or "No description provided."
                    )
                    st.caption(
                        f"Created by {group['creator_name'] or 'Unknown'}"
                        f" • {group['member_count']} member(s)"
                    )

                    if is_creator:
                        st.success(
                            "You created this group and are automatically a member."
                        )

                    elif membership:
                        st.success("You are a member of this group.")

                        if st.button(
                            "Leave group",
                            key=f"leave_group_{group_id}",
                            use_container_width=True,
                        ):
                            connection.execute(
                                """
                                DELETE FROM group_members
                                WHERE group_id = ? AND user_id = ?
                                """,
                                (group_id, user["id"]),
                            )
                            connection.commit()
                            st.rerun()

                    else:
                        if st.button(
                            "Join group",
                            key=f"join_group_{group_id}",
                            use_container_width=True,
                        ):
                            connection.execute(
                                """
                                INSERT INTO group_members
                                    (group_id, user_id, joined_at)
                                VALUES (?, ?, CURRENT_TIMESTAMP)
                                """,
                                (group_id, user["id"]),
                            )
                            connection.commit()
                            st.success("You joined the group!")
                            st.rerun()

                    can_view_messages = bool(membership) or is_creator

                    if can_view_messages:
                        st.caption("You can access this group's messages.")
                    else:
                        st.caption("Join this group to view its messages.")

                    if can_view_messages:
                        with st.expander(f"💬 Messages — {group['name']}"):
                            messages = connection.execute(
                                """
                                SELECT m.*, u.name AS sender_name
                                FROM group_messages m
                                LEFT JOIN users u ON u.id = m.user_id
                                WHERE m.group_id = ?
                                ORDER BY m.id ASC
                                """,
                                (group_id,),
                            ).fetchall()

                            if not messages:
                                st.info("No messages yet. Start the conversation!")

                            for message in messages:
                                st.markdown(
                                    f"**{message['sender_name'] or 'Unknown'}**"
                                )
                                st.write(message["message"])
                                st.caption(message["created_at"] or "")
                                st.divider()

                            with st.form(
                                f"group_message_form_{group_id}",
                                clear_on_submit=True,
                            ):
                                message_text = st.text_area(
                                    "Write a message",
                                    max_chars=2000,
                                    key=f"group_message_text_{group_id}",
                                )

                                send_clicked = st.form_submit_button(
                                    "Send message",
                                    use_container_width=True,
                                )

                            if send_clicked:
                                if not message_text.strip():
                                    st.error("Please enter a message.")
                                else:
                                    connection.execute(
                                        """
                                        INSERT INTO group_messages
                                            (group_id, user_id, message, created_at)
                                        VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                                        """,
                                        (
                                            group_id,
                                            user["id"],
                                            message_text.strip(),
                                        ),
                                    )
                                    connection.commit()
                                    st.rerun()

    except sqlite3.IntegrityError:
        connection.rollback()
        st.warning(
            "This action could not be completed. You may already be a member."
        )

    except sqlite3.Error as error:
        st.error(f"Study Groups database error: {error}")

    finally:
        connection.close()



elif page == "AI Study Assistant":
    st.title("🤖 AI Study Assistant")
    st.write(
        "Ask questions about your study PDFs and get answers "
        "with references to the relevant pages."
    )

    UPLOAD_FOLDER = BASE_DIR / "uploads"

    connection = get_db()

    try:
        pdf_columns = table_columns(connection, "pdfs")

        required_columns = {
            "id", "title", "subject", "stored_filename", "filename"
        }

        if not required_columns.issubset(pdf_columns):
            st.error(
                "The PDF database is missing required columns."
            )

        else:
            pdfs = connection.execute(
                """
                SELECT id, title, subject, stored_filename, filename
                FROM pdfs
                ORDER BY id DESC
                """
            ).fetchall()

            if not pdfs:
                st.info(
                    "Your PDF Library is empty. Upload a study PDF "
                    "before using the AI Study Assistant."
                )

            else:
                pdf_options = {
                    (
                        f"{pdf['title']} — {pdf['subject'] or 'General'} "
                        f"(PDF #{pdf['id']})"
                    ): pdf
                    for pdf in pdfs
                }

                selected_label = st.selectbox(
                    "Choose a study PDF",
                    list(pdf_options.keys()),
                )

                selected_pdf = pdf_options[selected_label]

                st.caption(
                    "The assistant will answer using the selected PDF."
                )

                if "ai_question_input" not in st.session_state:
                    st.session_state["ai_question_input"] = ""
                    
                if st.session_state.pop("clear_ai_question", False):
                    st.session_state["ai_question_input"] = ""

                if "ai_question_input" not in st.session_state:
                    st.session_state["ai_question_input"] = ""

                question = st.text_area(
    "Ask a question about this PDF",
    placeholder=(
        "For example: Explain the main concepts "
        "covered in chapter one."
    ),
    max_chars=2000,
    key="ai_question_input",
)

                if st.button(
                    "🤖 Ask AI",
                    use_container_width=True,
                    type="primary",
                ):
                    if not question.strip():
                        st.warning("Please enter a question.")
                    else:
                        stored_filename = selected_pdf["stored_filename"]
                        pdf_path = (
                            UPLOAD_FOLDER / stored_filename
                        ).resolve()

                        if (
                            not stored_filename
                            or pdf_path.parent != UPLOAD_FOLDER.resolve()
                            or not pdf_path.is_file()
                        ):
                            st.error(
                                "The selected PDF file could not be found "
                                "in your uploads folder."
                            )

                        else:
                            try:
                                with st.spinner(
                                    "Reading the PDF and generating your answer..."
                                ):
                                    page_texts = []

                                    with fitz.open(pdf_path) as document:
                                        for page_number, pdf_page in enumerate(
                                            document, start=1
                                        ):
                                            text = pdf_page.get_text().strip()

                                            if text:
                                                page_texts.append(
                                                    f"[Page {page_number}]\n{text}"
                                                )

                                    if not page_texts:
                                        st.error(
                                            "No selectable text was found "
                                            "in this PDF. It may be a scanned "
                                            "document that needs OCR."
                                        )

                                    else:
                                        # Find PDF pages that best match the student's question.
                                        import re
                                        from collections import Counter

                                        stop_words = {
                                            "the", "is", "are", "was", "were", "a", "an", "and", "or",
                                            "to", "of", "in", "on", "for", "with", "what", "why", "how",
                                            "explain", "describe", "tell", "me", "about", "from", "this",
                                            "that", "it", "be", "by", "as", "at", "which", "can", "do",
                                        }

                                        question_words = set(
                                            re.findall(r"\b[a-zA-Z0-9]+\b", question.lower())
                                        ) - stop_words

                                        ranked_pages = []

                                        for page_text in page_texts:
                                            match = re.match(r"\[Page (\d+)\]\n(.*)", page_text, re.DOTALL)

                                            if not match:
                                                continue

                                            page_number = int(match.group(1))
                                            text = match.group(2)
                                            words = re.findall(r"\b[a-zA-Z0-9]+\b", text.lower())
                                            word_counts = Counter(words)

                                            score = sum(
                                                word_counts[word] for word in question_words
                                            )

                                            if score > 0:
                                                ranked_pages.append((score, page_number, text))

                                        ranked_pages.sort(key=lambda item: item[0], reverse=True)

                                        # Use up to three relevant pages, within a small context budget.
                                        selected_pages = ranked_pages[:3]

                                        context = "\n\n".join(
                                            f"[Page {page_number}]\n{text}"
                                            for score, page_number, text in selected_pages
                                        )

                                        context = context[:5000]

                                        if not context.strip():
                                            st.warning(
                                                "I couldn't find relevant information in the selected PDF. "
                                                "Try different keywords or ask a more specific question."
                                            )
                                            st.stop()

                                        prompt = f"""

You are CampusOS, a helpful study tutor.

Answer the student's question using the PDF text below.
Use simple language and explain the main points clearly.
For explanation questions, include a definition and a useful example
when supported by the PDF.
Use short headings and bullet points where appropriate.
Cite page numbers only when supported by the text.
Do not return JSON.
If no relevant PDF passages are provided, say that you could not find
the answer in the selected PDF. Do not invent page references.

PDF TEXT:
{context}

QUESTION:
{question.strip()}

Give a clear, concise answer:
"""


                                        response = requests.post(
                                            "http://localhost:11434/api/generate",
                                            json={
                                                "model": "qwen2.5:3b",
                                                "prompt": prompt,
                                                "stream": False,
                                                "options": {
                                                    "num_predict": 10000,
                                                    "temperature": 0.2,
                                                    "num_ctx": 4096,
                                                },
                                            },
                                            timeout=240,
                                        )
                                        if response.status_code != 200:
                                            st.error(f"Ollama error: {response.text}")
                                            st.stop()
                                        result = response.json()
                                        answer = result.get(
                                            "response", ""
                                        ).strip()

                                        if answer:
                                            st.session_state["last_ai_question"] = question.strip()
                                            st.session_state["last_ai_pdf_id"] = selected_pdf["id"]
                                            st.session_state["last_ai_answer"] = answer

                                            chat_key = f"ai_chat_{selected_pdf['id']}"

                                            if chat_key not in st.session_state:
                                                st.session_state[chat_key] = []

                                            st.session_state[chat_key].append({
                                                "question": question.strip(),
                                                "answer": answer
                                            })
                                            st.session_state["clear_ai_question"] = True


                                        else:
                                            st.error(
                                                "The AI returned an empty "
                                                "answer. Please try again."
                                            )

                            except requests.exceptions.ConnectionError:
                                st.error(
                                    "Ollama is not running or cannot be "
                                    "reached. Start Ollama on your computer "
                                    "and make sure the llama3.2:1b model "
                                    "is installed."
                                )

                            except requests.exceptions.Timeout:
                                st.error(
                                    "The AI took too long to respond. "
                                    "Try a shorter question or a smaller PDF."
                                )

                            except requests.exceptions.RequestException as error:
                                st.error(f"AI request failed: {error}")

                            except Exception as error:
                                st.error(
                                    f"Could not process this PDF: {error}"
                                )

                chat_key = f"ai_chat_{selected_pdf['id']}"
                chat_history = st.session_state.get(chat_key, [])

                if chat_history:
                    st.divider()
                    st.subheader("💬 Conversation History")

                    if st.button("🗑️ Clear Chat", key=f"clear_chat_{selected_pdf['id']}"):
                        st.session_state[chat_key] = []
                        st.session_state.pop("last_ai_question", None)
                        st.session_state.pop("last_ai_answer", None)
                        st.session_state.pop("last_ai_pdf_id", None)
                        st.rerun()

                    for message in chat_history:
                        with st.chat_message("user"):
                            st.markdown(message["question"])

                        with st.chat_message("assistant"):
                            st.markdown(message["answer"])

                    st.caption(
                        "Answers are generated from extracted PDF text. "
                        "Verify important information against the original document."
                    )

    except sqlite3.Error as error:
        st.error(f"AI Study Assistant database error: {error}")

    finally:
        connection.close()



elif page == "AI Quiz Generator":
    st.title("📝 AI Quiz Generator")
    st.write(
        "Generate multiple-choice quizzes from your study PDFs, "
        "test your knowledge, and review your score."
    )

    UPLOAD_FOLDER = BASE_DIR / "uploads"
    connection = get_db()

    try:
        pdf_columns = table_columns(connection, "pdfs")
        attempt_columns = table_columns(connection, "quiz_attempts")
        question_columns = table_columns(connection, "quiz_questions")

        if not {
            "id", "title", "subject", "stored_filename"
        }.issubset(pdf_columns):
            st.error("The PDF table is missing required columns.")

        elif not {
            "id", "user_id", "pdf_id", "score",
            "total_questions", "submitted", "created_at"
        }.issubset(attempt_columns):
            st.error("The quiz_attempts table is missing required columns.")

        elif not {
            "id", "attempt_id", "question", "option_a",
            "option_b", "option_c", "option_d",
            "correct_answer", "explanation", "selected_answer"
        }.issubset(question_columns):
            st.error("The quiz_questions table is missing required columns.")

        else:
            pdfs = connection.execute(
                """
                SELECT id, title, subject, stored_filename
                FROM pdfs
                ORDER BY id DESC
                """
            ).fetchall()

            if not pdfs:
                st.info(
                    "Your PDF Library is empty. Upload a PDF before "
                    "generating a quiz."
                )

            else:
                pdf_options = {
                    (
                        f"{pdf['title']} — {pdf['subject'] or 'General'} "
                        f"(PDF #{pdf['id']})"
                    ): pdf
                    for pdf in pdfs
                }

                selected_label = st.selectbox(
                    "Choose a PDF",
                    list(pdf_options.keys()),
                    key="quiz_pdf_selection",
                )
                selected_pdf = pdf_options[selected_label]

                number_of_questions = st.selectbox(
                    "Number of questions",
                    [3, 5, 10, 15, 20],
                    index=1,
                )
                
                difficulty = st.selectbox(
                    "Choose difficulty level",
                    ["Easy", "Medium", "Hard"],
                    index=1,
                    key="quiz_difficulty",
                )

                if st.button(
                    "✨ Generate Quiz",
                    type="primary",
                    use_container_width=True,
                ):
                    stored_filename = selected_pdf["stored_filename"]
                    pdf_path = (
                        UPLOAD_FOLDER / stored_filename
                    ).resolve()

                    if (
                        not stored_filename
                        or pdf_path.parent != UPLOAD_FOLDER.resolve()
                        or not pdf_path.is_file()
                    ):
                        st.error("The selected PDF file could not be found.")

                    else:
                        try:
                            with st.spinner(
                                "Reading your PDF and generating questions..."
                            ):
                                page_texts = []

                                with fitz.open(pdf_path) as document:
                                    for page_number, pdf_page in enumerate(
                                        document, start=1
                                    ):
                                        text = pdf_page.get_text().strip()
                                        if text:
                                            page_texts.append(
                                                f"[Page {page_number}]\n{text}"
                                            )

                                context = "\n\n".join(page_texts)[:10000]

                                if not context.strip():
                                    st.error(
                                        "No readable text was found in this PDF. "
                                        "Scanned PDFs may need OCR first."
                                    )
                                else:
                                    prompt = f"""


You are a university-level multiple-choice quiz generator.

Generate exactly {number_of_questions} separate multiple-choice questions
from the PDF text provided below.
DIFFICULTY LEVEL: {difficulty}

Difficulty guidelines:
- Easy: Test basic definitions, facts, and direct understanding.
- Medium: Test understanding, comparisons, and application of concepts.
- Hard: Test deeper reasoning, analysis, and connections between concepts.
- Adjust the difficulty of the questions and answer options to match
  the selected level.
- Keep every question answerable using the supplied PDF.

REQUIREMENTS:
- Return exactly {number_of_questions} question objects in the questions array.
- Every object must represent one independent question.
- Questions must test different concepts from the PDF.
- Do not combine multiple questions into one.
- Do not make essay questions.
- Each question must have four answer options: A, B, C, D.
- Answer options must be short statements or phrases, not questions.
- All four options must be meaningfully different.
- Exactly one option must be correct.
- Incorrect options must be plausible but clearly incorrect according
  to the PDF.
- Avoid duplicate, overlapping, or nearly identical options.
- Explain briefly why the correct answer is correct.
- Use only information supported by the supplied PDF.
- If information is insufficient for some questions, use other distinct
  concepts in the supplied text rather than repeating a question.
- Before returning the result, count the question objects and verify
  that there are exactly {number_of_questions}.

Return valid JSON only, without Markdown fences, using this structure:

{{
  "questions": [
    {{
      "question": "A specific question about the PDF?",
      "A": "First possible answer",
      "B": "Second possible answer",
      "C": "Third possible answer",
      "D": "Fourth possible answer",
      "correct_answer": "A",
      "explanation": "A concise explanation supported by the PDF."
    }}
  ]
}}

PDF TEXT:
{context}
"""



                                    response = requests.post(
                                        "http://localhost:11434/api/generate",
                                        json={
                                            "model": "qwen2.5:3b",
                                            "prompt": prompt,
                                            "format": "json",
                                            "stream": False,
                                            "keep_alive": "10m",
                                            "options": {
                                                "num_predict": 600 * number_of_questions,
                                                "temperature": 0.2,
                                                "num_ctx": 4096,
                                            },
                                        },
                                        timeout=250,
                                    )
                                    response.raise_for_status()

                                    model_text = response.json().get(
                                        "response", ""
                                    ).strip()

                                    import json
                                    quiz_data = json.loads(model_text)
                                    generated_questions = quiz_data.get(
                                        "questions", []
                                    )
                                    st.info(f"AI generated {len(generated_questions)} questions.")

                                    
                                
                                    valid_questions = []
                                    seen_questions = set()

                                    for item in generated_questions:
                                        if not isinstance(item, dict):
                                            continue

                                        question_text = str(
                                            item.get("question", "")
                                        ).strip()

                                        correct = str(
                                            item.get("correct_answer", "")
                                        ).strip().upper()

                                        options = {
                                            letter: str(
                                                item.get(letter, "")
                                            ).strip()
                                            for letter in ["A", "B", "C", "D"]
                                        }

                                        explanation = str(
                                            item.get("explanation", "")
                                        ).strip()

                                        normalized_question = (
                                            " ".join(
                                                question_text.casefold().split()
                                            )
                                        )

                                        if (
                                            len(question_text) < 15
                                            or not all(options.values())
                                            or correct not in ["A", "B", "C", "D"]
                                            or len(set(
                                                option.casefold()
                                                for option in options.values()
                                            )) != 4
                                            or len(explanation) < 25
                                            or normalized_question in seen_questions
                                        ):
                                            continue

                                        item["question"] = question_text
                                        item["correct_answer"] = correct
                                        item["explanation"] = explanation

                                        for letter in ["A", "B", "C", "D"]:
                                            item[letter] = options[letter]
                                            

                                        seen_questions.add(normalized_question)

                                        valid_questions.append(item)


                                    if not valid_questions:
                                        st.info(f"AI returned {len(generated_questions)} questions; {len(valid_questions)} passed validation.")
                                        st.error(
                                            "The AI did not return valid questions. Please try again."
                                        )
                                    
                                    else:
                                        cursor = connection.execute(
                                            """
                                            INSERT INTO quiz_attempts
                                                (user_id, pdf_id, score,
                                                 total_questions, submitted,
                                                 created_at)
                                            VALUES (?, ?, 0, ?, 0, CURRENT_TIMESTAMP)
                                            """,
                                            (
                                                user["id"],
                                                selected_pdf["id"],
                                                len(valid_questions),
                                            ),
                                        )

                                        attempt_id = cursor.lastrowid

                                        for item in valid_questions:
                                            connection.execute(
                                                """
                                                INSERT INTO quiz_questions
                                                    (attempt_id, question,
                                                     option_a, option_b,
                                                     option_c, option_d,
                                                     correct_answer, explanation,
                                                     selected_answer)
                                                VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL)
                                                """,
                                                (
                                                    attempt_id,
                                                    item["question"].strip(),
                                                    item["A"].strip(),
                                                    item["B"].strip(),
                                                    item["C"].strip(),
                                                    item["D"].strip(),
                                                    item["correct_answer"].strip().upper(),
                                                    item.get("explanation", "").strip(),
                                                ),
                                            )

                                        connection.commit()
                                        st.session_state["active_quiz_id"] = attempt_id
                                        st.session_state["active_quiz_pdf_id"] = selected_pdf["id"]
                                        st.rerun()

                        except requests.exceptions.ConnectionError:
                            st.error(
                                "Ollama cannot be reached. Make sure Ollama "
                                "is running and llama3.2:1b is installed."
                            )
                        except requests.exceptions.Timeout:
                            st.error(
                                "Quiz generation took too long. Try fewer "
                                "questions or a shorter PDF."
                            )
                        except requests.exceptions.RequestException as error:
                            connection.rollback()
                            st.error(f"AI request failed: {error}")
                        except (ValueError, KeyError, TypeError) as error:
                            connection.rollback()
                            st.error(
                                "The AI returned an invalid quiz format. "
                                "Please try generating the quiz again."
                            )
                        except sqlite3.Error as error:
                            connection.rollback()
                            st.error(f"Could not save the quiz: {error}")
                        except Exception as error:
                            connection.rollback()
                            st.error(f"Could not generate the quiz: {error}")

                active_quiz_id = st.session_state.get("active_quiz_id")

                if active_quiz_id:
                    attempt = connection.execute(
                        """
                        SELECT * FROM quiz_attempts
                        WHERE id = ? AND user_id = ?
                        """,
                        (active_quiz_id, user["id"]),
                    ).fetchone()

                    if attempt and not attempt["submitted"]:
                        st.divider()
                        st.subheader("📝 Your Quiz")

                        quiz_questions = connection.execute(
                            """
                            SELECT * FROM quiz_questions
                            WHERE attempt_id = ?
                            ORDER BY id ASC
                            """,
                            (active_quiz_id,),
                        ).fetchall()

                        with st.form(f"quiz_answer_form_{active_quiz_id}"):
                            answers = {}

                            for index, question in enumerate(
                                quiz_questions, start=1
                            ):
                                st.markdown(
                                    f"**Question {index}: "
                                    f"{question['question']}**"
                                )

                                options = {
                                    "A": question["option_a"],
                                    "B": question["option_b"],
                                    "C": question["option_c"],
                                    "D": question["option_d"],
                                }

                                choice = st.radio(
                                    "Choose your answer",
                                    options=list(options.keys()),
                                    format_func=lambda letter, opts=options: (
                                        f"{letter}. {opts[letter]}"
                                    ),
                                    key=f"answer_{active_quiz_id}_{question['id']}",
                                    index=None,
                                )

                                answers[question["id"]] = choice
                                st.divider()

                            submitted = st.form_submit_button(
                                "Submit Quiz",
                                type="primary",
                                use_container_width=True,
                            )

                        if submitted:
                            score = 0

                            for question in quiz_questions:
                                selected = answers[question["id"]]

                                connection.execute(
                                    """
                                    UPDATE quiz_questions
                                    SET selected_answer = ?
                                    WHERE id = ? AND attempt_id = ?
                                    """,
                                    (
                                        selected,
                                        question["id"],
                                        active_quiz_id,
                                    ),
                                )

                                if (
                                    selected
                                    and selected == question["correct_answer"]
                                ):
                                    score += 1

                            connection.execute(
                                """
                                UPDATE quiz_attempts
                                SET score = ?, submitted = 1
                                WHERE id = ? AND user_id = ?
                                """,
                                (score, active_quiz_id, user["id"]),
                            )

                            connection.commit()
                            st.rerun()

                    elif attempt and attempt["submitted"]:
                        st.divider()
                        st.subheader("📊 Quiz Results")

                        score = attempt["score"]
                        total = attempt["total_questions"]
                        percentage = (
                            round((score / total) * 100)
                            if total else 0
                        )

                        col1, col2, col3 = st.columns(3)
                        col1.metric("Score", f"{score}/{total}")
                        col2.metric("Percentage", f"{percentage}%")
                        col3.metric(
                            "Result",
                            "Passed" if percentage >= 50 else "Keep practising",
                        )

                        result_questions = connection.execute(
                            """
                            SELECT * FROM quiz_questions
                            WHERE attempt_id = ?
                            ORDER BY id ASC
                            """,
                            (active_quiz_id,),
                        ).fetchall()

                        for index, question in enumerate(
                            result_questions, start=1
                        ):
                            options = {
                                "A": question["option_a"],
                                "B": question["option_b"],
                                "C": question["option_c"],
                                "D": question["option_d"],
                            }

                            st.markdown(
                                f"**Question {index}: {question['question']}**"
                            )

                            correct = question["correct_answer"]
                            chosen = question["selected_answer"]

                            if chosen == correct:
                                st.success(
                                    f"Your answer: {chosen}. "
                                    f"{options[chosen]} — Correct!"
                                )
                            else:
                                chosen_text = (
                                    f"{chosen}. {options[chosen]}"
                                    if chosen in options else "Not answered"
                                )
                                st.error(f"Your answer: {chosen_text}")
                                st.info(
                                    f"Correct answer: {correct}. "
                                    f"{options[correct]}"
                                )

                            if question["explanation"]:
                                st.write(
                                    f"**Explanation:** {question['explanation']}"
                                )

                            st.divider()

                        if st.button(
                            "Generate another quiz",
                            use_container_width=True,
                        ):
                            st.session_state.pop("active_quiz_id", None)
                            st.session_state.pop("active_quiz_pdf_id", None)
                            st.rerun()

    except sqlite3.Error as error:
        st.error(f"Quiz database error: {error}")

    finally:
        connection.close()


