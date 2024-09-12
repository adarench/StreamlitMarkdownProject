import streamlit as st
from docuparser import read_and_parse_docx
from generator import generate_markdown_sync
import openai

def chat_with_gpt():
    """
    Handles the chat interface for interacting with GPT-4 about the generated Markdown.
    """
    st.header("Chat with GPT-4 about the output")
    
    # Initialize the session state to store the conversation history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "system", "content": "You are a helpful assistant."}
        ]
    
    # Display the chat messages
    for msg in st.session_state.messages:
        if msg["role"] != "system":
            st.text_area(f"{msg['role'].capitalize()}:", msg["content"], height=100, key=f"{msg['role']}_{len(st.session_state.messages)}")
    
    # User input box
    user_input = st.text_input("Your message:")
    if st.button("Send"):
        # Add user message to the session state
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Generate response from GPT-4
        try:
            response = openai.ChatCompletion.create(
                model="gpt-4-turbo",
                messages=st.session_state.messages
            )
            assistant_message = response.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": assistant_message})
        except Exception as e:
            st.error(f"Error generating response: {e}")
        
        # Display the new messages
        for msg in st.session_state.messages[-2:]:
            st.text_area(f"{msg['role'].capitalize()}:", msg["content"], height=100, key=f"{msg['role']}_{len(st.session_state.messages)}")

def main():
    st.title("Survey Question Markdown Generator")

    # Use Streamlit tabs to separate functionalities
    tab1, tab2 = st.tabs(["Generate Markup", "Chat with GPT-4"])

    with tab1:
        uploaded_file = st.file_uploader("Choose a survey document", type=["docx"])
        
        if uploaded_file is not None:
            with st.spinner("Reading and processing file..."):
                # Parse the DOCX file to extract survey questions
                questions = read_and_parse_docx(uploaded_file)
            
            # Combine all questions into a single string
            combined_questions = "\n\n".join([f"Question {i+1}: {q}" for i, q in enumerate(questions)])

            # Show parsed questions in a single text area for verification
            st.subheader("Parsed Questions")
            st.text_area("Questions", combined_questions, height=300)

            # Button to generate Markdown from parsed questions
            if st.button("Generate Markdown"):
                with st.spinner("Generating Markdown..."):
                    # Generate markup using GPT-4
                    markdown_output = generate_markdown_sync(questions)
                    
                    # Display the generated markdown
                    st.subheader("Generated Markdown")
                    st.text_area("Markdown Output", markdown_output, height=800)
                    
                    # Option to download the markdown
                    st.download_button(
                        label="Download Markdown",
                        data=markdown_output,
                        file_name="generated_markdown.md",
                        mime="text/markdown"
                    )

    with tab2:
        chat_with_gpt()

if __name__ == "__main__":
    main()
