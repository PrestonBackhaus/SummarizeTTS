import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
import re
import spacy

# Load environment variable from .env file
load_dotenv()

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.client = OpenAI()
        self.nlp = spacy.load("en_core_web_sm")

    # Summarize text using the GPT-4o model
    def summarize_text(self, text, max_tokens=1024, temperature=0.7):
        prompt = f"""
        Summarize the following text in a flowing, narrative style, formatted in paragraphs. Ensure that the summary covers the main ideas, explains key terms, and includes important details. Do not include any introductory phrases or concluding statements; provide only the summary text.

        Text to summarize: 
        {text}
        """

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=max_tokens,
            temperature=temperature
        )
        summary = response.choices[0].message.content.text.strip()
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
        text = extract_text(pdf_path)
        text = text.lower()
        return text
    
    # Split text into paragraphs
    def split_text_by_paragraphs(self, text):
        paragraphs = re.split(r'\n\s*\n', text)
        return [para.strip() for para in paragraphs if para.strip()]

    # Group alike paragraphs
    def group_paragraphs_by_similarity(self, paragraphs, threshold=0.5):
        doc_paragraphs = [self.nlp(para) for para in paragraphs]
        groups = []
        current_group = []

        for i, para in enumerate(doc_paragraphs):
            if not current_group:
                current_group.append(paragraphs[i])
                continue
            
            similarity = para.similarity(self.nlp(current_group[-1]))
            if similarity > threshold:
                current_group.append(paragraphs[i])
            else:
                groups.append("\n\n".join(current_group))
                current_group = [paragraphs[i]]
        
        if current_group:
            groups.append("\n\n".join(current_group))
        
        return groups
    
    # Summarize text from a PDF file
    def summarize_document(self, pdf_path):
        full_text = self.extract_text_from_pdf(pdf_path)
        cleaned_text = self.clean_large_text(full_text)
        refined_text = self.refine_text_with_gpt(cleaned_text)
        paragraphs = self.split_text_by_paragraphs(refined_text)
        sections = self.group_paragraphs_by_similarity(paragraphs)

        summaries = []
        for section in sections:
            summary = self.summarize_text(section)
            summaries.append(summary)

        combined_summary = ' '.join(summaries)
        final_summary = self.summarize_text(combined_summary)

        return final_summary

    # Check the summary and revise
    def check_summary(self, text, max_tokens=1024, temperature=0.7):
        prompt = f"""
        Check the following summary for accuracy, clarity, and coherence. Revise the summary as needed to ensure that it is well-written and effectively communicates the main ideas of the text. Keep the content the same, but check the flow and narrative to ensure it is able to be properly converted to speech. Do not include any introductory phrases or concluding statements; provide only the summary text.

        Summary to check: 
        {text}
        """

        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=max_tokens,
            temperature=temperature
        )
        revised_summary = response.choices[0].message.content.text.strip()
        return revised_summary
    
    # Split text into manageable chunks
    def split_text_into_chunks(self, text, chunk_size=2048):
        chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        return chunks
    
    # Clean large text
    def clean_large_text(self, text):
        chunks = self.split_text_into_chunks(text)
        cleaned_chunks = [self.clean_text_with_gpt(chunk) for chunk in chunks]
        cleaned_text = ' '.join(cleaned_chunks)
        return cleaned_text
    
    # Clean using gpt-3.5 turbo, this might start to get costly
    def clean_text_with_gpt(self, text, max_tokens=2048, temperature=0.7):
        prompt = f"""
        Clean the following text by removing all unnecessary content, such as navigation bars, footers, references, and other non-essential information. Ensure that only the main content remains. Do not include any introductory phrases or concluding statements; provide only the cleaned text.
        
        Text to clean:
        {text}
        """
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in cleaning text."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=max_tokens,
            temperature=temperature
        )
        cleaned_text = response.choices[0].message.content.strip()
        return cleaned_text
    
    # Structure cleaned text, reduce redundancy
    def refine_text_with_gpt(self, text, max_tokens=3950, temperature=0.7):
        prompt = f"""
        Further clean and structure the following text. 
        1. Remove any remaining redundant information
        2. Standardize formatting and fix any potential errors
        3. Identify distinct sections and add appropriate headings
        4. Do not summarize or omit any meaningful content
        5. Ensure the text flows logically from one topic to the next

        Return the full refined text, maintaining all relevant content and meaning.

        Text to refine:
        {text}
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in cleaning and structuring text."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=max_tokens,
            temperature=temperature
        )
        refined_text = response.choices[0].message.content.strip()
        return refined_text

    # Clean the text by removing unwanted text
    def clean_text(self, text):
        # Define patterns to remove unwanted text
        patterns = [
            r'Privacy policy.*Terms of Use and Privacy Policy.',  # Remove footer
            r'Text is available under the Creative Commons Attribution-ShareAlike License.*',  # Remove license info
            r'Contents.*hide',  # Remove contents table
            r'\[\d+\]',  # Remove references like [48]
            r'\[.*?\]',  # Remove any text in brackets
            r'\n+',  # Replace multiple newlines with a single newline
            r'Edit\n',  # Remove 'Edit' links
            r'Jump to navigation\nJump to search\n',  # Remove navigation text
            r'Categories:.*?\n',  # Remove category listings
            r'Hidden categories:.*?\n',  # Remove hidden category listings
            r'Help\n',  # Remove help links
            r'From Wikipedia, the free encyclopedia',  # Remove Wikipedia intro
            r'[\r\n]+',  # Replace multiple newlines with a single newline
            r'^\s*$',  # Remove empty lines
            r'^[ \t]+|[ \t]+$',  # Trim leading/trailing spaces
        ]
        
        for pattern in patterns:
            text = re.sub(pattern, '', text, flags=re.DOTALL | re.MULTILINE)
            
        # Further cleaning using spaCy
        doc = self.nlp(text)
        cleaned_sentences = []
        for sent in doc.sents:
            if len(sent.text.strip()) > 10:
                cleaned_sentences.append(sent.text.strip())
        
        cleaned_text = ' '.join(cleaned_sentences)
        return cleaned_text.strip()

