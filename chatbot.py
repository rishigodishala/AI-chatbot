import os
from langchain.prompts import PromptTemplate
from rag_engine import RAGEngine
from mcp_module import MCPModule

class RecruitmentChatbot:
    def __init__(self):
        self.llm = MockLLM()  # Use mock for testing; replace with OpenAI(temperature=0.7, model="gpt-4") for real
        self.rag = RAGEngine()
        self.mcp = MCPModule()
        self.conversation_history = []
        self.biodata = {}
        self.scores = {
            "Openness": 0,
            "Conscientiousness": 0,
            "Extraversion": 0,
            "Agreeableness": 0,
            "Neuroticism": 0,
            "Authenticity": 0
        }
        self.question_count = 0
        self.max_questions = 10
        self.fixed_biodata_questions = [
            "What is your full name?",
            "How old are you?",
            "What is your current job title and years of experience? (If student, mention field of study.)"
        ]

    def generate_question(self):
        if self.question_count >= self.max_questions:
            return None

        if self.question_count < 3:
            # Fixed biodata questions
            question = self.fixed_biodata_questions[self.question_count]
        else:
            # Adaptive behavioral questions using LLM
            context = self.rag.retrieve("behavioral questions for personality assessment in recruitment", k=2)
            context_str = "\n".join(context)

            history_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])  # Last 3 exchanges
            biodata_str = str(self.biodata)

            prompt = PromptTemplate(
                input_variables=["context", "history", "biodata", "scores", "prev_topics"],
                template="""
                You are generating adaptive behavioral questions for a recruitment personality assessment based on Big Five traits.
                Total behavioral questions: 7 (after 3 biodata). Avoid repetition.

                Context from HR frameworks:
                {context}

                Biodata: {biodata}
                (Adapt questions: if no work experience, use academic/personal examples; if student, focus on studies/projects.)

                Recent history:
                {history}

                Current scores: {scores}

                Previous topics covered: {prev_topics} (Avoid these.)

                Generate one open-ended, probing question to assess traits like Openness, Conscientiousness, etc. Make it relevant to user's background.
                Question:
                """
            )

            # Track previous topics (simple string for mock)
            prev_topics = "biodata, challenges" if self.question_count > 3 else "biodata"

            formatted_prompt = prompt.format(
                context=context_str,
                history=history_str,
                biodata=biodata_str,
                scores=str(self.scores),
                prev_topics=prev_topics
            )
            question = self.llm(formatted_prompt)
            question = question.strip()

        self.question_count += 1
        return question

    def analyze_response(self, response):
        if self.question_count <= 3:
            # Biodata collection
            if self.question_count == 1:
                self.biodata['name'] = response
            elif self.question_count == 2:
                self.biodata['age'] = response
            elif self.question_count == 3:
                self.biodata['job'] = response
            return "Biodata recorded."

        # Adaptive analysis using LLM, considering biodata
        context = self.rag.retrieve("analyzing responses for Big Five traits", k=2)
        context_str = "\n".join(context)

        history_str = "\n".join([f"Q: {q}\nA: {a}" for q, a in self.conversation_history[-3:]])
        biodata_str = str(self.biodata)

        prompt = PromptTemplate(
            input_variables=["context", "response", "history", "biodata"],
            template="""
            Analyze the response for Big Five traits and authenticity, considering biodata.

            Context:
            {context}

            Biodata: {biodata} (Tailor analysis: e.g., for students, evaluate academic/personal behaviors.)

            Response: {response}

            History: {history}

            Update scores (0-10). Detect inconsistencies for authenticity.
            Output: Openness: X, Conscientiousness: X, Extraversion: X, Agreeableness: X, Neuroticism: X, Authenticity: X
            Explanation: [brief, adaptive insights]
            """
        )

        formatted_prompt = prompt.format(
            context=context_str,
            response=response,
            history=history_str,
            biodata=biodata_str
        )
        analysis = self.llm(formatted_prompt)

        # Parse scores from mock output
        lines = analysis.split('\n')
        scores_line = next((line for line in lines if any(trait in line for trait in self.scores)), "")
        explanation_line = next((line for line in lines if 'Explanation:' in line), lines[-1] if lines else "")

        if scores_line:
            parts = [p.strip() for p in scores_line.split(',')]
            for part in parts:
                if ':' in part:
                    trait, value = part.split(':', 1)
                    trait = trait.strip()
                    value = value.strip()
                    if trait in self.scores:
                        try:
                            self.scores[trait] = float(value)
                        except ValueError:
                            self.scores[trait] = 5.0  # Default

        explanation = explanation_line.replace("Explanation: ", "").strip() if explanation_line else "Analysis complete."
        return explanation

    def chat(self, user_input):
        if user_input.lower() in ['start', 'begin']:
            self.conversation_history = []
            self.biodata = {}
            self.scores = {k: 0 for k in self.scores}
            self.question_count = 0
            question = self.generate_question()
            self.conversation_history.append(("System", "Assessment started"))
            return f"Welcome to the recruitment assessment. Let's begin.\n\n{question}"

        # Store response
        prev_question = self.conversation_history[-1][0] if self.conversation_history and self.conversation_history[-1][0] != "System" else "Initial"
        self.conversation_history.append((prev_question, user_input))

        explanation = self.analyze_response(user_input)

        if self.question_count >= self.max_questions:
            return f"Assessment complete.\n{explanation}\n\nFinal Scores: {self.scores}"

        next_question = self.generate_question()
        return f"{explanation}\n\n{next_question}"

    def get_scores(self):
        return self.scores

class MockLLM:
    def __init__(self):
        self.mock_question_index = 0
        self.student_questions = [
            "Describe a challenging situation in your studies or personal projects and how you handled it.",
            "How do you typically react to constructive criticism in group projects or academic settings?",
            "Tell me about a time when you collaborated on a school or personal project.",
            "What motivates you in your academic or personal pursuits?",
            "How do you handle stress during exams or deadlines?",
            "Describe your ideal learning or collaborative environment.",
            "What are your key strengths and how do you apply them in team settings?",
            "Reflect on a time you received feedback and how it impacted you."
        ]
        self.professional_questions = [
            "Describe a challenging situation at work and how you handled it.",
            "How do you typically react to constructive criticism from your manager or colleagues?",
            "Tell me about a time when you collaborated on a professional project.",
            "What motivates you in your career or daily work?",
            "How do you handle stress during tight deadlines or high-pressure projects?",
            "Describe your ideal work or collaborative environment.",
            "What are your key strengths and how do you apply them in team settings at work?",
            "Reflect on a time you received feedback at work and how it impacted you."
        ]
        self.mock_analyses = [
            "Openness: 7, Conscientiousness: 6, Extraversion: 5, Agreeableness: 8, Neuroticism: 4, Authenticity: 9\nExplanation: Response indicates good problem-solving in professional context, high agreeableness in teams.",
            "Openness: 6, Conscientiousness: 7, Extraversion: 5, Agreeableness: 7, Neuroticism: 3, Authenticity: 8\nExplanation: Strong conscientiousness shown in handling work challenges.",
            "Openness: 8, Conscientiousness: 5, Extraversion: 7, Agreeableness: 6, Neuroticism: 4, Authenticity: 9\nExplanation: High openness to feedback and extraversion in professional collaboration.",
            "Openness: 5, Conscientiousness: 8, Extraversion: 4, Agreeableness: 9, Neuroticism: 2, Authenticity: 10\nExplanation: Motivation driven by career goals, high agreeableness.",
            "Openness: 7, Conscientiousness: 9, Extraversion: 6, Agreeableness: 8, Neuroticism: 5, Authenticity: 8\nExplanation: Effective stress management in work settings, low neuroticism.",
            "Openness: 6, Conscientiousness: 7, Extraversion: 8, Agreeableness: 7, Neuroticism: 3, Authenticity: 9\nExplanation: Prefers dynamic work environments, high extraversion.",
            "Openness: 9, Conscientiousness: 6, Extraversion: 5, Agreeableness: 8, Neuroticism: 4, Authenticity: 10\nExplanation: Creative strengths with professional team focus."
        ]

    def __call__(self, prompt):
        if "Question:" in prompt and "Biodata" in prompt:
            # Adaptive question generation
            biodata_str = prompt.split("Biodata: ")[1].split("\n")[0] if "Biodata: " in prompt else ""
            is_professional = "experience" in biodata_str.lower() and "student" not in biodata_str.lower()
            if is_professional:
                q = self.professional_questions[self.mock_question_index % len(self.professional_questions)]
            else:
                q = self.student_questions[self.mock_question_index % len(self.student_questions)]
            self.mock_question_index += 1
            return q
        elif "Analyze" in prompt:
            # Analysis
            analysis = self.mock_analyses[self.mock_question_index % len(self.mock_analyses)]
            return analysis
        return "Mock response"
