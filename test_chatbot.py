import os
from chatbot import RecruitmentChatbot
from report_generator import ReportGenerator

# Simulate full assessment for student and professional
def simulate_assessment(biodata_type="professional"):
    chatbot = RecruitmentChatbot()
    print(f"\n=== Starting {biodata_type.capitalize()} Assessment ===")
    
    # Step 1: Start
    response = chatbot.chat("start")
    print("Bot:", response)
    
    # Step 2: Answer 3 biodata questions
    if biodata_type == "student":
        biodata_answers = [
            "Jane Student",  # Name
            "20",            # Age
            "Computer Science student"  # Job
        ]
    else:
        biodata_answers = [
            "John Doe",  # Name
            "25",        # Age
            "Software Engineer with 3 years experience"  # Job
        ]
    
    for answer in biodata_answers:
        response = chatbot.chat(answer)
        print("User:", answer)
        print("Bot:", response)
    
    # Step 3: Answer 7 behavioral questions with sample responses
    behavioral_answers = [
        "I faced a tight deadline on a project and stayed late to complete it, collaborating with my team.",
        "I listen to feedback and adjust my approach, like when a reviewer suggested changes to my code.",
        "In a group project, I organized meetings and ensured everyone contributed equally.",
        "I'm motivated by solving complex problems and seeing the impact on users.",
        "I prioritize tasks and take breaks to manage stress during high-pressure periods.",
        "I thrive in collaborative, innovative environments where ideas are shared freely.",
        "My key strength is problem-solving; I apply it by debugging issues in team codebases."
    ]
    
    questions_asked = []
    for i, answer in enumerate(behavioral_answers):
        # The bot response includes the question before analysis
        response = chatbot.chat(answer)
        print(f"User (Q{i+1}):", answer)
        print("Bot:", response)
        if "Assessment complete" in response:
            break
        # Extract question from response (before analysis)
        if '\n\n' in response:
            question_part = response.split('\n\n')[0]
            questions_asked.append(question_part)
    
    print(f"\nQuestions asked for {biodata_type}:")
    for q in questions_asked:
        print(f"- {q}")
    
    # Final scores
    scores = chatbot.get_scores()
    print(f"\n=== Final Scores ({biodata_type}) ===")
    for trait, score in scores.items():
        print(f"{trait}: {score}")
    
    # Step 4: Generate reports (skip full print for brevity in dual run)
    history = chatbot.conversation_history
    biodata = chatbot.biodata
    report_gen = ReportGenerator(scores, history, biodata)
    text_report = report_gen.generate_text_report()
    print(f"\nText Report Preview ({biodata_type}):")
    print(text_report[:300] + "..." if len(text_report) > 300 else text_report)
    
    # Generate PDF
    pdf_file = report_gen.generate_pdf_report(f"report_{biodata_type}.pdf")
    print(f"PDF Report generated: {pdf_file}\n")
    
    return True

if __name__ == "__main__":
    print("=== Student Simulation ===")
    success_student = simulate_assessment("student")
    print("=== Professional Simulation ===")
    success_prof = simulate_assessment("professional")
    if success_student and success_prof:
        print("\n=== Both Simulations Completed Successfully ===")
    else:
        print("\n=== Simulations Failed ===")
