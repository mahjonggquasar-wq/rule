import sys
import re

def clean_text(text):
    # Remove spaces between CJK characters
    # This regex matches a CJK character, followed by whitespace, followed by a CJK character
    # and replaces it with just the two characters.
    # CJK ranges: \u4e00-\u9fff (Common), \u3040-\u309f (Hiragana), \u30a0-\u30ff (Katakana)
    # \u3000-\u303f (CJK punctuation) - we might want to keep spaces around punctuation though?
    # Let's just target CJK chars and Kana.
    pattern = r'(?<=[\u4e00-\u9fff\u3040-\u30ff])\s+(?=[\u4e00-\u9fff\u3040-\u30ff])'
    text = re.sub(pattern, '', text)
    
    # Also join lines that are likely broken (single characters)
    # If we have a sequence of lines that are 1-2 chars long, likely vertical text
    lines = text.split('\n')
    new_lines = []
    buffer = ""
    
    for line in lines:
        stripped = line.strip()
        if not stripped:
            if buffer:
                new_lines.append(buffer)
                buffer = ""
            new_lines.append("")
            continue
            
        if len(stripped) <= 2 and not stripped.startswith("・"):
            buffer += stripped
        else:
            if buffer:
                new_lines.append(buffer)
                buffer = ""
            new_lines.append(stripped)
            
    if buffer:
        new_lines.append(buffer)
        
    return "\n".join(new_lines)

def extract_with_pypdf(pdf_path):
    from pypdf import PdfReader
    reader = PdfReader(pdf_path)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n\n"
    return text

def main(pdf_path, output_path):
    try:
        print("Extracting with pypdf...")
        raw_text = extract_with_pypdf(pdf_path)
        print("Cleaning text...")
        cleaned_text = clean_text(raw_text)
        
        # Additional formatting for markdown
        md_lines = []
        for line in cleaned_text.split('\n'):
            line = line.strip()
            if not line:
                md_lines.append("")
                continue
            
            # Heuristics for headers
            if line.startswith("【") and line.endswith("】"):
                md_lines.append(f"### {line}")
            elif line.startswith("■") or line.startswith("●"):
                 md_lines.append(f"### {line}")
            elif "サンマフリー" in line or "ルール" in line: # Title-ish
                 md_lines.append(f"# {line}")
            else:
                md_lines.append(line)

        final_content = "\n".join(md_lines)
        
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(final_content)
        print(f"Done. Saved to {output_path}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        # Default for local testing
        pdf_path = r"C:\Users\menta\OneDrive\デスクトップ\雀荘Quasar\ルール一覧\６華６北五等サンマフリー.pdf"
        output_path = r"C:\Users\menta\OneDrive\デスクトップ\雀荘Quasar\ルール一覧\６華６北五等サンマフリー_cleaned.md"
        main(pdf_path, output_path)
    else:
        main(sys.argv[1], sys.argv[2])
