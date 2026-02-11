import sys
import os

def extract_with_pdfplumber(pdf_path):
    import pdfplumber
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n\n"
    return text

def extract_with_pypdf(pdf_path):
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text

def extract_with_pypdf2(pdf_path):
    import PyPDF2
    # PyPDF2 3.0+ uses PdfReader, older uses PdfFileReader
    if hasattr(PyPDF2, 'PdfReader'):
        reader = PyPDF2.PdfReader(pdf_path)
    else:
        reader = PyPDF2.PdfFileReader(open(pdf_path, 'rb'))
    
    text = ""
    # Handle numPages vs len(pages) depending on version
    if hasattr(reader, 'pages'):
        for page in reader.pages:
            text += page.extract_text() + "\n\n"
    else:
        for i in range(reader.numPages):
            text += reader.getPage(i).extract_text() + "\n\n"
    return text

def main(pdf_path, output_path):
    content = None
    
    print(f"Attempting to extract from {pdf_path}")
    
    # Try pdfplumber first
    try:
        print("Trying pdfplumber...")
        content = extract_with_pdfplumber(pdf_path)
        print("Success with pdfplumber")
    except ImportError:
        print("pdfplumber not found.")
    except Exception as e:
        print(f"pdfplumber failed: {e}")

    # Try pypdf if content is still None
    if content is None:
        try:
            print("Trying pypdf...")
            content = extract_with_pypdf(pdf_path)
            print("Success with pypdf")
        except ImportError:
            print("pypdf not found.")
        except Exception as e:
            print(f"pypdf failed: {e}")
            
    # Try PyPDF2
    if content is None:
        try:
            print("Trying PyPDF2...")
            content = extract_with_pypdf2(pdf_path)
            print("Success with PyPDF2")
        except ImportError:
            print("PyPDF2 not found.")
        except Exception as e:
            print(f"PyPDF2 failed: {e}")

    if content:
        # cleanup: replace multiple newlines
        lines = content.split('\n')
        cleaned_lines = []
        for line in lines:
            line = line.strip()
            # Simple heuristic to detect headers (not perfect)
            if line and not line.startswith("-") and not line.startswith("·") and len(line) < 30 and not line[-1] in ".,。、":
                cleaned_lines.append(f"## {line}")
            elif line:
                cleaned_lines.append(line)
            else:
                cleaned_lines.append("")
        
        md_content = "\n".join(cleaned_lines)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"Successfully wrote to {output_path}")
    else:
        print("Failed to extract text using available libraries.")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Default for local testing if args not provided correctly
        pdf_path = r"C:\Users\menta\OneDrive\デスクトップ\雀荘Quasar\ルール一覧\６華６北五等サンマフリー.pdf"
        output_path = r"C:\Users\menta\OneDrive\デスクトップ\雀荘Quasar\ルール一覧\６華６北五等サンマフリー.md"
        main(pdf_path, output_path)
    else:
        main(sys.argv[1], sys.argv[2])
