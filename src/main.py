import streamlit as st
from docuparser import read_and_parse_docx
from generator import generate_markdown_sync
import io
from ui import chat_with_gpt
def main():
    st.title("Survey Question Markup Generator")

    # Use Streamlit tabs to separate functionalities
    tab1, tab2 = st.tabs(["Generate Markup", "Chat with GPT-4"])

    with tab1:
        uploaded_file = st.file_uploader("Choose a survey document", type=["docx"])
        
        if uploaded_file is not None:
            with st.spinner("Reading and processing file..."):
                # Parse the DOCX file to extract survey questions
                questions = read_and_parse_docx(uploaded_file)
            
            # Button to generate and download Markup from parsed questions
            if st.button("Generate and Download Markup"):
                with st.spinner("Generating Markup..."):
                    # Generate markup using GPT-4
                    markup_output = generate_markdown_sync(questions)
                    
                    # Encode the markup output to bytes for download
                    markup_bytes = markup_output.encode('utf-8')
                    
                    # Provide a downloadable text file
                    st.download_button(
                        label="Download Markup",
                        data=io.BytesIO(markup_bytes),
                        file_name="generated_markup.txt",  # Change file extension to .txt
                        mime="text/plain"  # Change MIME type to text/plain
                    )

    with tab2:
        chat_with_gpt()

if __name__ == "__main__":
    main()
