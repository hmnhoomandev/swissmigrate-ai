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
            padding-top: 1.35rem;
            padding-bottom: 3rem;
        }

        section[data-testid="stSidebar"] {
            background:
                radial-gradient(circle at 12% 0%, rgba(227,6,19,.14), transparent 32%),
                radial-gradient(circle at 92% 12%, rgba(14,92,131,.14), transparent 34%),
                linear-gradient(180deg, rgba(255,255,255,.88), rgba(255,250,244,.82) 54%, rgba(238,244,252,.88));
            border-right: 1px solid rgba(255,255,255,.72);
            box-shadow: 20px 0 54px rgba(15,23,42,.08);
            backdrop-filter: blur(22px);
        }

        section[data-testid="stSidebar"] > div {
            padding: 1.45rem 1rem 1.6rem;
        }

        section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
            color: var(--ink);
        }

        section[data-testid="stSidebar"] hr {
            margin: 1.2rem 0;
            border-color: rgba(148,163,184,.20);
        }

        section[data-testid="stSidebar"] div[role="radiogroup"] {
            display: flex;
            flex-direction: column;
            gap: 8px;
            padding: 4px 0;
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"] {
            position: relative;
            min-height: 48px;
            margin: 0;
            padding: 0 12px 0 14px;
            border-radius: 16px;
            border: 1px solid transparent;
            background: transparent;
            color: #475569;
            font-size: .94rem;
            font-weight: 800;
            transition:
                transform .22s ease,
                color .22s ease,
                background .22s ease,
                border-color .22s ease,
                box-shadow .22s ease;
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"]:hover {
            transform: translateX(3px);
            color: var(--navy);
            border-color: rgba(255,255,255,.66);
            background: rgba(255,255,255,.58);
            box-shadow: 0 14px 34px rgba(6,27,61,.08);
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked) {
            color: var(--navy);
            border-color: rgba(227,6,19,.20);
            background:
                linear-gradient(135deg, rgba(255,255,255,.96), rgba(255,241,242,.78) 54%, rgba(239,245,252,.78));
            box-shadow:
                0 16px 38px rgba(6,27,61,.10),
                inset 0 1px 0 rgba(255,255,255,.86);
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"]:has(input:checked):before {
            content: "";
            position: absolute;
            left: 0;
            top: 10px;
            bottom: 10px;
            width: 4px;
            border-radius: 999px;
            background: linear-gradient(180deg, var(--swiss-red), var(--lake));
            box-shadow: 0 0 18px rgba(227,6,19,.28);
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"] > div:first-child {
            display: none;
        }

        section[data-testid="stSidebar"] label[data-baseweb="radio"] p {
            font-size: .94rem;
            font-weight: 850;
            line-height: 1.15;
            white-space: normal;
        }

        section[data-testid="stSidebar"] .brand-row {
            padding: 8px 6px 4px;
            margin-bottom: 10px;
        }

        .sidebar-section-label {
            color: #7b8798;
            font-size: .68rem;
            font-weight: 900;
            letter-spacing: .08em;
            line-height: 1;
            margin: 0 0 10px 6px;
            text-transform: uppercase;
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
            border-radius: 16px;
            background: white;
            border: 1px solid rgba(255,255,255,.86);
            box-shadow: 0 16px 38px rgba(6,27,61,.15);
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
            font-size: 1.13rem;
            font-weight: 900;
            margin: 0;
            line-height: 1.08;
        }

        .brand-caption {
            color: var(--muted);
            font-size: .78rem;
            line-height: 1.35;
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
            border-radius: 30px;
            padding: 34px;
            background:
                radial-gradient(circle at 86% 18%, rgba(227,6,19,.16), transparent 24%),
                radial-gradient(circle at 72% 88%, rgba(14,92,131,.14), transparent 30%),
                linear-gradient(135deg, rgba(255,255,255,.98), rgba(255,247,250,.92) 42%, rgba(239,245,252,.90));
            box-shadow:
                0 28px 76px rgba(15,23,42,.105),
                inset 0 1px 0 rgba(255,255,255,.84);
            margin-bottom: 24px;
            isolation: isolate;
        }

        .hero-panel:after {
            content: "";
            position: absolute;
            right: -34px;
            top: 22px;
            width: 290px;
            height: 86px;
            border-radius: 999px;
            background: linear-gradient(90deg, rgba(227,6,19,.13), rgba(255,255,255,.28), rgba(14,92,131,.16));
            transform: rotate(-14deg);
            z-index: -1;
        }

        .hero-eyebrow {
            display: inline-flex;
            align-items: center;
            gap: 10px;
            padding: 7px 12px;
            border-radius: 999px;
            background: rgba(255,255,255,.66);
            border: 1px solid rgba(227,6,19,.13);
            color: var(--deep-red);
            font-weight: 800;
            font-size: .82rem;
            margin-bottom: 14px;
            box-shadow: 0 10px 28px rgba(15,23,42,.055);
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
            font-size: 2.45rem;
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
            background:
                linear-gradient(145deg, rgba(255,255,255,.90), rgba(248,250,252,.72));
            border: 1px solid rgba(255,255,255,.76);
            border-radius: 24px;
            padding: 18px;
            box-shadow:
                0 18px 48px rgba(15,23,42,.075),
                inset 0 1px 0 rgba(255,255,255,.76);
            margin-bottom: 20px;
        }

        .first365-shell {
            border-radius: 28px;
            padding: 22px;
            margin-bottom: 24px;
            border: 1px solid rgba(255,255,255,.78);
            background:
                radial-gradient(circle at 92% 10%, rgba(14,92,131,.12), transparent 26%),
                linear-gradient(145deg, rgba(255,255,255,.94), rgba(255,247,250,.78) 48%, rgba(239,245,252,.80));
            box-shadow:
                0 22px 58px rgba(15,23,42,.085),
                inset 0 1px 0 rgba(255,255,255,.84);
        }

        .first365-panel-title {
            color: var(--ink);
            font-size: 1.05rem;
            font-weight: 900;
            margin-bottom: 14px;
        }

        .first365-muted {
            color: var(--muted);
            font-size: .92rem;
            line-height: 1.6;
            margin: 14px 2px 0;
        }

        .first365-shell label[data-baseweb="checkbox"] {
            min-height: 48px;
            margin-bottom: 8px;
            padding: 8px 10px;
            border-radius: 16px;
            border: 1px solid rgba(148,163,184,.18);
            background: rgba(255,255,255,.58);
            transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
        }

        .first365-shell label[data-baseweb="checkbox"]:hover {
            transform: translateY(-1px);
            border-color: rgba(227,6,19,.22);
            background: rgba(255,255,255,.82);
            box-shadow: 0 12px 28px rgba(15,23,42,.06);
        }

        .first365-result-intro {
            display: flex;
            align-items: center;
            gap: 14px;
            margin: 8px 0 18px;
            padding: 16px;
            border-radius: 22px;
            background: rgba(255,255,255,.78);
            border: 1px solid rgba(255,255,255,.72);
            box-shadow: 0 14px 34px rgba(15,23,42,.06);
        }

        .first365-result-intro > span {
            width: 50px;
            height: 50px;
            border-radius: 16px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: 900;
            background: linear-gradient(135deg, var(--swiss-red), var(--lake));
            box-shadow: 0 14px 28px rgba(6,27,61,.15);
        }

        .first365-result-intro b {
            display: block;
            color: var(--ink);
            font-size: 1rem;
            font-weight: 900;
        }

        .first365-result-intro p {
            margin: 4px 0 0;
            color: var(--muted);
            font-size: .9rem;
            font-weight: 750;
        }

        .first365-topic-card {
            margin: 16px 0 10px;
            padding: 20px;
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,.78);
            background:
                linear-gradient(145deg, rgba(255,255,255,.94), rgba(248,250,252,.76));
            box-shadow:
                0 18px 48px rgba(15,23,42,.075),
                inset 0 1px 0 rgba(255,255,255,.82);
        }

        .first365-topic-card--missing {
            border-color: rgba(246,184,75,.34);
            background:
                linear-gradient(145deg, rgba(255,255,255,.96), rgba(255,248,226,.74));
        }

        .first365-topic-card__head {
            display: flex;
            align-items: center;
            gap: 14px;
        }

        .first365-topic-card__head > span {
            width: 44px;
            height: 44px;
            flex: 0 0 44px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            border-radius: 15px;
            color: white;
            font-weight: 900;
            background: linear-gradient(135deg, var(--swiss-red), var(--deep-red));
        }

        .first365-topic-card h3 {
            margin: 0;
            font-size: 1.12rem;
            line-height: 1.25;
        }

        .first365-topic-card__head p,
        .first365-file-path {
            margin: 5px 0 0;
            color: var(--muted);
            font-size: .84rem;
            font-weight: 750;
            overflow-wrap: anywhere;
        }

        .first365-topic-card__summary {
            color: #475569;
            line-height: 1.68;
            margin: 14px 0 0;
        }

        .stat-card {
            min-height: 144px;
            background:
                linear-gradient(145deg, rgba(255,255,255,.88), rgba(248,250,252,.70));
            border: 1px solid rgba(255,255,255,.74);
            border-radius: 24px;
            padding: 21px;
            color: #475569;
            line-height: 1.58;
            box-shadow: 0 16px 42px rgba(15,23,42,.065);
            transition: transform .2s ease, box-shadow .2s ease, border-color .2s ease;
        }

        .stat-card:hover {
            transform: translateY(-3px);
            border-color: rgba(227,6,19,.16);
            box-shadow: 0 24px 58px rgba(15,23,42,.095);
        }

        .stat-card b {
            display: block;
            color: var(--ink);
            font-size: 1rem;
            font-weight: 900;
            margin-bottom: 7px;
        }

        .service-shell {
            position: relative;
            overflow: hidden;
            min-height: 220px;
            border: 1px solid rgba(255,255,255,.80);
            border-radius: 28px;
            padding: 24px;
            background:
                radial-gradient(circle at 90% 8%, rgba(227,6,19,.10), transparent 28%),
                linear-gradient(145deg, rgba(255,255,255,.96), rgba(255,247,250,.76) 50%, rgba(239,245,252,.80));
            box-shadow:
                0 18px 50px rgba(15,23,42,.08),
                inset 0 1px 0 rgba(255,255,255,.82);
            transition:
                transform .22s ease,
                box-shadow .22s ease,
                border-color .22s ease,
                background .22s ease;
            cursor: pointer;
            isolation: isolate;
        }

        .service-shell:hover {
            transform: translateY(-5px) scale(1.01);
            border-color: rgba(227,6,19,.20);
            box-shadow:
                0 30px 74px rgba(15,23,42,.13),
                inset 0 1px 0 rgba(255,255,255,.90);
        }

        .service-shell__shine {
            position: absolute;
            inset: 0;
            background: linear-gradient(115deg, transparent 0%, rgba(255,255,255,.52) 42%, transparent 62%);
            transform: translateX(-112%);
            transition: transform .45s ease;
            z-index: -1;
        }

        .service-shell:hover .service-shell__shine {
            transform: translateX(112%);
        }

        .service-icon {
            width: 54px;
            height: 54px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 1.28rem;
            font-weight: 900;
            background:
                linear-gradient(135deg, var(--swiss-red), #a70d17 42%, var(--lake));
            box-shadow: 0 16px 34px rgba(6,27,61,.16);
            margin-bottom: 18px;
        }

        .service-title {
            color: var(--ink);
            font-size: 1.12rem;
            font-weight: 900;
            margin-bottom: 8px;
            line-height: 1.2;
        }

        .service-text {
            color: var(--muted);
            line-height: 1.62;
            font-size: .95rem;
            min-height: 78px;
        }

        .profile-badge,
        .profile-chip {
            display: flex;
            align-items: center;
            gap: 12px;
            width: 100%;
            border-radius: 20px;
            background:
                radial-gradient(circle at 100% 0%, rgba(227,6,19,.12), transparent 30%),
                linear-gradient(145deg, rgba(255,255,255,.92), rgba(248,250,252,.78));
            border: 1px solid rgba(255,255,255,.72);
            padding: 12px;
            font-weight: 850;
            color: var(--ink);
            box-shadow:
                0 16px 38px rgba(6,27,61,.075),
                inset 0 1px 0 rgba(255,255,255,.72);
            line-height: 1.1;
            max-width: 100%;
        }

        .profile-badge__flag {
            width: 42px;
            height: 42px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            border-radius: 14px;
            background: white;
            border: 1px solid rgba(148,163,184,.18);
            box-shadow: 0 8px 18px rgba(6,27,61,.10);
            flex: 0 0 42px;
        }

        .flag-img {
            display: block;
            border-radius: 9px;
            object-fit: contain;
            background: white;
        }

        .profile-badge__place {
            display: block;
            color: var(--navy);
            font-weight: 900;
            font-size: .96rem;
            white-space: normal;
        }

        .profile-badge__content {
            min-width: 0;
        }

        .profile-badge__type {
            display: inline-flex;
            width: fit-content;
            margin-top: 8px;
            padding: 5px 9px;
            border-radius: 999px;
            background: rgba(227,6,19,.08);
            color: #8f111a;
            font-weight: 800;
            font-size: .76rem;
            white-space: normal;
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
            border-radius: 16px;
            border: 1px solid rgba(220,38,38,.18);
            background: linear-gradient(135deg, var(--swiss-red), #cf101b 48%, var(--deep-red));
            color: white;
            font-weight: 850;
            box-shadow: 0 14px 30px rgba(220,38,38,.22);
            transition:
                transform .18s ease,
                box-shadow .18s ease,
                border-color .18s ease,
                filter .18s ease;
            min-height: 46px;
            cursor: pointer;
        }

        div.stButton > button:hover,
        div.stDownloadButton > button:hover,
        div[data-testid="stLinkButton"] > a:hover {
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 20px 44px rgba(220,38,38,.28);
            filter: saturate(1.04);
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

        .letter-trust-strip {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: 12px;
            margin: -4px 0 22px;
        }

        .letter-trust-strip > div {
            min-height: 90px;
            border-radius: 22px;
            padding: 16px;
            background:
                linear-gradient(145deg, rgba(255,255,255,.86), rgba(239,245,252,.70));
            border: 1px solid rgba(255,255,255,.78);
            box-shadow: 0 14px 38px rgba(15,23,42,.06);
        }

        .letter-trust-strip b {
            display: block;
            color: var(--ink);
            font-size: .92rem;
            font-weight: 900;
            margin-bottom: 6px;
        }

        .letter-trust-strip span {
            color: var(--muted);
            font-size: .86rem;
            line-height: 1.45;
        }

        .letter-input-panel,
        .letter-output-shell,
        .letter-result-card {
            border-radius: 24px;
            border: 1px solid rgba(255,255,255,.78);
            background:
                linear-gradient(145deg, rgba(255,255,255,.93), rgba(248,250,252,.76));
            box-shadow:
                0 18px 48px rgba(15,23,42,.075),
                inset 0 1px 0 rgba(255,255,255,.80);
        }

        .letter-input-panel,
        .letter-output-shell {
            padding: 20px;
            margin-bottom: 20px;
        }

        .letter-output-shell {
            min-height: 430px;
            background:
                radial-gradient(circle at 84% 14%, rgba(227,6,19,.12), transparent 30%),
                linear-gradient(145deg, rgba(255,255,255,.94), rgba(255,241,242,.74) 48%, rgba(239,245,252,.78));
        }

        .letter-panel-title {
            color: var(--ink);
            font-size: 1.08rem;
            font-weight: 900;
            margin-bottom: 14px;
        }

        .privacy-flow {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 8px;
            margin: 22px 0;
        }

        .privacy-flow span {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 58px;
            padding: 10px;
            border-radius: 16px;
            color: var(--navy);
            background: rgba(255,255,255,.72);
            border: 1px solid rgba(148,163,184,.20);
            font-size: .78rem;
            font-weight: 850;
            text-align: center;
        }

        .letter-small-note {
            color: var(--muted);
            font-size: .9rem;
            line-height: 1.6;
        }

        .letter-results-grid {
            margin-top: 10px;
        }

        .letter-result-card {
            padding: 20px;
            margin-bottom: 18px;
        }

        .letter-card-kicker {
            display: flex;
            align-items: center;
            gap: 9px;
            color: var(--ink);
            font-weight: 900;
            margin-bottom: 14px;
        }

        .letter-card-kicker span {
            width: 32px;
            height: 32px;
            border-radius: 12px;
            display: inline-flex;
            align-items: center;
            justify-content: center;
            color: white;
            background: linear-gradient(135deg, var(--swiss-red), var(--lake));
            box-shadow: 0 10px 22px rgba(6,27,61,.13);
            font-weight: 900;
        }

        .summary-row {
            display: grid;
            grid-template-columns: minmax(120px, .45fr) minmax(0, 1fr);
            gap: 14px;
            padding: 11px 0;
            border-bottom: 1px solid rgba(148,163,184,.16);
        }

        .summary-row span {
            color: var(--muted);
            font-size: .84rem;
            font-weight: 800;
        }

        .summary-row b {
            color: var(--ink);
            font-size: .92rem;
            line-height: 1.45;
        }

        .letter-summary-copy {
            color: #475569;
            line-height: 1.65;
            margin: 14px 0 0;
        }

        .urgency-badge {
            display: inline-flex;
            align-items: center;
            min-height: 50px;
            padding: 0 18px;
            border-radius: 999px;
            color: white;
            font-size: .96rem;
            font-weight: 900;
            box-shadow: 0 16px 34px rgba(15,23,42,.12);
        }

        .urgency-badge--very-urgent {
            background: linear-gradient(135deg, #991b1b, #dc2626);
        }

        .urgency-badge--urgent {
            background: linear-gradient(135deg, #b45309, #f97316);
        }

        .urgency-badge--medium {
            background: linear-gradient(135deg, #0e7490, #14b8a6);
        }

        .urgency-badge--low {
            background: linear-gradient(135deg, #166534, #22c55e);
        }

        .urgency-badge--none {
            color: var(--ink);
            background: linear-gradient(135deg, rgba(255,255,255,.96), rgba(226,232,240,.88));
            border: 1px solid rgba(148,163,184,.24);
        }

        .deadline-pill {
            width: fit-content;
            margin-top: 16px;
            padding: 10px 13px;
            border-radius: 999px;
            color: #475569;
            background: rgba(255,255,255,.72);
            border: 1px solid rgba(148,163,184,.20);
            font-size: .86rem;
            font-weight: 800;
        }

        .pii-counts {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
        }

        .pii-counts span {
            padding: 8px 10px;
            border-radius: 999px;
            color: #475569;
            background: rgba(255,255,255,.72);
            border: 1px solid rgba(148,163,184,.18);
            font-size: .82rem;
            font-weight: 800;
        }

        @media (max-width: 760px) {
            .letter-trust-strip,
            .privacy-flow {
                grid-template-columns: 1fr;
            }
            .summary-row {
                grid-template-columns: 1fr;
                gap: 4px;
            }
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
