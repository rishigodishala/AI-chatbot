AI-Driven Recruitment Personality Assessment Chatbot

An intelligent chatbot system for recruitment personality assessments using AI, RAG (Retrieval-Augmented Generation), and multi-channel processing (MCP) to evaluate candidates based on Big Five personality traits.

Features

Adaptive Assessment: Dynamically generates behavioral questions based on candidate background (student vs. professional)
Big Five Traits Evaluation: Assesses Openness, Conscientiousness, Extraversion, Agreeableness, and Neuroticism
Authenticity Scoring: Detects response consistency and potential inconsistencies
RAG Integration: Uses retrieval-augmented generation with HR frameworks (Big Five, DISC, Emotional Intelligence)
Multi-Channel Processing: Placeholder for facial and voice emotion analysis (future enhancement)
Report Generation: Generates detailed text and PDF reports with scores, strengths, and recommendations
Streamlit UI: User-friendly web interface for the assessment

Project Structure

chatbot/
├── app.py                 Main Streamlit web application
├── chatbot.py             Main chatbot logic with adaptive questioning
├── rag_engine.py          RAG engine for retrieving HR context
├── mcp_module.py          Multi-channel processing module (placeholders)
├── report_generator.py    Report generation (text and PDF)
├── test_chatbot.py        Test script for chatbot simulation
├── requirements.txt       Python dependencies
├── TODO.md               Project tasks and progress
├── data/                 RAG data files
│   ├── big_five.txt
│   ├── disc_model.txt
│   └── emotional_intelligence.txt
└── README.md             This file

Installation

1. Clone the repository:
   git clone https://github.com/rishigodishala/AI-chatbot.git
   cd AI-chatbot

2. Install dependencies:
   pip install -r requirements.txt

3. Set up OpenAI API key:
   Create a .env file in the root directory
   Add your OpenAI API key: OPENAI_API_KEY=your_api_key_here

Usage

Running the Chatbot

Start the Streamlit application:
streamlit run app.py

Navigate to the provided URL (usually http://localhost:8501) in your browser.

Assessment Flow

1. Type "start" to begin the assessment
2. Answer 3 biodata questions (name, age, job/experience)
3. Answer 7 adaptive behavioral questions
4. View scores in the sidebar during assessment
5. Generate and download reports upon completion

Testing

Run the test script to simulate assessments:
python test_chatbot.py

This will run both student and professional assessment simulations.

Dependencies

streamlit: Web UI framework
langchain: LLM framework for RAG
openai: OpenAI API integration
faiss-cpu: Vector database for RAG
pandas: Data manipulation
matplotlib: Chart generation
reportlab: PDF report generation
pyAudioAnalysis: Audio feature extraction (future use)
librosa: Audio processing (future use)
opencv-python: Computer vision (future use)
fer: Facial emotion recognition (future use)

Assessment Methodology

Big Five Traits
Openness: Creativity, curiosity, openness to experience
Conscientiousness: Organization, reliability, goal-directedness
Extraversion: Sociability, energy, assertiveness
Agreeableness: Cooperation, empathy, altruism
Neuroticism: Emotional stability, anxiety levels

Adaptive Questioning
Questions adapt based on biodata (student vs. professional background)
Uses RAG to retrieve relevant HR frameworks
Analyzes responses for trait scoring and authenticity

Scoring
Traits scored 0-10 based on responses
Authenticity score evaluates response consistency
Reports include strengths and development recommendations

Future Enhancements

Implement real facial emotion recognition
Add voice emotion analysis
Integrate video/audio input capabilities
Add more comprehensive RAG data
Implement advanced NLP for deeper response analysis
Add multi-language support
Integrate with ATS (Applicant Tracking Systems)

Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

License

This project is licensed under the MIT License - see the LICENSE file for details.

Contact

For questions or feedback, please open an issue on GitHub.
