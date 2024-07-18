# SummarizeTTS

SummarizeTTS is a Python-based tool that summarizes PDF documents and converts the summaries to speech using OpenAI's API.

## Features

- Extract text from PDF documents
- Clean and preprocess extracted text
- Summarize text using OpenAI's GPT-3.5 and GPT-4o models
- Convert summaries to speech (text-to-speech)
- Handle large documents by splitting them into manageable chunks

## Requirements

- Python 3.7+
- OpenAI API key
- Required Python libraries: openai, pdfminer, spacy, dotenv

## Setup

1. Clone the repository
2. Install required libraries
3. Set up your OpenAI API key in a `.env` file
4. Download the SpaCy English model: `python -m spacy download en_core_web_sm`
