import streamlit as st
from chatbot import RecruitmentChatbot
from report_generator import ReportGenerator

st.title("AI-Driven Recruitment Personality Assessment Chatbot")

if 'chatbot' not in st.session_state:
    st.session_state.chatbot = RecruitmentChatbot()

if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'assessment_complete' not in st.session_state:
    st.session_state.assessment_complete = False

if 'biodata' not in st.session_state:
    st.session_state.biodata = {}

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Type 'start' to begin the assessment"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    response = st.session_state.chatbot.chat(prompt)
    st.session_state.messages.append({"role": "assistant", "content": response})
    with st.chat_message("assistant"):
        st.markdown(response)

    if "Assessment complete" in response:
        st.session_state.assessment_complete = True
        st.session_state.biodata = st.session_state.chatbot.biodata

# Display scores if assessment is ongoing
if st.session_state.messages and not st.session_state.assessment_complete:
    scores = st.session_state.chatbot.get_scores()
    st.sidebar.header("Current Scores")
    for trait, score in scores.items():
        st.sidebar.metric(trait, score)

# Generate report button
if st.session_state.assessment_complete:
    if st.button("Generate Report"):
        scores = st.session_state.chatbot.get_scores()
        history = st.session_state.chatbot.conversation_history
        biodata = st.session_state.biodata
        report_gen = ReportGenerator(scores, history, biodata)
        text_report = report_gen.generate_text_report()
        st.text_area("Report", text_report, height=400)

        # PDF download
        pdf_file = report_gen.generate_pdf_report()
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF Report", f, file_name="recruitment_report.pdf")
