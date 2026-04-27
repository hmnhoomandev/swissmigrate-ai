import streamlit as st


def load_custom_css() -> None:
    st.markdown(
        """
        <style>
        .stApp {
            background: #f7f8fb;
            color: #111827;
        }
        .main .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e7eb;
        }
        .brand-mark {
            width: 42px;
            height: 42px;
            border-radius: 8px;
            background: #0f766e;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 800;
            margin-bottom: 0.8rem;
        }
        .center-shell {
            max-width: 760px;
            margin: 8vh auto 0 auto;
            padding: 2rem;
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
        }
        div.stButton > button {
            border-radius: 8px;
            border: 1px solid #0f766e;
            background: #0f766e;
            color: white;
            font-weight: 700;
        }
        div.stButton > button:hover {
            border: 1px solid #115e59;
            background: #115e59;
            color: white;
        }
        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
        }
        .stAlert {
            border-radius: 8px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
