import streamlit as st


def load_css():
    st.markdown(
        """
        <style>
        .stApp {
            background: #f7f9fc;
        }

        section[data-testid="stSidebar"] {
            background: #ffffff;
            border-right: 1px solid #e5e7eb;
        }

        .main-title {
            font-size: 34px;
            font-weight: 800;
            color: #0f172a;
            margin-bottom: 5px;
        }

        .subtitle {
            font-size: 17px;
            color: #475569;
            margin-bottom: 30px;
        }

        .card {
            background: white;
            padding: 24px;
            border-radius: 22px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 8px 24px rgba(15, 23, 42, 0.06);
            margin-bottom: 18px;
        }

        .module-card {
            background: white;
            padding: 22px;
            border-radius: 20px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.05);
            min-height: 145px;
        }

        .module-icon {
            font-size: 34px;
            margin-bottom: 8px;
        }

        .module-title {
            font-size: 22px;
            font-weight: 800;
            color: #0f172a;
        }

        .module-text {
            font-size: 15px;
            color: #475569;
        }

        .privacy-box {
            background: #eef2ff;
            border-radius: 18px;
            padding: 18px;
            color: #1e3a8a;
            font-size: 15px;
        }

        div.stButton > button {
            border-radius: 14px;
            padding: 0.7rem 1rem;
            font-weight: 700;
        }

        div.stDownloadButton > button {
            border-radius: 14px;
            padding: 0.7rem 1rem;
            font-weight: 700;
        }

        .language-box {
            background: white;
            padding: 36px;
            border-radius: 26px;
            border: 1px solid #e5e7eb;
            box-shadow: 0 10px 30px rgba(15, 23, 42, 0.08);
            max-width: 760px;
            margin: auto;
            margin-top: 80px;
        }

        .small-muted {
            color: #64748b;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )