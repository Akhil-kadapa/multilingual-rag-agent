import os
import PyPDF2
import chardet

def load_documents(folder_path):
    """
    Loads documents from folder — supports PDF and TXT files
    """
    documents = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        if filename.endswith(".pdf"):
            try:
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    text = ""
                    for page in reader.pages:
                        extracted = page.extract_text()
                        if extracted:
                            text += extracted

                if text.strip():
                    documents.append({
                        "filename": filename,
                        "text": text
                    })
                else:
                    documents.append({
                        "filename": filename,
                        "text": f"Could not extract text from {filename}. Please convert to TXT format."
                    })
            except Exception as e:
                documents.append({
                    "filename": filename,
                    "text": f"Error reading {filename}. Please convert to TXT format."
                })

        elif filename.endswith(".txt"):
            try:
                with open(file_path, "rb") as f:
                    encoding = chardet.detect(f.read())['encoding']
                with open(file_path, "r", encoding=encoding, errors="ignore") as file:
                    text = file.read()
                documents.append({
                    "filename": filename,
                    "text": text
                })
            except Exception as e:
                documents.append({
                    "filename": filename,
                    "text": f"Error reading {filename}."
                })

    return documents


def chunk_text(text, filename, chunk_size=500, overlap=50):
    """
    Splits text into overlapping chunks
    """
    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append({
            "text": chunk,
            "filename": filename,
            "chunk_id": len(chunks)
        })
        start = end - overlap

    return chunks