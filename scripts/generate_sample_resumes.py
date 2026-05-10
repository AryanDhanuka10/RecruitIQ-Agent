import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

RESUMES = [
    {
        "filename": "john_doe_ml.pdf",
        "content": [
            "John Doe",
            "Email: john.doe@email.com | Phone: 555-123-4567 | Location: New York, NY",
            "",
            "Objective: Senior Machine Learning Engineer with 5 years of experience.",
            "Skills: Python, PyTorch, LangChain, MLflow, Docker",
            "Education: M.S. in Computer Science, NYU",
            "Experience:",
            "- Senior ML Engineer at TechCorp (2020-Present)",
            "- Built RAG pipelines using LangChain and FAISS.",
            "Projects: Deployed Llama-2 models on AWS SageMaker."
        ]
    },
    {
        "filename": "alice_smith_data.pdf",
        "content": [
            "Alice Smith",
            "Email: alice.smith@data.com | Phone: 555-987-6543 | Location: San Francisco, CA",
            "",
            "Objective: Data Scientist specializing in NLP.",
            "Skills: Python, TensorFlow, scikit-learn, SQL",
            "Education: B.S. in Data Science, UC Berkeley",
            "Experience:",
            "- Data Scientist at DataInc (2018-2023)",
            "Projects: Sentiment analysis using BERT."
        ]
    },
    {
        "filename": "bob_jones_backend.pdf",
        "content": [
            "Bob Jones",
            "Email: bob.j@backend.net | Phone: 555-555-5555 | Location: Austin, TX",
            "",
            "Objective: Backend Developer looking to transition into AI.",
            "Skills: Java, Spring Boot, Python, FastAPI",
            "Education: B.A. in Mathematics, UT Austin",
            "Experience:",
            "- Backend Dev at WebSolutions (2019-Present)",
            "Projects: Created REST APIs for an e-commerce platform."
        ]
    },
    {
        "filename": "charlie_brown_ml.pdf",
        "content": [
            "Charlie Brown",
            "Email: cbrown@peanuts.org | Phone: 555-111-2222 | Location: Chicago, IL",
            "",
            "Objective: Lead AI Engineer with 8 years experience.",
            "Skills: Python, C++, CUDA, PyTorch, Kubernetes",
            "Education: Ph.D. in AI, UChicago",
            "Experience:",
            "- AI Researcher at DeepTech (2016-Present)",
            "Projects: Developed custom transformer architectures for computer vision."
        ]
    },
    {
        "filename": "diana_prince_fullstack.pdf",
        "content": [
            "Diana Prince",
            "Email: diana.p@themyscira.com | Phone: 555-999-8888 | Location: Washington, D.C.",
            "",
            "Objective: Fullstack Developer exploring LLMs.",
            "Skills: JavaScript, React, Node.js, Python",
            "Education: B.S. in Software Engineering, MIT",
            "Experience:",
            "- Fullstack Engineer at JusticeWeb (2021-Present)",
            "Projects: Built a chatbot UI using React and OpenAI API."
        ]
    }
]

def generate():
    os.makedirs("data/sample_resumes", exist_ok=True)
    for resume in RESUMES:
        filepath = os.path.join("data/sample_resumes", resume["filename"])
        c = canvas.Canvas(filepath, pagesize=letter)
        y = 750
        for line in resume["content"]:
            c.drawString(50, y, line)
            y -= 20
        c.save()
    print("Generated 5 sample PDF resumes.")

if __name__ == "__main__":
    generate()
