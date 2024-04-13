**Paragraph Extraction from Scanned Documents**

This Python script is designed to extract paragraphs from scanned documents or images, particularly aimed at separating textual content from images or tables. It utilizes the OpenCV library for image processing tasks and NumPy for array manipulation.

**Key Features:**
1. **Table Removal**: The script includes a function to identify and remove tables spanning all columns in the document, enhancing the accuracy of paragraph extraction.
2. **Vertical and Horizontal Extraction**: Using vertical and horizontal projections, the script identifies paragraph boundaries both vertically and horizontally within each column.
3. **Image Detection**: The script includes a mechanism to detect images within paragraphs, ensuring that only textual content is extracted.
4. **Output Generation**: Extracted paragraphs are saved as separate image files, enabling further processing or analysis.

**Usage:**
1. Simply provide the path to the input image file, and the script will process it to extract paragraphs.
2. The extracted paragraphs are saved as individual image files for easy access and further processing.

**Applications:**
1. **Document Processing**: Useful for tasks such as Optical Character Recognition (OCR) or text extraction from scanned documents.
2. **Data Analysis**: Enables the extraction of textual data from scanned documents for analysis or integration into other systems.

Contributions are welcome! Feel free to submit bug reports, feature requests, or pull requests to improve the functionality and usability of the script.
