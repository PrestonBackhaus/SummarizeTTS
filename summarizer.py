import os
import openai
from dotenv import load_dotenv
import fitz

# Load environment variable from .env file
load_dotenv()

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key

    # Summarize text using the GPT-4o model
    def summarize_text(self, text, max_tokens=1024, temperature=0.7):
        prompt = f"""
        Summarize the following text in a flowing, narrative style, formatted in paragraphs. Ensure that the summary covers the main ideas, explains key terms, and includes important details. Do not include any introductory phrases or concluding statements; provide only the summary text.

        Text to summarize: 
        {text}
        """

        response = openai.Completion.create(
            engine="gpt-4o",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        summary = response.choices[0].text.strip()
        return summary
    
    # Write the summary to a text file
    def to_file(self, text, filename):
        with open(filename + ".txt", "w") as file:
            file.write(text)

    # Extract text for a plain text file
    def from_file(self, filename):
        with open(filename + ".txt", "r") as file:
            text = file.read()
        return text
    
    # Extract text from a PDF file
    def extract_text_from_pdf(self, pdf_path):
        doc = fitz.open(pdf_path)
        full_text = ""
        for page in doc:
            full_text += page.get_text()
        return full_text
    
    # Split text into chunks of a specified size
    def split_text(self, text, chunk_size=3000):
        return [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    
    # Split text by sections
    def split_text_by_sections(self, text, section_delimiter="Section"):
        sections = text.split(section_delimiter)
        sections = [section_delimiter + section for section in sections if section.strip()]
        return sections
    
    # Summarize text from a PDF file
    def summarize_document(self, pdf_path):
        full_text = self.extract_text_from_pdf(pdf_path)
        sections = self.split_text_by_sections(full_text)

        summaries = []
        for section in sections:
            summary = self.summarize_text(section)
            summaries.append(summary)

        combined_summary = ' '.join(summaries)

        return combined_summary

    # Check the summary and revise
    def check_summary(self, text, max_tokens=1024, temperature=0.7):
        prompt = f"""
        Check the following summary for accuracy, clarity, and coherence. Revise the summary as needed to ensure that it is well-written and effectively communicates the main ideas of the text. Keep the content the same, but check the flow and narrative to ensure it is able to be properly converted to speech. Do not include any introductory phrases or concluding statements; provide only the summary text.

        Summary to check: 
        {text}
        """

        response = openai.Completion.create(
            engine="gpt-4o",
            prompt=prompt,
            max_tokens=max_tokens,
            temperature=temperature
        )
        revised_summary = response.choices[0].text.strip()
        return revised_summary

