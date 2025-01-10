import streamlit as st
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.piecharts import Pie
from io import BytesIO

# Function to create a pie chart
def create_pie_chart(data, labels):
    drawing = Drawing(200, 100)
    pie = Pie()
    pie.x = 50
    pie.y = 15
    pie.data = data
    pie.labels = labels
    pie.slices.strokeWidth = 0.5
    pie.slices.strokeColor = colors.black
    drawing.add(pie)
    return drawing

# Streamlit app
def main():
    st.title("Candidate One-Pager PDF Generator")
    
    # Input fields for candidate details
    candidate_name = st.text_input("Candidate Name")
    years_experience = st.number_input("Years of Experience", min_value=0, step=1)
    recent_position = st.text_input("Most Recent Position")
    key_skills = st.text_area("Key Skills (comma-separated)")
    notes = st.text_area("Additional Notes")
    
    # Example data for pie chart (customize based on skills or experience distribution)
    if key_skills:
        skills_list = [skill.strip() for skill in key_skills.split(",")]
        pie_data = [len(skill) for skill in skills_list]  # Example: Skill length as data points
        pie_labels = skills_list
    else:
        pie_data = []
        pie_labels = []

    if st.button("Generate PDF"):
        if candidate_name and recent_position:
            # Create PDF buffer
            buffer = BytesIO()
            doc = SimpleDocTemplate(buffer)
            styles = getSampleStyleSheet()
            
            elements = []
            
            # Title Section
            elements.append(Paragraph(f"Candidate Overview: {candidate_name}", styles["h1"]))
            elements.append(Spacer(1, 12))
            
            # Key Details Section
            elements.append(Paragraph(f"<b>Years of Experience:</b> {years_experience}", styles["Normal"]))
            elements.append(Paragraph(f"<b>Most Recent Position:</b> {recent_position}", styles["Normal"]))
            elements.append(Spacer(1, 12))
            
            # Key Skills Section
            if skills_list:
                elements.append(Paragraph("<b>Key Skills:</b>", styles["h2"]))
                for skill in skills_list:
                    elements.append(Paragraph(f"- {skill}", styles["Normal"]))
                elements.append(Spacer(1, 12))
            
            # Additional Notes Section
            if notes:
                elements.append(Paragraph("<b>Additional Notes:</b>", styles["h2"]))
                elements.append(Paragraph(notes, styles["Normal"]))
                elements.append(Spacer(1, 12))
            
            # Pie Chart Section (if data exists)
            if pie_data and pie_labels:
                elements.append(Paragraph("<b>Skill Distribution:</b>", styles["h2"]))
                chart = create_pie_chart(pie_data, pie_labels)
                elements.append(chart)
                elements.append(Spacer(1, 12))
            
            # Build PDF and provide download link
            doc.build(elements)
            buffer.seek(0)
            
            st.download_button(
                label="Download Candidate One-Pager PDF",
                data=buffer,
                file_name=f"{candidate_name.replace(' ', '_')}_one_pager.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Please fill in all required fields.")

if __name__ == "__main__":
    main()
