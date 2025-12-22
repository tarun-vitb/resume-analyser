import sys
sys.path.append('.')

from backend_final import extract_text_from_pdf, extract_name_from_text, extract_skills_from_text

def test_extract_functions():
    # Test PDF extraction
    try:
        print("Testing PDF extraction...")
        text = extract_text_from_pdf("resume_alice.pdf")
        print(f"Extracted text length: {len(text)}")
        print(f"First 200 chars: {text[:200]}")
        
        print("\nTesting name extraction...")
        name = extract_name_from_text(text)
        print(f"Extracted name: {name}")
        
        print("\nTesting skills extraction...")
        skills = extract_skills_from_text(text)
        print(f"Extracted skills: {skills}")
        
    except Exception as e:
        import traceback
        print(f"Error: {e}")
        print(f"Traceback: {traceback.format_exc()}")

if __name__ == "__main__":
    test_extract_functions()
