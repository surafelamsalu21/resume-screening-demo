from fpdf import FPDF

# Load the structured resumes text file
resume_file_path = "./structured_random_resumes.txt"
with open(resume_file_path, "r") as file:
    resumes = file.read().split("\n\n")  # Split the file into individual resumes

# Initialize PDF generator
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Resume', align='C', ln=True)
        self.ln(10)

    def add_resume(self, resume_content):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, resume_content)
        self.ln(10)

# Create PDFs for each resume
for resume in resumes:
    # Extract the name for the PDF filename
    lines = resume.split("\n")
    name_line = [line for line in lines if line.startswith("Name:")][0]
    name = name_line.split(": ")[1].strip().replace(" ", "_")  # Use underscores for filename

    # Generate PDF
    pdf = PDF()
    pdf.add_page()
    pdf.add_resume(resume)

    # Save the PDF
    pdf_file_path = f"./PDF/{name}.pdf"
    pdf.output(pdf_file_path)

"./PDF"  # Return directory path where PDFs are saved
