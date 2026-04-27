import streamlit as st


def load_custom_css() -> None:
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

        :root {
            --swiss-red: #e30613;
            --deep-red: #a70d17;
            --navy: #061b3d;
            --navy-soft: #123564;
            --lake: #0e5c83;
            --mint: #dff8ec;
            --sun: #f6b84b;
            --rose: #fff1f2;
            --ink: #061b3d;
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
                radial-gradient(circle at 8% 5%, rgba(227,6,19,.12), transparent 28%),
                radial-gradient(circle at 90% 2%, rgba(6,27,61,.12), transparent 30%),
                linear-gradient(118deg, rgba(255,241,242,.92) 0%, rgba(255,250,244,.94) 34%, rgba(247,250,253,.96) 68%, rgba(239,245,252,.98) 100%),
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

        .brand-logo-frame {
            width: 48px;
            height: 48px;
            flex: 0 0 48px;
            overflow: hidden;
            border-radius: 15px;
            background: white;
            border: 1px solid rgba(255,255,255,.86);
            box-shadow: 0 14px 34px rgba(6,27,61,.14);
            transition: transform .18s ease, box-shadow .18s ease, opacity .18s ease;
        }

        .brand-row:hover .brand-logo-frame {
            transform: translateY(-1px) scale(1.035);
            box-shadow: 0 18px 42px rgba(6,27,61,.20);
        }

        .brand-logo-img {
            width: 100%;
            height: 100%;
            display: block;
            object-fit: cover;
        }

        .brand-row--compact .brand-logo-frame {
            width: 40px;
            height: 40px;
            flex-basis: 40px;
            border-radius: 12px;
        }

        .brand-title {
            color: var(--navy);
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
            margin: 1.8vh auto 0;
            padding: 0 18px 52px;
            animation: fadeUp .55s ease both;
        }

        .language-gate .brand-row {
            justify-content: flex-start;
            width: fit-content;
            margin-bottom: 24px;
        }

        .language-gate .brand-caption {
            text-align: left;
        }

        .language-landing {
            position: relative;
            overflow: hidden;
            display: grid;
            grid-template-columns: minmax(0, 1.04fr) minmax(330px, .82fr);
            align-items: center;
            gap: 34px;
            border-radius: 34px;
            padding: 42px;
            border: 1px solid rgba(255,255,255,.74);
            background:
                linear-gradient(135deg, rgba(255,255,255,.97), rgba(255,242,243,.94) 44%, rgba(239,245,252,.94)),
                repeating-linear-gradient(135deg, rgba(255,255,255,.32) 0, rgba(255,255,255,.32) 1px, transparent 1px, transparent 18px);
            box-shadow:
                0 34px 90px rgba(6,27,61,.13),
                inset 0 1px 0 rgba(255,255,255,.72);
            isolation: isolate;
        }

        .language-landing:before {
            content: "";
            position: absolute;
            inset: 12px;
            border-radius: 26px;
            border: 1px solid rgba(255,255,255,.58);
            pointer-events: none;
            z-index: -1;
        }

        .language-landing:after {
            content: "";
            position: absolute;
            width: 420px;
            height: 120px;
            right: -110px;
            top: 34px;
            border-radius: 32px;
            background: linear-gradient(90deg, rgba(227,6,19,.13), rgba(255,255,255,.22), rgba(6,27,61,.13));
            transform: rotate(-16deg);
            opacity: .9;
            z-index: -1;
        }

        .language-copy {
            position: relative;
            z-index: 1;
        }

        .language-hero__badge {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            padding: 9px 15px;
            border-radius: 999px;
            background: rgba(255,255,255,.68);
            border: 1px solid rgba(227,6,19,.14);
            color: var(--deep-red);
            font-size: .8rem;
            font-weight: 850;
            margin-bottom: 20px;
            box-shadow: 0 10px 28px rgba(15,23,42,.06);
        }

        .language-hero__title {
            margin: 0;
            color: var(--ink);
            font-size: 4.2rem;
            line-height: 1.02;
            font-weight: 900;
            white-space: nowrap;
            max-width: 980px;
        }

        .language-hero__copy {
            max-width: 640px;
            margin: 20px 0 0;
            color: #526174;
            font-size: 1.12rem;
            line-height: 1.65;
        }

        .language-benefits {
            display: flex;
            justify-content: flex-start;
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
            background: linear-gradient(135deg, var(--swiss-red), var(--navy));
        }

        .language-visual {
            position: relative;
            z-index: 1;
            border-radius: 28px;
            overflow: hidden;
            background: rgba(255,255,255,.84);
            border: 1px solid rgba(255,255,255,.88);
            box-shadow:
                0 28px 70px rgba(6,27,61,.16),
                inset 0 1px 0 rgba(255,255,255,.86);
            transform: rotate(1.2deg);
            transition: transform .2s ease, box-shadow .2s ease;
        }

        .language-visual:hover {
            transform: rotate(0deg) translateY(-3px);
            box-shadow: 0 34px 82px rgba(6,27,61,.20);
        }

        .language-banner-img {
            display: block;
            width: 100%;
            aspect-ratio: 1 / 1;
            object-fit: cover;
        }

        .language-selector-card {
            max-width: 860px;
            margin: 30px auto 0;
            padding: 28px;
            border-radius: 30px;
            border: 1px solid rgba(255,255,255,.78);
            background: rgba(255,255,255,.82);
            backdrop-filter: blur(18px);
            box-shadow:
                0 28px 70px rgba(6,27,61,.12),
                inset 0 1px 0 rgba(255,255,255,.76);
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

        .language-gate div.stButton > button {
            min-width: 196px;
            min-height: 52px;
            padding: 0 32px;
            border-radius: 999px;
            font-size: 1rem;
            background: linear-gradient(135deg, var(--swiss-red), #d20d19 44%, var(--deep-red));
        }

        .language-selector-card div.stButton > button {
            width: 100%;
            min-width: 0;
            min-height: 86px;
            padding: 0 18px;
            border-radius: 24px;
            border: 1px solid rgba(148,163,184,.22);
            background:
                linear-gradient(145deg, rgba(255,255,255,.99), rgba(248,250,252,.90));
            color: var(--ink);
            font-size: 1.13rem;
            font-weight: 900;
            box-shadow: 0 14px 34px rgba(6,27,61,.07);
            transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
        }

        .language-selector-card div.stButton > button:hover {
            transform: translateY(-3px);
            border-color: rgba(227,6,19,.36);
            color: var(--ink);
            background:
                linear-gradient(145deg, rgba(255,255,255,1), rgba(255,241,242,.86));
            box-shadow: 0 20px 48px rgba(6,27,61,.12);
        }

        .language-selector-card div.stButton > button[kind="primary"] {
            border-color: rgba(227,6,19,.72);
            color: var(--deep-red);
            background:
                linear-gradient(145deg, rgba(255,255,255,1), rgba(255,236,238,.96) 50%, rgba(238,244,252,.94));
            box-shadow:
                0 20px 52px rgba(227,6,19,.16),
                inset 0 0 0 1px rgba(227,6,19,.18);
        }

        .language-selector-card div.stButton > button p {
            font-size: 1.13rem;
            font-weight: 900;
            line-height: 1.2;
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

        .hero-logo-img {
            width: 28px;
            height: 28px;
            border-radius: 8px;
            object-fit: cover;
            box-shadow: 0 8px 18px rgba(6,27,61,.14);
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
            .language-gate .brand-row {
                margin-left: 2px;
            }
            .language-landing {
                grid-template-columns: 1fr;
                padding: 26px 18px 20px;
                border-radius: 26px;
            }
            .language-visual {
                max-width: 280px;
                margin: 0 auto;
                border-radius: 22px;
                transform: none;
            }
            .language-hero__badge {
                font-size: .72rem;
            }
            .language-hero__title {
                font-size: 2.25rem;
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
            .language-selector-card div.stButton > button {
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
