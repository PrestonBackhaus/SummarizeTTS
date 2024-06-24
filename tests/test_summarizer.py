from summarizer import Summarizer

def test_extract_text_from_pdf():
    pdf_path = "tests/SWikipedia.pdf"
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    assert text is not None
    assert len(text) > 0
    print("Extracted Text: ")
    print(text)
    return text

def test_split_text_by_sections():
    pdf_path = "tests/SWikipedia.pdf"
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    sections = summarizer.split_text_by_sections(text, section_delimiter="Section")
    assert len(sections) > 1
    print("Split Sections: ")
    for i, section in enumerate(sections):
        print(f"Section {i+1}:")
        print(section[:500])
        print()

def main():
    pdf_path = "tests/OSWikipedia.pdf"
    summarizer = Summarizer()

    final_summary = summarizer.summarize_document(pdf_path)

    print("Final Summary: ")
    print(final_summary)

if __name__ == "__main__":
    # main()
    extracted_text = test_extract_text_from_pdf()
    test_split_text_by_sections()