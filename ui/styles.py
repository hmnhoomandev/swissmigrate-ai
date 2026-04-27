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
            --mint: #dff8ec;
            --sun: #f6b84b;
            --rose: #fff1f2;
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
                linear-gradient(118deg, rgba(255,241,242,.92) 0%, rgba(255,250,244,.90) 32%, rgba(238,251,246,.92) 68%, rgba(248,251,255,.96) 100%),
                linear-gradient(180deg, #fffaf4 0%, #f8fbff 100%);
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

        .brand-logo {
            position: relative;
            width: 48px;
            height: 48px;
            flex: 0 0 48px;
            overflow: hidden;
            border-radius: 15px;
            background:
                linear-gradient(145deg, #fffbf7 0%, #ffe8e6 42%, #dff8ec 100%);
            border: 1px solid rgba(255,255,255,.82);
            box-shadow:
                0 16px 34px rgba(153,27,27,.16),
                inset 0 1px 0 rgba(255,255,255,.92);
        }

        .brand-logo__cross,
        .brand-logo__path,
        .brand-logo__node {
            position: absolute;
            display: block;
        }

        .brand-logo__cross {
            left: 11px;
            top: 11px;
            width: 15px;
            height: 15px;
        }

        .brand-logo__cross:before,
        .brand-logo__cross:after {
            content: "";
            position: absolute;
            border-radius: 999px;
            background: var(--swiss-red);
        }

        .brand-logo__cross:before {
            left: 6px;
            top: 0;
            width: 4px;
            height: 15px;
        }

        .brand-logo__cross:after {
            left: 0;
            top: 6px;
            width: 15px;
            height: 4px;
        }

        .brand-logo__path {
            left: 16px;
            bottom: 12px;
            width: 24px;
            height: 18px;
            border-right: 4px solid var(--lake);
            border-bottom: 4px solid var(--lake);
            border-radius: 0 0 14px 0;
            transform: skewX(-12deg);
        }

        .brand-logo__path:after {
            content: "";
            position: absolute;
            right: -7px;
            top: -6px;
            width: 9px;
            height: 9px;
            border-top: 4px solid var(--lake);
            border-right: 4px solid var(--lake);
            transform: rotate(45deg);
            border-radius: 2px;
        }

        .brand-logo__node {
            right: 11px;
            top: 12px;
            width: 7px;
            height: 7px;
            border-radius: 50%;
            background: var(--ink);
            box-shadow:
                -8px 18px 0 -1px rgba(23,32,51,.80),
                0 18px 0 -1px rgba(220,38,38,.80);
        }

        .brand-row--compact .brand-logo {
            width: 40px;
            height: 40px;
            flex-basis: 40px;
            border-radius: 13px;
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

        .language-gate {
            position: relative;
            max-width: 1120px;
            margin: 2.2vh auto 0;
            padding: 0 18px 44px;
            animation: fadeUp .55s ease both;
        }

        .language-gate .brand-row {
            justify-content: center;
            margin-bottom: 22px;
        }

        .language-gate .brand-caption {
            text-align: left;
        }

        .language-hero {
            position: relative;
            overflow: hidden;
            text-align: center;
            border-radius: 34px;
            padding: 54px 48px 48px;
            border: 1px solid rgba(255,255,255,.74);
            background:
                linear-gradient(135deg, rgba(255,255,255,.96), rgba(255,243,238,.94) 44%, rgba(230,249,240,.92)),
                repeating-linear-gradient(135deg, rgba(255,255,255,.32) 0, rgba(255,255,255,.32) 1px, transparent 1px, transparent 18px);
            box-shadow:
                0 34px 90px rgba(15,23,42,.13),
                inset 0 1px 0 rgba(255,255,255,.72);
            isolation: isolate;
        }

        .language-hero:before {
            content: "";
            position: absolute;
            inset: 12px;
            border-radius: 26px;
            border: 1px solid rgba(255,255,255,.58);
            pointer-events: none;
            z-index: -1;
        }

        .language-hero:after {
            content: "";
            position: absolute;
            width: 420px;
            height: 120px;
            right: -110px;
            top: 34px;
            border-radius: 32px;
            background: linear-gradient(90deg, rgba(220,38,38,.14), rgba(246,184,75,.16), rgba(15,118,110,.14));
            transform: rotate(-16deg);
            opacity: .9;
            z-index: -1;
        }

        .language-hero__badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 9px 15px;
            border-radius: 999px;
            background: rgba(255,255,255,.68);
            border: 1px solid rgba(220,38,38,.12);
            color: var(--deep-red);
            font-size: .8rem;
            font-weight: 850;
            margin-bottom: 20px;
            box-shadow: 0 10px 28px rgba(15,23,42,.06);
        }

        .language-hero__title {
            margin: 0 auto;
            color: var(--ink);
            font-size: 4.45rem;
            line-height: 1.02;
            font-weight: 900;
            white-space: nowrap;
            max-width: 980px;
        }

        .language-hero__copy {
            max-width: 820px;
            margin: 20px auto 0;
            color: #526174;
            font-size: 1.12rem;
            line-height: 1.65;
        }

        .language-benefits {
            display: flex;
            justify-content: center;
            gap: 10px;
            flex-wrap: wrap;
            margin-top: 24px;
        }

        .language-benefits span {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 13px;
            border-radius: 999px;
            color: #334155;
            background: rgba(255,255,255,.68);
            border: 1px solid rgba(148,163,184,.18);
            font-size: .88rem;
            font-weight: 800;
            box-shadow: 0 10px 26px rgba(15,23,42,.055);
        }

        .language-benefits span:before {
            content: "";
            width: 7px;
            height: 7px;
            border-radius: 999px;
            background: linear-gradient(135deg, var(--swiss-red), var(--lake));
        }

        .language-selector-card {
            max-width: 930px;
            margin: -20px auto 0;
            padding: 24px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,.78);
            background: rgba(255,255,255,.82);
            backdrop-filter: blur(18px);
            box-shadow: 0 28px 70px rgba(15,23,42,.12);
        }

        .language-selector-heading {
            display: flex;
            align-items: flex-end;
            justify-content: space-between;
            gap: 18px;
            margin-bottom: 18px;
        }

        .language-selector-heading span {
            color: var(--ink);
            font-size: 1.04rem;
            font-weight: 900;
        }

        .language-selector-heading small {
            color: var(--muted);
            font-size: .85rem;
            font-weight: 650;
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 12px;
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label {
            position: relative;
            min-height: 58px;
            margin: 0;
            padding: 0 18px;
            border-radius: 999px;
            border: 1px solid rgba(148,163,184,.24);
            background:
                linear-gradient(145deg, rgba(255,255,255,.98), rgba(255,250,244,.76));
            box-shadow: 0 12px 30px rgba(15,23,42,.052);
            transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
            cursor: pointer;
            justify-content: center;
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label:hover {
            transform: translateY(-3px);
            border-color: rgba(220,38,38,.30);
            box-shadow: 0 18px 42px rgba(15,23,42,.10);
            background:
                linear-gradient(145deg, rgba(255,255,255,1), rgba(255,241,242,.82));
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked) {
            border-color: rgba(220,38,38,.62);
            background:
                linear-gradient(145deg, rgba(255,255,255,.98), rgba(255,241,242,.92) 52%, rgba(223,248,236,.78));
            box-shadow:
                0 20px 50px rgba(220,38,38,.16),
                inset 0 0 0 1px rgba(220,38,38,.18);
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label:has(input:checked):after {
            content: "";
            position: absolute;
            right: 16px;
            top: 50%;
            width: 8px;
            height: 14px;
            border-right: 2px solid var(--deep-red);
            border-bottom: 2px solid var(--deep-red);
            transform: translateY(-58%) rotate(42deg);
            border-radius: 1px;
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label > div:first-child {
            display: none;
        }

        .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label p {
            color: var(--ink);
            font-size: 1.02rem;
            font-weight: 850;
            line-height: 1.2;
            white-space: normal;
        }

        .language-action {
            display: flex;
            justify-content: center;
            margin-top: 26px;
        }

        .language-action div.stButton {
            width: auto;
        }

        .language-action div.stButton > button {
            min-width: 196px;
            min-height: 52px;
            padding: 0 32px;
            border-radius: 999px;
            font-size: 1rem;
            background: linear-gradient(135deg, #e11d48, #dc2626 44%, #991b1b);
        }

        @keyframes fadeUp {
            from {
                opacity: 0;
                transform: translateY(14px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
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
            .language-gate {
                margin-top: 1.2vh;
                padding: 0 4px 34px;
            }
            .language-hero {
                padding: 34px 20px 32px;
                border-radius: 26px;
            }
            .language-hero__badge {
                font-size: .72rem;
            }
            .language-hero__title {
                font-size: 2.1rem;
                white-space: nowrap;
            }
            .language-hero__copy {
                font-size: .98rem;
            }
            .language-selector-card {
                padding: 18px;
                border-radius: 24px;
            }
            .language-selector-heading {
                display: block;
            }
            .language-selector-heading small {
                display: block;
                margin-top: 4px;
            }
            .language-gate div[data-testid="stRadio"] div[role="radiogroup"] {
                grid-template-columns: repeat(2, minmax(0, 1fr));
                gap: 10px;
            }
            .language-gate div[data-testid="stRadio"] div[role="radiogroup"] > label {
                min-height: 72px;
                padding: 14px;
                border-radius: 17px;
            }
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
