import xml.etree.ElementTree as ET
import tkinter as tk
import tkinter.filedialog as filedialog
from fpdf import FPDF

# Parse the XML file and create a list of spells
tree = ET.parse("./spells.xml")
root = tree.getroot()
spells = [spell for spell in root.findall("spell")]

# Create the GUI
root = tk.Tk()
root.title("D&D Spell Card Creator")

frame = tk.Frame(root)
frame.pack()

canvas = tk.Canvas(frame)
canvas.configure(scrollregion=(0,0,1000,1000))
canvas.pack()

frame_checkbox = tk.Frame(canvas)
canvas.create_window((0,0), window=frame_checkbox, anchor='nw')

# Create a label to display the title of the list
label = tk.Label(frame_checkbox, text="List of spells")
label.pack()

# Create a list of labels to display the spell names
spell_labels = []
selected_spells = []
for spell in spells:
    spell_name = spell.find("name").text
    spell_var = tk.StringVar()
    spell_checkbox = tk.Checkbutton(frame_checkbox, text=spell_name, variable=spell_var)
    spell_checkbox.pack()
    spell_labels.append(spell_checkbox)
    selected_spells.append(spell_var)
    
def generate_pdf():
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    for spell_var in selected_spells:
        if spell_var.get() == '1': # check if the spell is selected
            spell_index = selected_spells.index(spell_var)
            spell = spells[spell_index]
            spell_name = spell.find("name").text
            pdf.cell(0, 10, txt=spell_name, ln=1)
            pdf.cell(0, 10, txt=spell.find("School").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Level").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Range").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Save").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Duration").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Components").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Aoe").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Time").text, ln=1)
            pdf.cell(0, 10, txt=spell.find("Effect").text, ln=1)
    filepath = filedialog.asksaveasfilename(defaultextension='.pdf')
    pdf.output(filepath)

generate_pdf_button = tk.Button(frame_checkbox, text="Generate PDF", command=generate_pdf)
generate_pdf_button.pack()

root.mainloop()