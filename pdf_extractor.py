# pdf_extractor.py
"""
Simple PDF Text Extractor Utility

Extract text from PDF files and save to text files.

Usage:
    from utils.pdf_extractor import extract_pdf_text
    
    text = extract_pdf_text("document.pdf")
"""

import PyPDF2
import os
import re

def extract_pdf_text(pdf_path):
    """
    Extract text from PDF file
    
    Args:
        pdf_path: Path to PDF file
        
    Returns:
        Extracted text as string
    """
    try:
        text = ""
        
        with open(pdf_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            
            # Extract text from all pages
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
        
        # Clean the text
        text = clean_text(text)
        return text
        
    except Exception as e:
        print(f"Error extracting PDF {pdf_path}: {e}")
        return ""

def clean_text(text):
    """Clean extracted text"""
    # Remove extra whitespace and newlines
    text = re.sub(r'\s+', ' ', text)
    text = text.strip()
    return text

def save_pdf_as_text(pdf_path, output_dir="extracted_pdfs"):
    """
    Extract PDF and save as text file with PDF name as filename
    
    Args:
        pdf_path: Path to PDF file
        output_dir: Output directory
        
    Returns:
        Path to saved text file
    """
    # Extract text
    text = extract_pdf_text(pdf_path)
    
    if text:
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate filename from PDF path
        pdf_name = os.path.basename(pdf_path)
        txt_filename = pdf_name.replace('.pdf', '.txt')
        
        # Save text file
        output_path = os.path.join(output_dir, txt_filename)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(f"Source PDF: {pdf_path}\n")
            f.write("=" * 80 + "\n\n")
            f.write(text)
        
        print(f"Saved: {output_path}")
        return output_path
    
    return None

def extract_multiple_pdfs(pdf_paths, output_dir="extracted_pdfs"):
    """
    Extract text from multiple PDF files
    
    Args:
        pdf_paths: List of PDF file paths
        output_dir: Output directory
        
    Returns:
        List of saved text file paths
    """
    saved_files = []
    
    for pdf_path in pdf_paths:
        print(f"Processing: {pdf_path}")
        file_path = save_pdf_as_text(pdf_path, output_dir)
        if file_path:
            saved_files.append(file_path)
    
    return saved_files

def process_pdf_folder(input_folder="input", output_folder="output", processed_folder="processed"):
    """
    Process all PDFs from input folder, extract text, and move to processed folder
    
    Args:
        input_folder: Folder containing PDF files to process
        output_folder: Folder to save extracted text files
        processed_folder: Folder to move processed PDF files
        
    Returns:
        Number of PDFs processed
    """
    import shutil
    
    # Create directories if they don't exist
    os.makedirs(input_folder, exist_ok=True)
    os.makedirs(output_folder, exist_ok=True)
    os.makedirs(processed_folder, exist_ok=True)
    
    # Find all PDF files in input folder
    pdf_files = []
    for file in os.listdir(input_folder):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(input_folder, file))
    
    if not pdf_files:
        print(f"No PDF files found in {input_folder}")
        return 0
    
    print(f"Found {len(pdf_files)} PDF files to process")
    
    processed_count = 0
    
    for pdf_path in pdf_files:
        print(f"Processing: {os.path.basename(pdf_path)}")
        
        # Extract text and save
        text_file = save_pdf_as_text(pdf_path, output_folder)
        
        if text_file:
            # Move PDF to processed folder
            pdf_filename = os.path.basename(pdf_path)
            processed_path = os.path.join(processed_folder, pdf_filename)
            
            try:
                shutil.move(pdf_path, processed_path)
                print(f"Moved to processed: {pdf_filename}")
                processed_count += 1
            except Exception as e:
                print(f"Error moving {pdf_filename}: {e}")
        else:
            print(f"Failed to extract text from {os.path.basename(pdf_path)}")
    
    print(f"\nProcessing complete! {processed_count} PDFs processed successfully")
    return processed_count

# Example usage
if __name__ == "__main__":
    # Process all PDFs from input folder
    processed_count = process_pdf_folder()
    
    # Or with custom folders
    # processed_count = process_pdf_folder(
    #     input_folder="my_pdfs",
    #     output_folder="text_files", 
    #     processed_folder="done_pdfs"
    # )