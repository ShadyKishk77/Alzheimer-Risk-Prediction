from fpdf import FPDF
from datetime import datetime


class PDFReport(FPDF):
    def header(self):
        # Header with Logo text
        self.set_font('Arial', 'B', 15)
        self.set_text_color(99, 102, 241)  # Primary color from your CSS
        self.cell(0, 10, 'NeuroPredict AI - Risk Assessment Report', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')


def generate_report(input_data, result):
    pdf = PDFReport()
    pdf.add_page()

    # 1. Prediction Summary
    pdf.set_font('Arial', 'B', 12)
    pdf.set_text_color(0)
    pdf.cell(0, 10, f'Assessment Date: {datetime.now().strftime("%Y-%m-%d %H:%M")}', 0, 1)
    pdf.ln(5)

    # Result Box
    status = "Elevated Risk Detected" if result['is_positive'] else "Low Risk Profile"
    color = (239, 68, 68) if result['is_positive'] else (16, 185, 129)  # Red or Green

    pdf.set_fill_color(*color)
    pdf.set_text_color(255)
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 15, f"{status} ({result['probability'] * 100:.1f}%)", 0, 1, 'C', 1)

    # Disclaimer
    pdf.ln(5)
    pdf.set_text_color(100)
    pdf.set_font('Arial', 'I', 9)
    pdf.multi_cell(0, 5,
                   "Disclaimer: This tool is for educational and screening purposes only. It does not constitute medical advice.")

    # 2. Patient data
    pdf.ln(10)
    pdf.set_text_color(0)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, 'Patient data Input:', 0, 1)

    pdf.set_font('Arial', '', 10)

    # Iterate through inputs nicely
    col_width = pdf.w / 2.2
    for key, value in input_data.items():
        # Clean up key name (e.g., 'SystolicBP' -> 'Systolic BP')
        clean_key = key
        pdf.cell(col_width, 8, f"{clean_key}: {value}", 1)
        # Simple logic to create 2 columns
        if pdf.get_x() > pdf.w - 30:
            pdf.ln()

    return bytes(pdf.output(dest='S'))