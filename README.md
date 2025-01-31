# Sticker Generator

This project is a Sticker Generator application that allows users to generate custom PDF stickers containing product information, barcodes, and QR codes. The application supports reading data from a CSV file and provides a simple GUI for input selection. Stickers are saved as PDF files, making them ready for printing.

---

## Features

- **Data Loading:** Load product data from a CSV file.
- **Barcode and QR Code Generation:** Automatically generate barcodes and QR codes based on the data.
- **PDF Export:** Generate PDF files containing stickers for multiple products.
- **Dynamic Layout:** Supports up to 8 stickers per page.
- **Graphical User Interface (GUI):** User-friendly interface for file selection and PDF generation.
- **Data Cleanup:** Automatically removes temporary barcode and QR code images after processing.

---

## Technologies Used

- **Programming Language:** Python
- **Libraries:**
  - `pandas`: Data manipulation
  - `reportlab`: PDF generation
  - `qrcode`: QR code generation
  - `python-barcode`: Barcode generation
  - `Pillow`: Image handling
  - `tkinter`: GUI development

---

## Requirements

Ensure you have Python 3 installed.
Install the required dependencies by running:

```bash
pip install pandas reportlab qrcode python-barcode Pillow
```

---

## How to Use

### 1. Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### 2. Run the Application

```bash
python sticker_generator.py
```

### 3. GUI Instructions

- **CSV File:** Click "Browse CSV" and select the CSV file containing the product data.
- **Output Folder:** Click "Browse Output Folder" and select the folder where the generated PDF will be saved.
- **Output File Name:** Enter the desired name for the output PDF file.
- **Generate Stickers:** Click the "Generate Stickers" button to create the PDF file.

### Example CSV Format

| PART NO | OEM  | DESCRIPTION | Qty |
|---------|------|-------------|-----|
| 12345   | ABC  | Widget A    | 100 |
| 67890   | XYZ  | Widget B    | 200 |

---

## Project Structure

```plaintext
Sticker Generator/
├── Bars/         # Temporary folder for barcode images
├── QRs/          # Temporary folder for QR code images
├── sticker_generator.py  # Main application file
└── README.md     # Documentation
```

---

## Key Functions

### `loadData(csv_file)`
Loads data from the specified CSV file.

### `generate_barcode(bar_data, file_path)`
Creates a barcode image for the given data.

### `generate_qrcode(data, file_path)`
Generates a QR code image for the given data.

### `generate_pdf(pdf_filename)`
Generates the final PDF containing all stickers.

### `delete_all_files_in_folder(folder_path)`
Cleans up temporary barcode and QR code images.

### `draw_multiline_paragraph(c, x, y, text, max_width)`
Draws multiline text in the PDF.

---

## Example Output

The generated stickers include:
- **Barcode and QR Code**
- **Product Information:** Part Number, Manufacturer, Description, and Quantity

---

## Improvements
Potential future enhancements:
- Add support for additional barcode types.
- Improve error handling for missing or malformed data.
- Customize sticker layout dynamically.
- Include support for custom fonts and branding.

---

## License
This project is licensed under the [MIT License](LICENSE).

---

## Contributions
Contributions are welcome! Feel free to fork this repository and submit a pull request.

---

## Contact
For questions or suggestions, please contact bqadeer347@gmail.com.

