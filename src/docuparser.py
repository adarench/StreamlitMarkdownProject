import docx

def read_and_parse_docx(file):
    """
    Reads and parses a DOCX file to extract survey questions.
    Parameters:
        file (UploadedFile): The uploaded DOCX file.
    Returns:
        list: A list of parsed survey questions.
    """
    try:
        doc = docx.Document(file)
    except Exception as e:
        print(f"Error reading DOCX file: {e}")
        return []

    questions = []
    current_question = []
    question_indicators = [
        "?", "Select", "Choose", "Rate", "Describe", "How many", "Please record", 
        "Would you say", "Do you", "Please indicate", "From the following list", 
        "In politics today", "Generally speaking", "For each one", "And do you",
        "Do you consider", "Thinking some more", "These agreements", "In your state",
        "Some elected officials", "The following are some statements", "Having read some more",
        "In what year", "Please select", "How would you"
    ]

    for para in doc.paragraphs:
        text = para.text.strip()
        if not text:
            continue

        # Identify new questions using indicators
        if any(text.startswith(indicator) for indicator in question_indicators):
            if current_question:
                questions.append(' '.join(current_question))
                current_question = []

        current_question.append(text)

    if current_question:
        questions.append(' '.join(current_question))

    return questions
