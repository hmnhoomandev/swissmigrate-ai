import streamlit as st


def render_sidebar():
    with st.sidebar:
        st.markdown(
            """
            <div class="sidebar-logo">🧭</div>
            <p class="sidebar-title">IMMIGRATION AI ASSISTANT</p>
            <p class="sidebar-subtitle">Understand. Navigate. Belong.</p>
            """,
            unsafe_allow_html=True,
        )

        page = st.radio(
            "Navigation",
            [
                "📄 Letter Helper",
                "🗓️ First 365 Days Guide",
                "📍 Canton Navigator",
                "🕘 History",
                "🔖 Saved",
                "⚙️ Settings",
            ],
            label_visibility="collapsed",
        )

        st.markdown("---")

        st.markdown(
            """
            <div class="privacy-box">
                🛡️ Your data stays private and secure.
                <br><br>
                <span style="font-size: 13px; text-decoration: underline;">Learn more</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        return page