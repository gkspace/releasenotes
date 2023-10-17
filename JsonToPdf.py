import json
import os
import re
from fpdf import FPDF
from unidecode import unidecode

def insert_spaces(text):
    # Use regular expressions to insert spaces before capital letters
    text = re.sub(r"([A-Z])", r" \1", text)
    return text.capitalize()

def json_to_pdf(filename, sprint_id,releaseVersion, testType, instancesTested, platformOsVersion, apiVersion, releaseDate, releaseType):
     # Load JSON data from file
    with open(filename, 'r', encoding='utf-8') as file:
        extracted_values = json.load(file)

    # Initialize PDF object
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True)  # Disable auto-page break


    pdf.add_page()
    pdf.set_font("Arial", size=15, style='B')

    # Add subheading to PDF
    pdf.cell(0, 10, sprint_id , 0, 1,'C' )
    pdf.ln()
    # Set font
    pdf.set_font("Arial", size=9)

    # Adding sprint details to the table
    details = [
            ("Release Version",releaseVersion),
            ("Test Type", testType),
            ("Instances Tested", instancesTested),
            ("Platform & OS version", platformOsVersion),
            ("API version", apiVersion),
            ("Release Date", releaseDate),
            ("Release Type", releaseVersion),
        ]

    # Define colors
    blue_color = (173, 206, 230)
    grey_color = (255, 255, 255)
    for label, value in details:
        # Set fill color for the first column (blue)
        pdf.set_fill_color(*blue_color)
        pdf.cell(95, 10, label, 1, 0, 'C', 1)
            
        # Set fill color for the second column (grey)
        pdf.set_fill_color(*grey_color)
        pdf.cell(95, 10, value, 1, 1, 'C', 1)
        
        # Reset fill color for the next row
        pdf.set_fill_color(255, 255, 255)

    pdf.ln()
    # Function to add issues to PDF
    def add_issues_to_pdf(subheading, issues):
        if not issues:
            return False  
        
        # Seting font with style 'B' (bold) just for printing the heading
        pdf.set_font("Arial", size=10, style='B')

        # Add subheading to PDF
        pdf.cell(0, 10, subheading, 0, 1 )


         # Setting font back to regular style after printing the heading
        pdf.set_font("Arial", size=9)


        # Adding extracted issues data
        for issue in issues:
            # Creating a single line string with 'Key' and 'Summary' information
            issue_info = f"{issue['key']} - {issue['summary']}"
            issue_info = unidecode(issue_info)

            # Add the issue information to the PDF
            pdf.multi_cell(0, 10, issue_info)

        return True 

    for heading, issues in extracted_values.items():


        if not any(issues):
            continue

        # Add a new page for the different section
       # pdf.add_page()
        
        # Setying font with style 'B' (bold) just for printing the heading
        pdf.set_font("Arial", size=12, style='B')

        # Change the title based on sprint data
        if heading == "puntedIssues":
            heading = "Issues Removed From Sprint"

        # Add heading to PDF on the new page
        pdf.cell(0, 10, insert_spaces(heading), 0, 1, 'C')
        pdf.ln()
        
        # Set font back to regular style after printing the heading
        pdf.set_font("Arial", size=9)

        # Group issues by type ID under the  section
        issues_by_type = {}
        for issue in issues:
            typeid = issue['typeid']
            if typeid not in issues_by_type:
                issues_by_type[typeid] = []
            issues_by_type[typeid].append(issue)

        # Add extracted issues data to PDF for each type under  heading
        for typeid, type_issues in issues_by_type.items():
            # Get the subheading based on the typeid
            subheading = typeid  
            if not add_issues_to_pdf(subheading, type_issues):
                # If no issues for the subheading, remove the last added subheading and newline
                pdf.cell(0, 10, "", 0, 1, 'C')
                pdf.cell(0, 10, "", 0, 1, 'C')

    # Save the PDF file
    pdf_filename = f"{sprint_id}.pdf"
    pdf.output(pdf_filename,'F')

    # Delete the JSON file
    os.remove(filename)

    print(f"Data saved to '{pdf_filename}'")