import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import qrcode
import barcode
from barcode.writer import ImageWriter
import os
import glob
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk  # Importing Image and ImageTk from Pillow

data = pd.DataFrame()
def loadData(csv_file):
    global data
    data = pd.read_csv(csv_file)
def delete_all_files_in_folder(folder_path):
    # Get a list of all files in the folder (excluding subdirectories)
    files = glob.glob(os.path.join(folder_path, "*"))

    for file in files:
        try:
            if os.path.isfile(file):  # Ensure it's a file, not a directory
                os.remove(file)
            else:
                print(f"Skipping directory: {file}")
        except Exception as e:
            print(f"Error deleting {file}: {e}")
def getData(index):
    barcode_data = str(data["PART NO"].iloc[index]) + ", " + data["OEM"].iloc[index]
    product_name = str(data["PART NO"].iloc[index])
    product_info = str(data["DESCRIPTION"].iloc[index])
    manufacturer = data["OEM"].iloc[index]
    qty = str(data["Qty"].iloc[index])
    qr_data = barcode_data
    tc = "T&C.png"
    return barcode_data, product_name, product_info, qr_data, manufacturer, qty, tc
def resize_image_with_aspect_ratio(image_path, desired_width, desired_height):
    # Open the image
    img = Image.open(image_path)
    # Get the original dimensions
    original_width, original_height = img.size
    # Calculate the aspect ratio
    aspect_ratio = original_width / original_height
    # Calculate new dimensions while maintaining aspect ratio
    if desired_width / desired_height > aspect_ratio:
        # If the desired aspect ratio is wider than the original, adjust height
        new_height = desired_height
        new_width = int(new_height * aspect_ratio)
    else:
        # If the desired aspect ratio is taller than the original, adjust width
        new_width = desired_width
        new_height = int(new_width / aspect_ratio)
    # Return the new dimensions
    return new_width, new_height
# Function to create a barcode and draw it on the canvas
def generate_barcode(bar_data, file_path):
    barcode_type = barcode.get_barcode_class('code128')
    barcode_data = bar_data
    my_barcode = barcode_type(barcode_data, writer=ImageWriter())
    options = {"write_text": False}
    # Save the barcode as an image
    my_barcode.save(file_path, options)
# Function to create a QR code and save it as an image
def generate_qrcode(data, file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
    qr = qrcode.QRCode(version=1, box_size=10, border=1)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill='black', back_color='white')
    img.save(file_path)
# For Multiple Line Description
def draw_multiline_paragraph(c, x, y, text, max_width):
    """
    Draws multiline text using ReportLab's Paragraph.

    Parameters:
        c (canvas): ReportLab canvas object.
        x, y (float): Starting position for the paragraph.
        text (str): Text to draw.
        max_width (float): Maximum width for the paragraph in points.
    """
    # Get a basic style for the paragraph
    styles = getSampleStyleSheet()
    style = styles["Normal"]
    style.fontName = "Helvetica"
    style.fontSize = 8
    style.leading = 10  # Line height

    # Create a paragraph
    paragraph = Paragraph(text, style)

    # Set up a frame to fit the paragraph
    from reportlab.platypus import Frame
    frame = Frame(x, y - 100, max_width, 200)  # Adjust height and position as needed
    frame.addFromList([paragraph], c)
def generateSticker(height, sticker_width, sticker_height, c, index, stckr_x, stckr_y, cntnt_x, cntnt_y, qr_x):
    barcode_data, product_name, product_info, qr_data, manufacturer, qty, tc = getData(index)
    # ------------------------------------- STICKER 01 -------------------------------------
    # Draw border around the sticker
    sticker_x = stckr_x
    sticker_y = height - stckr_y
    c.setStrokeColor("black")
    c.setLineWidth(1)
    c.rect(sticker_x, sticker_y, sticker_width, -sticker_height, stroke=True, fill=False)

    # Barcode
    bar_path = "Bars/" + str(index)
    generate_barcode(barcode_data, bar_path)
    bar_path = bar_path + ".png"
    bar_width, bar_height = resize_image_with_aspect_ratio(bar_path, 170, 32)
    c.drawImage(bar_path, cntnt_x, height - cntnt_y, width=bar_width, height=bar_height)

    # Product Info
    c.setFont("Times-Roman", 10)
    c.drawString(cntnt_x, height - (cntnt_y + 12), f"Part No: {product_name}")
    c.drawString(cntnt_x, height - (cntnt_y + 24), f"Qty: {qty}")
    draw_multiline_paragraph(c, cntnt_x - 5, height - (cntnt_y + 120), "Manufacturer: " + manufacturer, 180)
    draw_multiline_paragraph(c, cntnt_x - 5, height - (cntnt_y + 144), "Description: " + product_info, 250)

    # QR Code
    qr_code_path = "QRs/" + str(index) + ".png"
    generate_qrcode(qr_data, qr_code_path)
    c.drawImage(qr_code_path, qr_x, height - (cntnt_y + 36), width=72, height=72)
    c.drawImage(tc, cntnt_x, height - (cntnt_y + 124), width=245, height=30)
def generate_pdf(pdf_filename):
    c = canvas.Canvas(pdf_filename, pagesize=A4)
    width, height = A4

    total_rows = len(data)
    sticker_width = 260
    sticker_height = 170
    # Loop through the data, step size of 8
    for i in range(0, total_rows, 8):
        # Add a new page for every 8 items
        if i > 0:
            c.showPage()  # This creates a new page

        # Call getData for 8 rows or less if there are remaining rows
        for j in range(i, min(i + 8, total_rows)):
            if j - i == 0:
                generateSticker(height, sticker_width, sticker_height, c, j, 20, 10, 30, 48, 205)
            elif j - i == 1:
                generateSticker(height, sticker_width, sticker_height, c, j, 300, 10, 310, 48, 485)
            elif j - i == 2:
                generateSticker(height, sticker_width, sticker_height, c, j, 20, 190, 30, 228, 205)
            elif j - i == 3:
                generateSticker(height, sticker_width, sticker_height, c, j, 300, 190, 310, 228, 485)
            elif j - i == 4:
                generateSticker(height, sticker_width, sticker_height, c, j, 20, 370, 30, 408, 205)
            elif j - i == 5:
                generateSticker(height, sticker_width, sticker_height, c, j, 300, 370, 310, 408, 485)
            elif j - i == 6:
                generateSticker(height, sticker_width, sticker_height, c, j, 20, 550, 30, 588, 205)
            elif j - i == 7:
                generateSticker(height, sticker_width, sticker_height, c, j, 300, 550, 310, 588, 485)

    # Save PDF
    c.save()
# loadData("C:/Users/thear/Desktop/Jupyter Notebooks/Sticker Generator/bilal.csv")
# generate_pdf("C:/Users/thear/Desktop/Stickers.pdf")
# delete_all_files_in_folder("Bars")
# delete_all_files_in_folder("QRs")

# ================================================= GUI ================================================================
def browse_csv():
    filename = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    csv_input.delete(0, tk.END)  # Clear the current input
    csv_input.insert(0, filename)  # Insert the selected file path
def browse_output_folder():
    folder_path = filedialog.askdirectory()  # Let user choose the output folder
    output_folder_input.delete(0, tk.END)  # Clear current input
    output_folder_input.insert(0, folder_path)  # Insert the selected folder path
def generate_stickers():
    # Placeholder for the button functionality
    csv_file = csv_input.get()
    loadData(csv_file)
    output_folder = output_folder_input.get()
    output_file = output_input.get()
    generate_pdf(output_folder + "/" + output_file + ".pdf")
    delete_all_files_in_folder("Bars")
    delete_all_files_in_folder("QRs")
    # You can add your logic for generating stickers here
# Create the main window
root = tk.Tk()
root.title("Sticker Generator")
# Set a default window size (e.g., 400x400)
window_width = 400
window_height = 600

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y position to center the window
position_top = 20
position_right = int(screen_width / 2 - window_width / 2)

# Set the geometry with the calculated position and window size
root.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')
root.config(bg="#2c3e50")  # Background color for the window
# Load and display the logo using Pillow
logo_image = Image.open("logo.png")  # Replace with your logo path
logo_image = logo_image.resize((100, 100))  # Resize logo if needed
logo = ImageTk.PhotoImage(logo_image)  # Convert to a Tkinter-compatible image

logo_label = tk.Label(root, image=logo, bg="#F0F0F0")
logo_label.pack(pady=20)

# Title "Sticker Generator"
title = tk.Label(root, text="Sticker Generator", font=("Helvetica", 16, "bold"), bg="#F0F0F0", fg="#3A3A3A")
title.pack(pady=10)

# CSV input field
csv_label = tk.Label(root, text="Select CSV File:", bg="#F0F0F0", fg="#3A3A3A")
csv_label.pack(pady=5)

csv_input = tk.Entry(root, width=40, bg="#FFFFFF", fg="#3A3A3A", font=("Helvetica", 12))
csv_input.pack(pady=5)

browse_button = tk.Button(root, text="Browse", command=browse_csv, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
browse_button.pack(pady=5)

# Output file name input field
output_label = tk.Label(root, text="Output File Name:", bg="#F0F0F0", fg="#3A3A3A")
output_label.pack(pady=5)

output_input = tk.Entry(root, width=40, bg="#FFFFFF", fg="#3A3A3A", font=("Helvetica", 12))
output_input.pack(pady=5)

# Output folder selection
output_folder_label = tk.Label(root, text="Select Output Folder:", bg="#F0F0F0", fg="#3A3A3A")
output_folder_label.pack(pady=5)

output_folder_input = tk.Entry(root, width=40, bg="#FFFFFF", fg="#3A3A3A", font=("Helvetica", 12))
output_folder_input.pack(pady=5)

folder_button = tk.Button(root, text="Browse", command=browse_output_folder, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
folder_button.pack(pady=5)

# Generate Stickers button
generate_button = tk.Button(root, text="Generate Stickers", command=generate_stickers, bg="#4CAF50", fg="#FFFFFF", font=("Helvetica", 12, "bold"))
generate_button.pack(pady=20)

# Run the main loop
root.mainloop()