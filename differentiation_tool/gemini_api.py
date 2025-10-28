import os
import json
import re
import markdown
import google.generativeai as genai
from google.generativeai import caching
import datetime

# Cache object for curriculum standards (module-level to persist across requests)
_curriculum_cache = None
_cache_created_at = None

def configure_gemini():
    """Configure the Gemini API with API key from environment"""
    api_key = os.environ.get('GEMINI_API_KEY')
    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set")
    genai.configure(api_key=api_key)

def load_curriculum_standards():
    """Load curriculum standards from file"""
    curriculum_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        'Intro_CS.md'
    )

    try:
        with open(curriculum_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Warning: Curriculum standards file not found at {curriculum_path}")
        return ""

def parse_curriculum_standards():
    """
    Parse curriculum standards into a structured format for selection

    Returns:
        List of dicts with structure:
        {
            'domain': 'Domain 1',
            'domain_title': 'Careers and Professionalism',
            'standard': 'Standard 1.1',
            'standard_title': 'Demonstrate professional readiness...',
            'code': '1.1.1',
            'text': 'Demonstrate understanding of various career paths...'
        }
    """
    curriculum_text = load_curriculum_standards()
    if not curriculum_text:
        return []

    standards = []
    current_domain = None
    current_domain_title = None
    current_standard = None
    current_standard_title = None

    lines = curriculum_text.split('\n')

    for line in lines:
        line = line.strip()

        # Match domain headers (e.g., "## Domain 1 – Careers and Professionalism")
        domain_match = re.match(r'^##\s+Domain\s+(\d+)\s+[–-]\s+(.+)$', line)
        if domain_match:
            current_domain = f"Domain {domain_match.group(1)}"
            current_domain_title = domain_match.group(2).strip()
            continue

        # Match standard headers (e.g., "### Standard 1.1 – Demonstrate...")
        standard_match = re.match(r'^###\s+Standard\s+([\d.]+)\s+[–-]\s+(.+)$', line)
        if standard_match:
            current_standard = f"Standard {standard_match.group(1)}"
            current_standard_title = standard_match.group(2).strip()
            continue

        # Match performance indicators (e.g., "* **1.1.1** Text...")
        indicator_match = re.match(r'^\*\s+\*\*([\d.]+)\*\*\s+(.+)$', line)
        if indicator_match and current_domain and current_standard:
            code = indicator_match.group(1)
            text = indicator_match.group(2).strip()

            standards.append({
                'domain': current_domain,
                'domain_title': current_domain_title,
                'standard': current_standard,
                'standard_title': current_standard_title,
                'code': code,
                'text': text
            })

    return standards

def get_selected_standards_text(selected_codes):
    """
    Get the full text for selected standard codes

    Args:
        selected_codes: List of standard codes (e.g., ['1.1.1', '2.3.4'])

    Returns:
        Formatted string with selected standards
    """
    if not selected_codes:
        return ""

    all_standards = parse_curriculum_standards()
    selected = [s for s in all_standards if s['code'] in selected_codes]

    if not selected:
        return ""

    # Group by domain and standard
    grouped = {}
    for std in selected:
        domain_key = f"{std['domain']} – {std['domain_title']}"
        standard_key = f"{std['standard']} – {std['standard_title']}"

        if domain_key not in grouped:
            grouped[domain_key] = {}
        if standard_key not in grouped[domain_key]:
            grouped[domain_key][standard_key] = []

        grouped[domain_key][standard_key].append(std)

    # Format output
    output_lines = ["SELECTED CURRICULUM STANDARDS TO REFERENCE:\n"]

    for domain, standards in grouped.items():
        output_lines.append(f"\n{domain}")
        for standard, indicators in standards.items():
            output_lines.append(f"  {standard}")
            for indicator in indicators:
                output_lines.append(f"    • {indicator['code']}: {indicator['text']}")

    return "\n".join(output_lines)

def get_or_create_curriculum_cache():
    """Get existing cache or create new one for curriculum standards"""
    global _curriculum_cache, _cache_created_at

    configure_gemini()

    # Check if cache exists and is still valid (refresh every 6 hours)
    if _curriculum_cache and _cache_created_at:
        age = datetime.datetime.now() - _cache_created_at
        if age.total_seconds() < 6 * 3600:  # 6 hours
            return _curriculum_cache

    # Load curriculum standards
    curriculum_text = load_curriculum_standards()

    if not curriculum_text:
        return None

    try:
        # Create a new cache with the curriculum standards
        # Cache will expire after 1 hour by default
        # NOTE: The curriculum content must be in 'contents' parameter, not in system_instruction
        # This ensures the full document is cached and meets the minimum 4096 token requirement
        cache = caching.CachedContent.create(
            model='models/gemini-2.0-flash',
            display_name='intro_cs_curriculum',
            system_instruction="""You are an expert in educational differentiation for students with IEPs, 504 plans, and special accommodations.

You have deep knowledge of the Introduction to Computer Science curriculum standards that have been provided to you. Use this curriculum knowledge to inform all differentiation suggestions and ensure they align with course objectives and standards.

When generating differentiation suggestions:
- Align modifications with the relevant curriculum standards
- Reference specific standards by their codes (e.g., 2.1.1, 3.2.4) when appropriate
- Ensure adaptations maintain academic rigor and course goals
- Consider how modifications support students in meeting the learning objectives
- Balance accessibility with maintaining the integrity of the standards
""",
            contents=[
                {
                    'role': 'user',
                    'parts': [
                        {
                            'text': f"""Below are the Introduction to Computer Science curriculum standards. Please familiarize yourself with these standards as you will use them to inform differentiation suggestions.

INTRODUCTION TO COMPUTER SCIENCE CURRICULUM STANDARDS:

{curriculum_text}

Please confirm you have reviewed these standards and are ready to use them for differentiation guidance."""
                        }
                    ]
                },
                {
                    'role': 'model',
                    'parts': [
                        {
                            'text': """I have thoroughly reviewed the Introduction to Computer Science curriculum standards. I understand the five main domains:

1. Careers and Professionalism (Domain 1)
2. Computational Thinking (Domain 2)
3. Data Analysis and Visualization (Domain 3)
4. Major and Emerging Technologies (Domain 4)
5. Cybersecurity, Computer Systems, and Networking (Domain 5)

I'm ready to provide differentiation suggestions that align with these standards while ensuring accessibility for students with diverse learning needs. I will reference specific performance indicators when relevant and ensure that modifications maintain the academic rigor and learning objectives outlined in these standards."""
                        }
                    ]
                }
            ],
            ttl=datetime.timedelta(hours=1),
        )

        _curriculum_cache = cache
        _cache_created_at = datetime.datetime.now()

        print(f"Created curriculum cache: {cache.name}")
        return cache

    except Exception as e:
        print(f"Error creating cache: {e}")
        print("Falling back to non-cached mode")
        return None

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

def generate_suggestions(original_material, students_data, selected_standards=None):
    """
    Generate differentiation suggestions based on material and student profiles

    Args:
        original_material: The lesson/assignment text
        students_data: List of dicts with student info (name, accommodations, needs)
        selected_standards: Optional list of standard codes to focus on (e.g., ['1.1.1', '2.3.4'])

    Returns:
        List of suggestion dicts with structure:
        {
            'text': 'suggestion text',
            'applies_to': ['Student Name 1', 'Student Name 2']
        }
    """
    try:
        # Try to use cached curriculum context
        cache = get_or_create_curriculum_cache()

        if cache:
            # Use model with cached curriculum context
            model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        else:
            # Fall back to non-cached model
            configure_gemini()
            model = genai.GenerativeModel('gemini-2.0-flash')

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

        # Add selected standards context if provided
        standards_context = ""
        if selected_standards:
            standards_text = get_selected_standards_text(selected_standards)
            if standards_text:
                standards_context = f"\n\n{standards_text}\n\nIMPORTANT: Focus your differentiation suggestions on helping students meet these specific standards. Reference the standard codes (e.g., 2.1.1) in your suggestions when relevant.\n"

        prompt = f"""You are an expert in educational differentiation for students with IEPs, 504 plans, and special accommodations.

ORIGINAL LESSON/ASSIGNMENT:
{original_material}

STUDENT PROFILES:
{students_text}
{standards_context}
Your task is to analyze this lesson and the student profiles, then generate specific, actionable differentiation suggestions. For each suggestion:
1. Explain what modification should be made
2. Indicate which student(s) would benefit from this modification
3. If specific curriculum standards were provided, reference them by code when your suggestion helps address those standards

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
- Aligning with the curriculum standards provided

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
        # Try to use cached curriculum context
        cache = get_or_create_curriculum_cache()

        if cache:
            # Use model with cached curriculum context
            model = genai.GenerativeModel.from_cached_content(cached_content=cache)
        else:
            # Fall back to non-cached model
            configure_gemini()
            model = genai.GenerativeModel('gemini-2.0-flash')

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
