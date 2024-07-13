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
    def summarize_with_gpt4o(self, text, max_tokens=7500, temperature=0.7):
        prompt = f"""
        Provide a comprehensive summary of the following text. Follow these guidelines:
        1. Capture all main ideas, key concepts, and important details.
        2. Include supplementary details that provide context or deeper understanding.
        3. The summary should be thorough but not exceed 25% of the input text's length.
        4. Ensure the summary is coherent, well-structured, and flows logically.
        5. If the input text starts or ends abruptly due to chunking:
        - For abrupt starts: Begin the summary naturally, inferring context if necessary.
        - For abrupt ends: Conclude the summary at the last complete thought or section.
        6. Do not disregard any potentially useful information.
        7. If the text contains distinct sections, maintain this structure in the summary.

        Text to summarize:
        {text}
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a highly capable assistant skilled in summarizing complex information comprehensively and accurately."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",
            max_tokens=max_tokens,
            temperature=temperature
        )
        summary = response.choices[0].message.content.strip()
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
    
    # Summarize text from a PDF file
    def summarize_document(self, pdf_path):
        full_text = self.extract_text_from_pdf(pdf_path)
        cleaned_text = self.clean_large_text(full_text)
        refined_text = self.refine_text_with_gpt(cleaned_text)
        
        # Split refined text into 30,000 token chunks
        chunks = self.split_text_into_chunks(refined_text, chunk_size=30000)
        
        summaries = [self.summarize_with_gpt4o(chunk) for chunk in chunks]
        combined_summary = ' '.join(summaries)
        
        final_summary = self.summarize_with_gpt4o(combined_summary, max_tokens=15000)
        return final_summary
    
    # Split text into manageable chunks
    def split_text_into_chunks(self, text, chunk_size=30000):
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
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
