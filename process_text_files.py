import re
import os

def read_text_file(file_path):
    """Read text from file"""
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

def extract_sentences(text):
    """Split text into sentences"""
    # Simple sentence splitting on periods, exclamation marks, and question marks
    sentences = re.split(r'[.!?]+', text)
    
    # Clean and filter sentences
    clean_sentences = []
    for sentence in sentences:
        sentence = sentence.strip()
        # Keep sentences that are reasonable length and contain risk-related words
        if 20 <= len(sentence) <= 300 and contains_risk_keywords(sentence):
            clean_sentences.append(sentence)
    
    return clean_sentences

def contains_risk_keywords(sentence):
    """Check if sentence contains any risk-related keywords"""
    risk_words = [
        'risk', 'threat', 'vulnerability', 'exposure', 'disruption', 'crisis',
        'supply', 'financial', 'legal', 'compliance', 'security', 'operational',
        'shortage', 'delay', 'cost', 'revenue', 'debt', 'litigation', 'regulation'
    ]
    
    sentence_lower = sentence.lower()
    return any(word in sentence_lower for word in risk_words)

def classify_risk(sentence):
    """Classify sentence into risk category"""
    sentence_lower = sentence.lower()

    return "Supply Chain"
    
    # legal_words = ['legal', 'litigation', 'compliance', 'regulatory', 'regulation']
    # supply_words = ['supply', 'supplier', 'delivery', 'shortage', 'disruption', 'logistics']
    # financial_words = ['financial', 'revenue', 'cost', 'debt', 'profit', 'margin']
    
    # if any(word in sentence_lower for word in legal_words):
    #     return "Legal"
    # elif any(word in sentence_lower for word in supply_words):
    #     return "Supply Chain"
    # elif any(word in sentence_lower for word in financial_words):
    #     return "Financial"
    # else:
    #     return "Legal"  # Default

def process_files(folder_paths=["sc_output"]):
    """Loop through multiple folders and process all text files"""
    
    # Handle single folder or list of folders
    if isinstance(folder_paths, str):
        folder_paths = [folder_paths]
    
    all_sentences = []
    all_labels = []
    all_numeric_labels = []
    
    for folder_path in folder_paths:
        print(f"Processing folder: {folder_path}")
        
        # Check if folder exists
        if not os.path.exists(folder_path):
            print(f"Folder {folder_path} does not exist, skipping...")
            continue
        
        # Get all text files in folder
        text_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        
        for file_name in text_files:
            file_path = os.path.join(folder_path, file_name)
            print(f"Processing: {folder_path}/{file_name}")
            
            # Read the text file
            text = read_text_file(file_path)
            
            # Extract sentences
            sentences = extract_sentences(text)
            
            # Classify based on folder path
            if folder_path in ("sc_output","scraped_content"):
                labels = ["Supply Chain" for sentence in sentences]
            elif folder_path == "fin_output":
                labels = ["Financial" for sentence in sentences]
            else:
                labels = ["Legal" for sentence in sentences]  # default
            
            # Create numeric labels
            label_map = {"Legal": 0, "Supply Chain": 1, "Financial": 2}
            numeric_labels = [label_map[label] for label in labels]
            
            # Add to combined results
            all_sentences.extend(sentences)
            all_labels.extend(labels)
            all_numeric_labels.extend(numeric_labels)
    
    return all_sentences, all_labels, all_numeric_labels



