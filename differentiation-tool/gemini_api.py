import os
import json
import re
import markdown
import google.generativeai as genai

def configure_gemini():
    """Configure the Gemini API with API key from environment"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

def markdown_to_html(text):
    """
    Convert markdown text to clean, formatted HTML

    Args:
        text: Markdown formatted text

    Returns:
        Clean HTML string with proper formatting
    """
    # Remove markdown code fences if present
    text = text.strip()

    # Remove triple backtick code fences
    text = re.sub(r'^```[\w]*\n', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n```$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```[\w]*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^```$', '', text, flags=re.MULTILINE)

    # Convert markdown to HTML with extensions for better formatting
    html = markdown.markdown(
        text,
        extensions=[
            'fenced_code',
            'codehilite',
            'tables',
            'nl2br',
            'sane_lists'
        ]
    )

    return html

def generate_suggestions(original_material, students_data):
    """
    Generate differentiation suggestions based on material and student profiles

    Args:
        original_material: The lesson/assignment text
        students_data: List of dicts with student info (name, accommodations, needs)

    Returns:
        List of suggestion dicts with structure:
        {
            'text': 'suggestion text',
            'applies_to': ['Student Name 1', 'Student Name 2']
        }
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        # Build student profiles text
        student_profiles = []
        for student in students_data:
            profile = f"- {student['name']}"
            if student.get('accommodations'):
                profile += f"\n  Accommodations: {student['accommodations']}"
            if student.get('needs'):
                profile += f"\n  Needs: {student['needs']}"
            student_profiles.append(profile)

        students_text = "\n".join(student_profiles)

        prompt = f"""You are an expert in educational differentiation for students with IEPs, 504 plans, and special accommodations.

ORIGINAL LESSON/ASSIGNMENT:
{original_material}

STUDENT PROFILES:
{students_text}

Your task is to analyze this lesson and the student profiles, then generate specific, actionable differentiation suggestions. For each suggestion:
1. Explain what modification should be made
2. Indicate which student(s) would benefit from this modification

Format your response as a JSON array of objects, where each object has:
- "text": the suggestion text
- "applies_to": array of student names this applies to

Example format:
[
    {{"text": "Provide a code template with pre-written class structure and comments", "applies_to": ["Jane D.", "504 Group"]}},
    {{"text": "Add a glossary defining 'class', 'object', 'method', and 'constructor'", "applies_to": ["Mike K."]}}
]

Focus on practical, concrete modifications that address the specific needs listed in the student profiles. Consider:
- Breaking down complex tasks into smaller steps
- Providing scaffolding and templates
- Adding visual aids or examples
- Simplifying language while maintaining rigor
- Offering alternative ways to demonstrate understanding
- Adjusting time requirements or deadlines

Return ONLY the JSON array, no other text."""

        response = model.generate_content(prompt)

        # Parse the JSON response
        try:
            # Clean the response text
            response_text = response.text.strip()
            # Remove markdown code blocks if present
            if response_text.startswith('```'):
                response_text = response_text.split('```')[1]
                if response_text.startswith('json'):
                    response_text = response_text[4:]
                response_text = response_text.strip()

            suggestions = json.loads(response_text)
            return suggestions
        except json.JSONDecodeError:
            # If JSON parsing fails, return a basic structure
            return [{
                'text': response.text,
                'applies_to': [s['name'] for s in students_data]
            }]

    except Exception as e:
        print(f"Error generating suggestions: {e}")
        # Return a fallback suggestion
        return [{
            'text': f"Error generating suggestions: {str(e)}. Please check your API key and try again.",
            'applies_to': []
        }]

def generate_differentiated_content(original_material, approved_suggestions):
    """
    Generate the final differentiated content incorporating all approved suggestions

    Args:
        original_material: The original lesson text
        approved_suggestions: List of approved suggestion texts

    Returns:
        HTML string containing the formatted differentiated content
    """
    try:
        configure_gemini()
        model = genai.GenerativeModel('gemini-2.0-flash-exp')

        suggestions_text = "\n".join([f"- {s}" for s in approved_suggestions])

        prompt = f"""You are an expert in educational differentiation. Create a final, polished version of this lesson that incorporates all the approved modifications.

ORIGINAL LESSON:
{original_material}

APPROVED MODIFICATIONS TO INCORPORATE:
{suggestions_text}

Create a complete, ready-to-use lesson document that:
1. Maintains the core learning objectives
2. Seamlessly integrates all the approved modifications
3. Is clearly organized and easy to follow
4. Preserves academic rigor while being accessible
5. Uses clear, professional formatting with headers and sections
6. Includes proper indentation for any code examples
7. Makes the content print-friendly and easy to read

IMPORTANT: Format your response in clean markdown. Use:
- Headers (# ## ###) for sections
- Code blocks with proper indentation for code examples
- Lists for step-by-step instructions
- Bold and italic for emphasis where appropriate

Do NOT wrap your response in markdown code fences (```). Just provide the formatted content directly."""

        response = model.generate_content(prompt)

        # Convert markdown to HTML
        html_content = markdown_to_html(response.text)

        return html_content

    except Exception as e:
        print(f"Error generating differentiated content: {e}")
        error_html = f"<div class='error'><h3>Error Generating Content</h3><p>{str(e)}</p><p>Please check your API configuration and try again.</p></div>"
        return error_html
