import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
import matplotlib.pyplot as plt
import base64
from io import BytesIO

class ReportGenerator:
    def __init__(self, scores, history, biodata=None):
        self.scores = scores
        self.history = history
        self.biodata = biodata or {}

    def generate_text_report(self):
        report = "Recruitment Personality Assessment Report\n\n"
        if self.biodata:
            report += "Biodata:\n"
            for key, value in self.biodata.items():
                report += f"{key.capitalize()}: {value}\n"
            report += "\n"

        report += "Big Five Traits Scores (0-10):\n"
        for trait, score in self.scores.items():
            if trait != "Authenticity":
                report += f"{trait}: {score}\n"
        report += f"\nAuthenticity Score: {self.scores['Authenticity']}\n\n"

        # Enhanced Strengths and Recommendations
        strengths = []
        recommendations = []

        # Strengths based on high scores (>7)
        if self.scores["Openness"] > 7:
            strengths.append("High Openness: Creative, open to new ideas, and adaptable to change.")
        elif self.scores["Openness"] > 4:
            strengths.append("Moderate Openness: Balanced creativity and practicality.")
        else:
            recommendations.append("Low Openness: May benefit from exposure to new experiences.")

        if self.scores["Conscientiousness"] > 7:
            strengths.append("High Conscientiousness: Organized, reliable, and goal-oriented.")
        elif self.scores["Conscientiousness"] > 4:
            strengths.append("Moderate Conscientiousness: Dependable with room for structure.")
        else:
            recommendations.append("Low Conscientiousness: Develop time management skills.")

        if self.scores["Extraversion"] > 7:
            strengths.append("High Extraversion: Outgoing, energetic, and thrives in social settings.")
        elif self.scores["Extraversion"] > 4:
            strengths.append("Moderate Extraversion: Balanced social and independent work.")
        else:
            recommendations.append("Low Extraversion: Consider roles with independent tasks.")

        if self.scores["Agreeableness"] > 7:
            strengths.append("High Agreeableness: Cooperative, empathetic, and team player.")
        elif self.scores["Agreeableness"] > 4:
            strengths.append("Moderate Agreeableness: Collaborative with assertiveness.")
        else:
            recommendations.append("Low Agreeableness: Work on conflict resolution.")

        if self.scores["Neuroticism"] < 3:
            strengths.append("Low Neuroticism: Emotionally stable and resilient under pressure.")
        elif self.scores["Neuroticism"] < 7:
            strengths.append("Moderate Neuroticism: Handles stress well overall.")
        else:
            recommendations.append("High Neuroticism: Stress management techniques recommended.")

        if self.scores["Authenticity"] > 7:
            strengths.append("High Authenticity: Responses appear genuine and consistent.")
        else:
            recommendations.append("Moderate Authenticity: Follow-up verification suggested.")

        report += "Strengths:\n" + "\n".join(strengths) + "\n\n"
        report += "Recommendations:\n" + "\n".join(recommendations) + "\n\n"

        # Assessment Summary
        report += "Assessment Summary:\n"
        report += "This assessment evaluates personality traits using the Big Five model, tailored to the candidate's background. "
        report += "Scores indicate potential fit for roles requiring specific behaviors, such as teamwork (high Agreeableness) or innovation (high Openness). "
        report += "For students or entry-level candidates, focus on academic and personal experiences highlights transferable skills.\n\n"

        report += "Conversation Summary:\n"
        for i, (q, a) in enumerate(self.history):
            if q != "System":
                report += f"Q{i+1}: {q}\nA{i+1}: {a}\n\n"

        return report

    def generate_chart(self):
        traits = [k for k in self.scores.keys() if k != "Authenticity"]
        values = [self.scores[t] for t in traits]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(traits, values, color=['blue', 'green', 'orange', 'purple', 'red'])
        ax.set_ylabel('Score')
        ax.set_title('Big Five Personality Traits')
        ax.set_ylim(0, 10)
        plt.xticks(rotation=45, ha='right')

        buf = BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        img_data = buf.read()
        plt.close(fig)
        return img_data

    def generate_pdf_report(self, filename="report.pdf"):
        text_report = self.generate_text_report()
        chart_img = self.generate_chart()

        c = canvas.Canvas(filename, pagesize=letter)
        width, height = letter

        # Title
        c.setFont("Helvetica-Bold", 16)
        c.drawString(100, height - 100, "Recruitment Personality Assessment Report")

        # Biodata
        y = height - 150
        if self.biodata:
            c.setFont("Helvetica", 12)
            c.drawString(100, y, "Biodata:")
            y -= 20
            for key, value in self.biodata.items():
                c.drawString(120, y, f"{key.capitalize()}: {value}")
                y -= 20

        # Scores
        y -= 20
        c.drawString(100, y, "Big Five Traits Scores:")
        y -= 20
        for trait, score in self.scores.items():
            if trait != "Authenticity":
                c.drawString(120, y, f"{trait}: {score}")
                y -= 15
        c.drawString(120, y, f"Authenticity: {self.scores['Authenticity']}")
        y -= 30

        # Embed chart image
        img = ImageReader(io.BytesIO(chart_img))
        c.drawImage(img, 100, y - 200, width=400, height=200, preserveAspectRatio=True)
        y -= 250

        # Strengths and Recommendations (truncated for PDF simplicity)
        c.drawString(100, y, "Strengths and Recommendations: See text report for details.")
        y -= 20
        c.drawString(100, y, "Assessment covers all traits comprehensively based on responses.")

        c.save()
        return filename
