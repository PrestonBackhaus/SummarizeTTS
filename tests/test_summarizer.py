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

def test_clean_and_refine_text():
    summarizer = Summarizer()
    text = summarizer.extract_text_from_pdf(pdf_path)
    cleaned_and_refined_text = summarizer.clean_and_refine_text(text[:15000])
    assert cleaned_and_refined_text is not None
    assert len(cleaned_and_refined_text) > 0
    print("Cleaned and Refined Text: ")
    print(cleaned_and_refined_text[:1000])
    summarizer.to_file(cleaned_and_refined_text, "cleaned_and_refined_text")

def test_summarize_document():
    summarizer = Summarizer()
    final_summary = summarizer.summarize_document(pdf_path)
    assert final_summary is not None
    assert len(final_summary) > 0
    print("Final Summary: ")
    print(final_summary)
    summarizer.to_file(final_summary, "final_summary15000chars")

def test_summarize_and_vocalize():
    summarizer = Summarizer()
    summary = summarizer.summarize_and_vocalize(pdf_path, "final_summary.txt", "os_summary_audio.mp3")
    assert summary is not None
    assert len(summary) > 0
    print("Summary:")
    with open("final_summary.txt", 'r', encoding='utf-8') as f:
        print(f.read())
    print("Audio version of the summary has been saved to 'os_summary_audio.mp3'")

def main():
    summarizer = Summarizer()
    final_summary = summarizer.summarize_document(pdf_path)
    print("Final Summary: ")
    print(final_summary)

if __name__ == "__main__":
    # Uncomment the test you want to run
    # test_extract_text_from_pdf()
    # test_clean_and_refine_text()
    # test_summarize_document()
    test_summarize_and_vocalize()
    # main()