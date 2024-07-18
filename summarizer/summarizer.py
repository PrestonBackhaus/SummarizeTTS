import os
import openai
from openai import OpenAI
from dotenv import load_dotenv
from pdfminer.high_level import extract_text
from pathlib import Path

# Load environment variable from .env file
load_dotenv()

class Summarizer:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        openai.api_key = self.api_key
        self.client = OpenAI()

    # Summarize text using the GPT-4o model
    def summarize_with_gpt4o(self, text, max_tokens=4000):
        prompt = f"""
        Provide a comprehensive summary of the following text. This summary will be converted to speech, so follow these guidelines:

        1. Capture all main ideas, key concepts, and important details.
        2. Include supplementary details that provide context or deeper understanding.
        3. The summary should be thorough but not exceed 25% of the input text's length.
        4. Ensure the summary is coherent, well-structured, and flows logically.
        5. Structure the summary with clear sections, using full sentences to introduce new topics. Avoid using symbols or numbers that might be read aloud awkwardly.
        6. Use transition phrases between sections to improve flow in spoken form (e.g., "Moving on to", "Next, we'll discuss", "Another important aspect is").
        7. Spell out abbreviations and acronyms at least once, as they may be unclear when spoken.
        8. If mentioning specific years or numbers, write them in a way that's clear when spoken (e.g., "the year two thousand and twenty-four" instead of "2024").
        9. If the input text starts or ends abruptly due to chunking:
        - For abrupt starts: Begin the summary naturally, inferring context if necessary.
        - For abrupt ends: Conclude the summary at the last complete thought or section.
        10. Do not disregard any potentially useful information.
        11. Do not include any concluding statements about the summary itself.

        Remember, this summary will be read aloud, so focus on clarity and natural speech patterns.

        Text to summarize:
        {text}
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a highly capable assistant skilled in summarizing complex information comprehensively and accurately."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-4o",
            max_tokens=max_tokens
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
    def summarize_document(self, pdf_path, summary_file="final_summary.txt"):
        full_text = self.extract_text_from_pdf(pdf_path)
        chunks = self.split_text_into_chunks(full_text)
        refined_chunks = [self.clean_and_refine_text(chunk) for chunk in chunks]
        refined_text = ' '.join(refined_chunks)
        
        chunks = self.split_text_into_chunks(refined_text, chunk_size=30000)
        
        summaries = [self.summarize_with_gpt4o(chunk) for chunk in chunks]
        combined_summary = ' '.join(summaries)
        
        final_summary = self.summarize_with_gpt4o(combined_summary, max_tokens=4000)
        
        # Save summary to file
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(final_summary)
        
        return final_summary
    
    # Split text into manageable chunks
    def split_text_into_chunks(self, text, chunk_size=30000):
        return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
        
    # Clean and refine text using GPT-3.5 turbo
    def clean_and_refine_text(self, text, max_tokens=3950):
        prompt = f"""
        Clean and refine the following text:
        1. Remove all unnecessary content (navigation bars, footers, references, etc.)
        2. Remove any remaining redundant information
        3. Standardize formatting and fix any potential errors
        4. Identify distinct sections and add appropriate headings
        5. Do not summarize or omit any meaningful content
        6. Ensure the text flows logically from one topic to the next

        Return the full refined text, maintaining all relevant content and meaning.

        Text to clean and refine:
        {text}
        """
        
        response = self.client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant skilled in cleaning and structuring text."},
                {"role": "user", "content": prompt}
            ],
            model="gpt-3.5-turbo",
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    
    def text_to_speech(self, input_file, output_file="output.mp3", voice="onyx"):
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        response = self.client.audio.speech.create(
            model="tts-1",
            voice=voice,
            input=text
        )
        
        speech_file_path = Path(output_file)
        
        with speech_file_path.open("wb") as file:
            for chunk in response.iter_bytes():
                file.write(chunk)
    
        print(f"Audio saved to {output_file}")

    def summarize_and_vocalize(self, pdf_path, summary_file="final_summary.txt", output_file="summary_audio.mp3"):
        # Extract and summarize text, saving to file
        summary = self.summarize_document(pdf_path, summary_file)
        
        # Convert summary file to speech
        self.text_to_speech(summary_file, output_file)
        
        return summary



    def main():
            summarizer = Summarizer()
            
            # Specify the path to your PDF file
            pdf_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "examples", "OSWikipedia.pdf")
            
            # Specify the output files
            summary_file = os.path.join(os.path.dirname(__file__), "main_final_summary.txt")
            audio_file = os.path.join(os.path.dirname(__file__), "summary_audio.mp3")
            
            # Summarize and vocalize
            final_summary = summarizer.summarize_and_vocalize(pdf_path, summary_file, audio_file)
            
            print("Final Summary: ")
            print(final_summary)
            print(f"Summary saved to '{summary_file}'")
            print(f"Audio summary saved to '{audio_file}'")

if __name__ == "__main__":
    Summarizer.main()