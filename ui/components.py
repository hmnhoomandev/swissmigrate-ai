import streamlit as st


def render_header():
    col1, col2 = st.columns([4, 1])

    with col1:
        st.markdown(
            """
            <h1 class="app-title">Hello, Hooman! 👋</h1>
            <p class="app-subtitle">
                Welcome to <span class="gradient-text">IMMIGRATION AI ASSISTANT</span>.
                How can I help you today?
            </p>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.selectbox(
            "Language",
            ["English", "فارسی", "Français", "Arabic", "Turkish", "Ukrainian", "Chinese", "Spanish"],
            label_visibility="collapsed",
        )


def render_letter_helper():
    left, right = st.columns([1.05, 1.15], gap="large")

    with left:
        st.markdown(
            """
            <div class="hero-card">
                <div class="section-title">📄 Letter Helper</div>
                <p class="section-description">
                    Upload a letter or paste the text below. The assistant explains it in simple language,
                    detects urgency, and suggests what you should do next.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.write("")

        uploaded_file = st.file_uploader(
            "Upload your letter",
            type=["pdf", "png", "jpg", "jpeg"],
            help="Supported formats: PDF, JPG, PNG",
        )

        letter_text = st.text_area(
            "Or paste letter text",
            placeholder="Paste the content of your letter here...",
            height=190,
            max_chars=5000,
        )

        analyze_clicked = st.button("✨ Explain My Letter", use_container_width=True)

        st.markdown(
            """
            <div class="privacy-box">
                🛡️ We handle your data securely and never share it with third parties.
            </div>
            """,
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
            <div class="glass-card">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div class="section-title">Analysis Result</div>
                    <div class="success-pill">✅ Analysis Complete</div>
                </div>

                <div class="result-box">
                    <h4>📌 Summary</h4>
                    <p>
                        This letter appears to be from an official office. It asks the person to take action,
                        attend an appointment, or provide documents related to their immigration situation.
                    </p>
                </div>

                <div class="result-box">
                    <div style="display:flex; justify-content:space-between; align-items:center;">
                        <h4>⚠️ Urgency</h4>
                        <div class="danger-pill">HIGH</div>
                    </div>
                    <p>You may need to act within a limited time.</p>
                    <p style="color:#e11d48; font-weight:800;">Possible deadline: Please check the letter date carefully.</p>
                </div>

                <div class="result-box">
                    <h4>✅ Next Steps</h4>
                    <p><span class="step-circle">1</span>Read the appointment date, deadline, or requested action.</p>
                    <p><span class="step-circle">2</span>Prepare all documents mentioned in the letter.</p>
                    <p><span class="step-circle">3</span>If you do not understand something, contact the office quickly.</p>
                </div>

                <div class="result-box" style="background:#eef6ff;">
                    <h4>💬 Suggested Reply</h4>
                    <p>
                        Dear Sir/Madam,<br><br>
                        I confirm the receipt of your letter. I will follow the requested steps and provide
                        the necessary documents as soon as possible.<br><br>
                        Best regards,
                    </p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        col_a, col_b = st.columns(2)
        with col_a:
            st.button("🔖 Save Result", use_container_width=True)
        with col_b:
            st.button("📤 Export / Share", use_container_width=True)

    return analyze_clicked, uploaded_file, letter_text


def render_feature_footer():
    st.markdown(
        """
        <div class="footer-strip">
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap: 18px;">
                <div class="feature-card">
                    <div class="feature-icon">🛡️</div>
                    <h4>Understand with Clarity</h4>
                    <p class="section-description">We explain complex official letters in simple words.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🧭</div>
                    <h4>Navigate with Confidence</h4>
                    <p class="section-description">Get step-by-step guidance for your situation.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🤝</div>
                    <h4>Access Support</h4>
                    <p class="section-description">Find useful services, offices, and organizations.</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon">🏠</div>
                    <h4>Feel at Home Faster</h4>
                    <p class="section-description">Settle in Switzerland with less stress and confusion.</p>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_placeholder_page(title, description, icon):
    st.markdown(
        f"""
        <div class="hero-card">
            <h2>{icon} {title}</h2>
            <p class="section-description">{description}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">✨</div>
                <h4>Coming Soon</h4>
                <p class="section-description">This feature will be added in the next development chapter.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔐</div>
                <h4>Privacy First</h4>
                <p class="section-description">The design will protect sensitive user information.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🌍</div>
                <h4>Multilingual</h4>
                <p class="section-description">The feature will support multiple migrant languages.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )