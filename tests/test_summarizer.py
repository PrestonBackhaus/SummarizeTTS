import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from summarizer import Summarizer

pdf_path = os.path.join(os.path.dirname(__file__), "OSWikipedia.pdf")

def test_extract_text_from_pdf():
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    assert text is not None
    assert len(text) > 0
    print("Extracted Text: ")
    print(text[:1000])

def test_split_text_by_paragraphs():
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    cleaned_text = summarizer.clean_large_text(text)
    paragraphs = summarizer.split_text_by_paragraphs(cleaned_text)
    assert len(paragraphs) > 1
    print("Paragraphs: ")
    for i, para in enumerate(paragraphs):
        print(f"Paragraph {i+1}:")
        print(para[:1000])
        print()

def test_group_paragraphs_by_similarity():
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    cleaned_text = summarizer.clean_large_text(text)
    paragraphs = summarizer.split_text_by_paragraphs(cleaned_text)
    sections = summarizer. group_paragraphs_by_similarity(paragraphs)
    assert len(sections) > 1
    print("Sections: ")
    for i, section in enumerate(sections):
        print(f"Section {i+1}:")
        print(section[:1000])
        print()

def test_clean_text():
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    cleaned_text = summarizer.clean_large_text(text)
    assert cleaned_text is not None
    assert len(cleaned_text) > 0
    print("Cleaned Text: ")
    print(cleaned_text[:1000])
    summarizer.to_file(cleaned_text, "cleaned_text")


def main():
    summarizer = Summarizer()

    final_summary = summarizer.summarize_document(pdf_path)

    print("Final Summary: ")
    print(final_summary)

if __name__ == "__main__":
    # main()
    # test_extract_text_from_pdf()
    test_clean_text()
    # test_split_text_by_paragraphs()
    # test_group_paragraphs_by_similarity()