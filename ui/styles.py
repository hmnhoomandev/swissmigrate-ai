import streamlit as st


def load_custom_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --swiss-red: #dc2626;
            --deep-red: #991b1b;
            --lake: #0f766e;
            --ink: #172033;
            --muted: #64748b;
            --paper: #fffaf4;
            --card: rgba(255,255,255,.86);
            --line: rgba(148,163,184,.24);
        }

        * {
            font-family: 'Inter', system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
            letter-spacing: 0;
        }

        .stApp {
            color: var(--ink);
            background:
                radial-gradient(circle at 12% 8%, rgba(220,38,38,.12), transparent 28%),
                radial-gradient(circle at 88% 3%, rgba(15,118,110,.13), transparent 28%),
                linear-gradient(135deg, #fffaf4 0%, #f8fbff 45%, #f2f7f5 100%);
        }

        .main .block-container {
            max-width: 1220px;
            padding-top: 1.6rem;
            padding-bottom: 3rem;
        }

        section[data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, rgba(255,255,255,.94), rgba(255,250,244,.88));
            border-right: 1px solid var(--line);
            box-shadow: 18px 0 44px rgba(15,23,42,.05);
        }

        h1, h2, h3 {
            color: var(--ink);
            font-weight: 850;
        }

        .brand-row {
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }

        .brand-mark {
            width: 48px;
            height: 48px;
            border-radius: 14px;
            background: linear-gradient(135deg, var(--swiss-red), var(--deep-red));
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            box-shadow: 0 14px 30px rgba(220,38,38,.28);
        }

        .brand-title {
            font-size: 1.12rem;
            font-weight: 900;
            margin: 0;
        }

        .brand-caption {
            color: var(--muted);
            font-size: .84rem;
            margin: 0;
        }

        .hero-panel {
            position: relative;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,.72);
            border-radius: 28px;
            padding: 30px;
            background:
                linear-gradient(135deg, rgba(255,255,255,.96), rgba(255,247,237,.90) 44%, rgba(236,253,245,.88));
            box-shadow: 0 24px 70px rgba(15,23,42,.10);
            margin-bottom: 22px;
        }

        .hero-panel:after {
            content: "";
            position: absolute;
            right: -56px;
            top: -74px;
            width: 210px;
            height: 210px;
            border-radius: 50%;
            background: conic-gradient(from 35deg, rgba(220,38,38,.20), rgba(15,118,110,.18), rgba(255,255,255,.04));
        }

        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(220,38,38,.08);
            color: var(--deep-red);
            font-weight: 800;
            font-size: .82rem;
            margin-bottom: 14px;
        }

        .hero-title {
            position: relative;
            font-size: 2.2rem;
            line-height: 1.05;
            font-weight: 900;
            max-width: 760px;
            margin: 0;
        }

        .hero-copy {
            position: relative;
            color: var(--muted);
            max-width: 780px;
            font-size: 1.02rem;
            line-height: 1.7;
            margin-top: 12px;
            margin-bottom: 0;
        }

        .soft-card {
            background: var(--card);
            border: 1px solid rgba(255,255,255,.72);
            border-radius: 22px;
            padding: 22px;
            box-shadow: 0 18px 48px rgba(15,23,42,.07);
        }

        .stat-card {
            min-height: 138px;
            background: rgba(255,255,255,.78);
            border: 1px solid var(--line);
            border-radius: 22px;
            padding: 20px;
        }

        .service-shell {
            min-height: 205px;
            border: 1px solid rgba(255,255,255,.78);
            border-radius: 26px;
            padding: 22px;
            background:
                linear-gradient(145deg, rgba(255,255,255,.94), rgba(255,247,237,.72));
            box-shadow: 0 18px 48px rgba(15,23,42,.08);
            transition: transform .18s ease, box-shadow .18s ease;
        }

        .service-shell:hover {
            transform: translateY(-3px);
            box-shadow: 0 26px 70px rgba(15,23,42,.12);
        }

        .service-icon {
            width: 50px;
            height: 50px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.35rem;
            font-weight: 900;
            background: linear-gradient(135deg, var(--swiss-red), var(--lake));
            margin-bottom: 15px;
        }

        .service-title {
            font-size: 1.08rem;
            font-weight: 900;
            margin-bottom: 8px;
        }

        .service-text {
            color: var(--muted);
            line-height: 1.55;
            font-size: .94rem;
            min-height: 72px;
        }

        .profile-chip {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            border-radius: 999px;
            background: rgba(255,255,255,.72);
            border: 1px solid var(--line);
            padding: 8px 12px;
            font-weight: 800;
            color: var(--ink);
        }

        .center-shell {
            max-width: 840px;
            margin: 7vh auto 0 auto;
            padding: 34px;
            background:
                linear-gradient(135deg, rgba(255,255,255,.96), rgba(255,250,244,.90));
            border: 1px solid rgba(255,255,255,.72);
            border-radius: 28px;
            box-shadow: 0 28px 80px rgba(15,23,42,.12);
        }

        div.stButton > button,
        div.stDownloadButton > button,
        div[data-testid="stLinkButton"] > a {
            border-radius: 14px;
            border: 1px solid rgba(220,38,38,.18);
            background: linear-gradient(135deg, var(--swiss-red), var(--deep-red));
            color: white;
            font-weight: 850;
            box-shadow: 0 14px 30px rgba(220,38,38,.22);
            transition: transform .16s ease, box-shadow .16s ease;
            min-height: 42px;
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover,
        div[data-testid="stLinkButton"] > a:hover {
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 20px 44px rgba(220,38,38,.28);
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,.82);
            border: 1px solid var(--line);
            border-radius: 20px;
            padding: 1rem;
            box-shadow: 0 14px 34px rgba(15,23,42,.06);
        }

        .stAlert {
            border-radius: 18px;
            border: 1px solid rgba(255,255,255,.5);
        }

        textarea,
        input,
        div[data-baseweb="select"] > div {
            border-radius: 16px !important;
        }

        div[data-testid="stExpander"] {
            border-radius: 18px;
            border: 1px solid var(--line);
            background: rgba(255,255,255,.72);
        }

        @media (max-width: 760px) {
            .hero-panel {
                padding: 22px;
                border-radius: 22px;
            }
            .hero-title {
                font-size: 1.65rem;
            }
            .center-shell {
                padding: 22px;
                margin-top: 2vh;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
