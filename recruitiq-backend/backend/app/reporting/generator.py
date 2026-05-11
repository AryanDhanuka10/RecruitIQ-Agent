import os
import json
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from jinja2 import Template

def generate_pdf_report(candidates: list, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    c = canvas.Canvas(output_path, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, 750, "RecruitIQ Agent - Shortlist Report")
    
    y = 710
    c.setFont("Helvetica", 12)
    for i, cand in enumerate(candidates):
        if y < 100:
            c.showPage()
            y = 750
            c.setFont("Helvetica", 12)
        
        name = cand.get("candidate_id", "Unknown")
        score = cand.get("weighted_total", 0)
        rec = cand.get("recommendation", "UNKNOWN")
        flags = cand.get("red_flags", [])
        
        c.drawString(50, y, f"{i+1}. {name}")
        y -= 20
        c.drawString(70, y, f"Score: {score}/10 | Recommendation: {rec}")
        y -= 20
        if flags:
            c.drawString(70, y, f"Red Flags: {', '.join(flags)}")
            y -= 20
        y -= 10
        
    c.save()
    print(f"PDF Report generated at {output_path}")

def generate_html_report(candidates: list, output_path: str):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    html_template = """
    <html>
    <head>
        <title>RecruitIQ Shortlist</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #333; }
            table { border-collapse: collapse; width: 100%; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            .red-flag { color: red; font-size: 0.9em; }
        </style>
    </head>
    <body>
        <h1>RecruitIQ Agent - Shortlist Report</h1>
        <table>
            <tr>
                <th>Rank</th>
                <th>Candidate Name</th>
                <th>Score</th>
                <th>Recommendation</th>
                <th>Red Flags</th>
            </tr>
            {% for cand in candidates %}
            <tr>
                <td>{{ loop.index }}</td>
                <td>{{ cand.candidate_id }}</td>
                <td>{{ cand.weighted_total }}/10</td>
                <td>{{ cand.recommendation }}</td>
                <td>
                    {% if cand.red_flags %}
                        <span class="red-flag">{{ cand.red_flags | join(', ') }}</span>
                    {% else %}
                        None
                    {% endif %}
                </td>
            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    """
    template = Template(html_template)
    html_content = template.render(candidates=candidates)
    
    with open(output_path, "w") as f:
        f.write(html_content)
    print(f"HTML Report generated at {output_path}")
