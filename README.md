<<<<<<< HEAD
# Survey Question to Markdown Generator

## Project Specifications

### Objective
The goal of this project is to create a chat interface application that converts survey questions into a proprietary Markdown format using GPT-4o mini. Users will upload survey documents, and the system will parse the questions and generate the appropriate Markdown for each question.

### Question Types and Markdown Formats
Based on the provided documents, the following question types and Markdown formats are defined:

#### 1. Simple Choice Question
```markdown
{Q<number>:

<Question text>

!FIELD
<Code> <Answer choice>
<Code> <Answer choice>
...
}
Example:

markdown
Copy code
{Q4:

Is the country going in the right direction or is it on the wrong track?

!FIELD
01 RIGHT DIRECTION
02 WRONG TRACK
08 DON’T KNOW
09 REFUSED
}
2. Numeric Input Question

markdown
Copy code
{<Label>:

<Question text> (USE <special code> if refused)

!NUMERIC,<subtype>,<decimals>,<range>,<special code>
}
Example:

markdown
Copy code
{YEAR_OF_BIRTH:

In what year were you born? (USE 9999 if refused)

!NUMERIC,,,1900-2024,9999
}
3. Scale Question

markdown
Copy code
{Q<number>:

<Question text>

!SCALE,<min value>,<max value>
}
Example:

markdown
Copy code
{Q10:

On a scale from 1 to 10, how would you rate the importance of protecting the environment?

!SCALE,1,10
}
4. Multiple Part Question

Each part is treated as a separate question but grouped under the main question label.

markdown
Copy code
{Q<number>_Part1:

<Part 1 Question text>

!FIELD
<Code> <Answer choice>
...
}

{Q<number>_Part2:

<Part 2 Question text>

!FIELD
<Code> <Answer choice>
...
}
Example:

markdown
Copy code
{Q20_Part1:

Part 1: How satisfied are you with the following aspects of your job?

!FIELD
01 VERY SATISFIED
02 SOMEWHAT SATISFIED
03 NEUTRAL
04 SOMEWHAT DISSATISFIED
05 VERY DISSATISFIED
}

{Q20_Part2:

Part 2: How likely are you to recommend your job to others?

!FIELD
01 VERY LIKELY
02 SOMEWHAT LIKELY
03 NEUTRAL
04 SOMEWHAT UNLIKELY
05 VERY UNLIKELY
}
5. Open-Ended Question

markdown
Copy code
{<Label>:

<Question text>

!OPEN
}
Example:

markdown
Copy code
{FEEDBACK:

Please provide any additional feedback or comments you may have.

!OPEN
}
6. Rating Question

markdown
Copy code
{Q<number>:

<Question text>

!RATING,<min value>,<max value>
<Code> <Label>
<Code> <Label>
...
}
Example:

markdown
Copy code
{Q15:

Please rate the following aspects of our service from 1 to 5, where 1 is Poor and 5 is Excellent.

!RATING,1,5
1 Poor
2 Fair
3 Good
4 Very Good
5 Excellent
}
File Structure

Root Directory
README.md: Project overview and setup instructions.
requirements.txt: List of required Python packages.
Directories
/src

Contains all the source code for the project.

main.py: The main script to run the Streamlit app.
parser.py: Functions for parsing survey documents.
generator.py: Functions for generating Markdown using GPT-4o mini.
ui.py: Functions for handling the Streamlit user interface.
/env

Contains environment configuration files.

.env: Environment variables (e.g., OpenAI API key).
Example File Structure
plaintext
Copy code
project-root/
│
├── README.md
├── requirements.txt
├── .env
│
├── src/
│   ├── main.py
│   ├── parser.py
│   ├── generator.py
│   └── ui.py
│
└── env/
    └── .env
=======
# StreamlitMarkdownProject
>>>>>>> 1593acfa12bf487155a44c51c966d17342fdc013
