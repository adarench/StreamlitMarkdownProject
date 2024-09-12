import os
import openai
from dotenv import load_dotenv
import aiohttp
import asyncio
import backoff

# Load environment variables from .env file
load_dotenv()

# Initialize the OpenAI client with the API key
openai.api_key = os.getenv("OPENAI_API_KEY")

def chunk_questions(questions, chunk_size=5):
    """Splits the list of questions into smaller chunks."""
    for i in range(0, len(questions), chunk_size):
        yield questions[i:i + chunk_size]

async def generate_markdown_async(session, question, question_label):
    """
    Generates Markup for a survey question using GPT-4 asynchronously with retry logic.
    Parameters:
    session (ClientSession): The aiohttp session for making API requests.
    question (str): The survey question.
    question_label (str): The label for the question.
    Returns:
    str: Generated Markup content or an error message.
    """
    instructions = """
    Convert each of the following survey questions into the specified markup format.
    Every question must be processed individually, regardless of similarity to other questions.
    Do not assume or skip any question, and make sure every question is output in its complete markup form.

    Each question should follow this structure:
    - Start with a left curly bracket '{'
    - Followed by the Question Label, which starts with an uppercase 'Q'
    - The Question Label is immediately followed by a colon ':'
    - The following lines contain the question text
    - The 'Question Type' line terminates the question text lines. It starts with an exclamation point '!' followed by the question type.
    - For single choice questions, use '!FIELD' followed by the answer choices/categories. Each line starts with the answer code and is followed by the answer text. Answer codes must be numeric and zero-padded.
    - For numeric questions, use '!NUMERIC,,,min,max,refused_code'
    - For open-ended questions, use '!VERBATIM'
    - For dropdown questions, use '!DROPDOWN' followed by the options
    - The question definition is terminated with a right curly bracket '}'

    Important Nuances:
    - Some questions have a list of options to rate, these should each be treated as individual numeric questions.
    - Always generate Markup for every question from Q1 to the end of the document.
    - If a question has a paragraph of text followed by multiple items to rate on a scale (e.g., 1-10), treat each item as a separate numeric question with the same rating scale.
    - Do not skip or ignore any question. If uncertain, generate a reasonable Markdown format based on the instructions.
    """

    messages = [
        {"role": "system", "content": "You are a survey markup expert. You will iterate through every paragraph of a file to generate survey markup in the specified format. Errors are not acceptable. Generate markup for every question on each page of the document, no matter how complicated. Do not produce errors. You will only generate markup. do not explain your reasoning for any of it. markup only. "},
        {"role": "user", "content": f"{instructions}\n\n{question}"}
    ]

    # Define the backoff strategy for retrying the API request
    @backoff.on_exception(backoff.expo, (aiohttp.ClientError, asyncio.TimeoutError), max_tries=5)
    async def request_openai_api():
        try:
            async with session.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}"},
                json={"model": "gpt-4", "messages": messages}
            ) as response:
                data = await response.json()
                if response.status != 200:
                    return f"Error generating Markup for {question_label}: HTTP {response.status} - {data.get('error', {}).get('message', 'Unknown error')}"
                if 'choices' in data and data['choices']:
                    markdown = data['choices'][0]['message']['content'].strip()
                    return markdown
                else:
                    return f"Error generating Markup for {question_label}: 'choices' not in response"
        except Exception as e:
            return f"Error generating Markup for {question_label}: {e}"

    # Call the request function with retry logic
    return await request_openai_api()

async def generate_markdown(questions):
    """
    Generates Markdown for a list of survey questions using GPT-4 asynchronously.
    Parameters:
    questions (list): List of survey questions.
    Returns:
    str: Generated Markdown content.
    """
    markdown_output = []
    async with aiohttp.ClientSession() as session:
        for question_chunk in chunk_questions(questions):
            tasks = [generate_markdown_async(session, question, f"Q{i+1}") for i, question in enumerate(question_chunk)]
            results = await asyncio.gather(*tasks)
            markdown_output.extend(results)
    return "\n\n".join(markdown_output)

def generate_and_verify_markdown(questions):
    """
    Generate markdown and ensure every question is processed.
    """
    markup_output = generate_markdown_sync(questions)
    missing_questions = [q for q in questions if q not in markup_output]
    if missing_questions:
        print("Retrying missing questions...")
        additional_output = generate_markdown_sync(missing_questions)
        markup_output += "\n\n" + additional_output
    return markup_output

def generate_markdown_sync(questions):
    """
    Synchronous wrapper for generate_markdown to be used in Streamlit.
    """
    return asyncio.run(generate_markdown(questions))

def split_questions(content):
    """
    Splits content into individual questions based on custom logic.
    """
    return content.split("\n\n")

def merge_related_content(questions):
    """
    Merges related content to form complete questions, handling multi-paragraph questions.
    """
    # You can enhance this function with specific logic to merge content based on patterns or keywords.
    merged_questions = []
    for question in questions:
        if question:
            merged_questions.append(question.strip())
    return merged_questions


