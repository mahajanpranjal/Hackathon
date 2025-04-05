from fpdf import FPDF
import unicodedata
import os

def sanitize_text(text):
    """Convert Unicode smart characters to ASCII equivalents"""
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def save_report_as_pdf(report_text, filename="downloaded_report.pdf", images=None):
    os.makedirs("static/reports", exist_ok=True)
    full_path = os.path.join("static/reports", filename)

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add report content
    for line in report_text.split("\n"):
        safe_line = sanitize_text(line)
        pdf.multi_cell(190, 10, txt=safe_line, align='L')

    # Add any images (charts)
    if images:
        for image_path in images:
            if os.path.exists(image_path):
                pdf.add_page()
                pdf.image(image_path, x=10, y=30, w=180)
            else:
                print(f"⚠️ Image not found: {image_path}")

    pdf.output(full_path)
    print(f"✅ Report with image(s) saved as {full_path}")
    return filename
