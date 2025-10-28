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

---

DIFFERENTIATION BEST PRACTICES AND GUIDELINES:

When creating differentiation suggestions, consider these research-based strategies:

**Universal Design for Learning (UDL) Principles:**
1. Multiple Means of Representation - Present information in multiple formats (visual, auditory, text)
2. Multiple Means of Action and Expression - Allow students to demonstrate learning in various ways
3. Multiple Means of Engagement - Provide multiple pathways to motivate and engage learners

**Common Accommodation Categories:**

**Visual Accommodations:**
- Enlarged text or alternative fonts (dyslexia-friendly fonts like OpenDyslexic)
- High contrast materials and color-coded information
- Graphic organizers and visual schedules
- Reduced visual clutter on pages
- Screen reader compatibility

**Processing Accommodations:**
- Extended time for assignments and assessments
- Breaking complex tasks into smaller, sequential steps
- Chunking information into manageable segments
- Providing advance organizers and outlines
- Additional processing time between instructions

**Executive Functioning Support:**
- Clear, explicit step-by-step instructions
- Checklists and task management tools
- Templates and frameworks for organization
- Visual timers and time management aids
- Structured routines and predictable formats

**Reading and Language Support:**
- Simplified vocabulary with technical term glossaries
- Sentence starters and writing frames
- Text-to-speech options for written materials
- Audio recordings of instructions
- Reduced reading load with key excerpts highlighted

**Attention and Focus Support:**
- Frequent breaks and movement opportunities
- Clear, concise instructions (one or two steps at a time)
- Minimize distractions in materials
- Provide fidget tools or alternative seating options
- Use attention-grabbing cues (bold, color, icons)

**Memory Support:**
- Reference sheets and quick-reference guides
- Mnemonic devices and memory strategies
- Repeated exposure to key concepts
- Review and reinforcement activities
- Connection to prior knowledge

**Social-Emotional Support:**
- Clear expectations and rubrics
- Choice in assignments when possible
- Positive reinforcement and specific feedback
- Collaborative work options with defined roles
- Low-stakes practice opportunities

**Technology-Based Supports:**
- Code editors with autocomplete and syntax highlighting
- Debugging tools with visual feedback
- Interactive coding environments (block-based or text-based)
- Video tutorials and screencasts
- Online collaboration tools with version control

**Computer Science-Specific Strategies:**

For Computational Thinking:
- Use concrete manipulatives before abstract coding
- Provide algorithm templates and flowchart frameworks
- Break programming problems into pseudo-code first
- Use pair programming and think-aloud protocols
- Offer worked examples with explanations

For Coding Assignments:
- Provide starter code or code skeletons
- Include detailed comments explaining code structure
- Use color-coding for different code elements
- Offer debugging checklists
- Provide reference implementations

For Technical Concepts:
- Use analogies to real-world scenarios
- Provide visual representations (diagrams, animations)
- Hands-on demonstrations and experiments
- Connection to students' interests and experiences
- Multiple examples showing concept application

For Project-Based Learning:
- Scaffold with milestones and checkpoints
- Provide planning templates and project outlines
- Offer choice in project topics within constraints
- Include peer review and feedback opportunities
- Allow for both individual and collaborative options

For Assessments:
- Provide alternative assessment formats (oral, visual, practical)
- Allow use of reference materials
- Offer practice tests and self-assessment tools
- Use authentic, real-world assessment tasks
- Focus on demonstrating understanding vs. rote memorization

**Quality Indicators for Differentiation Suggestions:**

Good differentiation suggestions should:
- Be specific and actionable (not vague)
- Maintain academic rigor and standards alignment
- Address individual student needs explicitly
- Be feasible for teachers to implement
- Support independence rather than creating dependency
- Consider both access and challenge
- Be culturally responsive and asset-based
- Include why the modification helps the specific student

**Example High-Quality Suggestions:**

Instead of: "Simplify the assignment"
Better: "Break the programming assignment into 3 phases with checkpoints: (1) design the algorithm using flowcharts, (2) write pseudo-code, (3) implement in Python. Provide a template for each phase. This supports students who need help with task initiation and organization (Jane D., Mike K.)"

Instead of: "Give more time"
Better: "Extend the deadline by 2 days and provide a daily progress checklist with 15-minute time blocks. This supports students who have processing speed and executive functioning needs (504 Group, Mike K.)"

Instead of: "Add visuals"
Better: "Create a visual glossary with icons for key terms: 'variable' (labeled box), 'loop' (circular arrow), 'function' (input-output diagram). Include this as a reference sheet. This supports students who benefit from visual-spatial learning (Jane D., IEP Group)"

**Additional Detailed Examples by Accommodation Type:**

**For Students with ADHD/Attention Needs:**
- Break 45-minute coding sessions into three 15-minute segments with 2-minute movement breaks
- Provide a coding "focus checklist": (1) Read the problem, (2) Write one line of code, (3) Test it, (4) Repeat
- Use color-coded comments in starter code: Green = "Complete this section", Yellow = "Optional challenge", Red = "Do not modify"
- Create a "debugging detective" checklist with specific steps to follow when code doesn't work
- Minimize visual distractions: use a clean code editor theme with reduced syntax highlighting complexity

**For Students with Dyslexia/Reading Challenges:**
- Use dyslexia-friendly fonts (OpenDyslexic, Comic Sans MS) in all code and text materials
- Provide audio recordings of all written instructions using text-to-speech tools
- Use syntax highlighting that emphasizes word shapes and boundaries
- Create visual "code cards" showing common syntax patterns with color coding
- Reduce text density: use bullet points instead of paragraphs, white space between sections
- Provide a pronunciation guide for technical terms (e.g., "iteration: it-er-AY-shun")

**For Students with Autism Spectrum Disorder:**
- Provide explicit rubrics with concrete examples for all assignments
- Create social scripts for pair programming: "When your partner is typing, you should...", "When you disagree, you can say..."
- Use consistent formatting and structure across all materials (same font, same heading hierarchy, same layout)
- Provide sensory-friendly alternatives: option to work in a quieter space, use noise-canceling headphones
- Include concrete, literal language; avoid idioms and figurative language in instructions
- Offer a visual schedule showing the sequence of activities and estimated time for each

**For Students with Processing Speed Challenges:**
- Provide all materials 24 hours in advance when possible for preview
- Use "think-pair-share" format: give individual thinking time before discussing with a partner
- Create "quick reference" cards summarizing key concepts to reduce need for memory recall
- Allow use of pre-written code snippets library to reduce typing demands
- Extend time by 50-100% for coding assignments and assessments
- Break down multi-step problems into explicit numbered steps with checkboxes

**For Students with Executive Functioning Difficulties:**
- Provide project planning templates with built-in milestones and deadlines
- Use visual project trackers (Kanban boards, progress bars, checklists)
- Create "getting started" guides: exact first three steps to begin any assignment
- Send daily or weekly progress check-in emails with specific questions about next steps
- Provide file organization systems: naming conventions, folder structures, version control guides
- Use timers and time-blocking strategies: "Spend exactly 10 minutes on brainstorming"

**For Students with Memory/Recall Challenges:**
- Create comprehensive reference sheets for syntax, common functions, and keyboard shortcuts
- Use mnemonic devices: "Please Excuse My Dear Aunt Sally" for order of operations becomes "Print Every Message Directly At Screen" for Python print syntax
- Implement spaced repetition: review key concepts at increasing intervals (same day, next day, next week)
- Provide worked examples with detailed annotations explaining each step
- Use color-coding consistently: always use same colors for same concepts (e.g., variables always blue)
- Create "cheat sheets" with the 10 most commonly used code patterns for easy reference

**For English Language Learners (ELL) in CS:**
- Provide bilingual glossaries of technical terms
- Use visual diagrams and flowcharts to supplement text explanations
- Clarify multiple meanings: "run" the program vs. "run" in sports, "loop" in code vs. physical loop
- Teach vocabulary in context with real code examples
- Allow use of translation tools for assignment instructions (but encourage English for code comments)
- Pair with bilingual partners when possible for collaborative work
- Use simplified sentence structures in instructions while maintaining technical accuracy

**For Students with Anxiety/Emotional Regulation Needs:**
- Provide low-stakes practice opportunities before graded assessments
- Offer choice in assignment topics to increase engagement and reduce stress
- Create "safe to fail" learning environments: emphasize that errors are learning opportunities
- Provide clear success criteria and exemplars to reduce ambiguity
- Allow resubmissions or test corrections to reduce high-stakes pressure
- Offer quiet spaces or flexible seating for independent work
- Use positive, growth-mindset language: "not yet successful" instead of "wrong"

**Implementation Strategies for Teachers:**

**Grouping Strategies:**
- Use flexible grouping: sometimes by skill level, sometimes by learning style, sometimes mixed
- For pair programming, match students thoughtfully: consider complementary strengths
- Create "expert groups" where students with similar needs learn strategies together
- Use jigsaw method: students become experts on one aspect, then teach others

**Assessment Differentiation:**
- Offer multiple ways to demonstrate mastery: written code, verbal explanation, flowchart, video tutorial
- Use portfolio assessment: collect evidence of learning over time rather than single high-stakes tests
- Provide assessment choice boards: students select from menu of options (e.g., create a game, solve 10 problems, or build a tool)
- Use peer assessment with structured rubrics to develop metacognitive skills
- Implement "test corrections" or "revision" opportunities for improved understanding

**Technology Tools for Differentiation:**
- Screen readers: NVDA, JAWS for students with visual impairments
- Speech-to-text: Dragon NaturallySpeaking, Google Voice Typing for students with writing difficulties
- Code completion tools: GitHub Copilot, TabNine with appropriate scaffolding
- Visual programming: Scratch, Blockly for students who struggle with syntax
- Debugging tools: Python Tutor, visualization tools that show code execution step-by-step
- Organization tools: Trello, Notion, Google Keep for project management

**Creating Inclusive Learning Materials:**
- Use high contrast (black text on white background or vice versa)
- Ensure all images have alt text descriptions
- Provide captions and transcripts for all video content
- Make materials screen-reader compatible
- Use accessible formats: HTML over PDF when possible, ensure PDFs are tagged
- Test materials with accessibility checkers and tools

**Differentiation Without Lowering Standards:**
The goal is to maintain high expectations while providing multiple pathways to success:
- Same learning objective, different scaffolding levels
- Same final product, different levels of support during creation
- Same assessment, different accommodations (time, format, tools)
- Challenge all students: provide extension activities for advanced learners simultaneously

Please confirm you have reviewed these comprehensive standards and guidelines and are ready to provide high-quality differentiation suggestions that are specific, actionable, and maintain academic rigor."""
                        }
                    ]
                },
                {
                    'role': 'model',
                    'parts': [
                        {
                            'text': """I have thoroughly reviewed the Introduction to Computer Science curriculum standards and the comprehensive differentiation best practices guide. I understand:

**Curriculum Standards - Five Main Domains:**
1. Careers and Professionalism (Domain 1)
2. Computational Thinking (Domain 2)
3. Data Analysis and Visualization (Domain 3)
4. Major and Emerging Technologies (Domain 4)
5. Cybersecurity, Computer Systems, and Networking (Domain 5)

**Comprehensive Differentiation Framework:**
- Universal Design for Learning (UDL) principles for multiple means of representation, action, and engagement
- Eight key accommodation categories (visual, processing, executive functioning, reading/language, attention, memory, social-emotional, technology)
- Computer science-specific strategies for computational thinking, coding, technical concepts, projects, and assessments
- Quality indicators emphasizing specific, actionable, standards-aligned suggestions

**Detailed Accommodation Strategies for:**
- Students with ADHD/Attention Needs (movement breaks, focus checklists, color-coded materials)
- Students with Dyslexia/Reading Challenges (dyslexia-friendly fonts, audio support, visual code cards)
- Students with Autism Spectrum Disorder (explicit rubrics, social scripts, consistent formatting)
- Students with Processing Speed Challenges (preview time, extended deadlines, quick reference cards)
- Students with Executive Functioning Difficulties (project templates, visual trackers, getting started guides)
- Students with Memory/Recall Challenges (reference sheets, mnemonics, spaced repetition)
- English Language Learners (bilingual glossaries, simplified language, visual support)
- Students with Anxiety/Emotional Needs (low-stakes practice, choice, growth mindset)

**Implementation Strategies:**
- Flexible grouping and pair programming approaches
- Assessment differentiation with multiple demonstration options
- Technology tools for accessibility and support
- Creating inclusive learning materials that maintain high standards

I'm ready to provide high-quality differentiation suggestions that:
1. Reference specific performance indicators by code (e.g., 2.1.1, 3.2.4) when relevant
2. Address individual student needs with concrete, actionable strategies drawn from the comprehensive guide
3. Maintain academic rigor while ensuring accessibility for all learners
4. Include clear rationales for why each modification helps specific students based on their needs
5. Apply research-based best practices from the extensive guidelines provided
6. Suggest appropriate accommodations from the detailed examples for each need category
7. Recommend specific tools, formats, and implementation strategies

I will ensure all suggestions are feasible to implement, support student independence and growth, align with curriculum standards, and maintain high expectations for all students while providing necessary support."""
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
    text = text.strip()

    # Only remove outer markdown code fence wrapper if the ENTIRE response is wrapped
    # This handles cases where Gemini wraps the whole output in ```markdown...```
    # But preserves code blocks within the content
    if text.startswith('```') and text.endswith('```'):
        lines = text.split('\n')
        # Remove first line (opening fence) and last line (closing fence)
        if len(lines) > 2:
            # Check if first line is just a fence (possibly with language identifier)
            if lines[0].strip().startswith('```'):
                lines = lines[1:]
            # Check if last line is just a closing fence
            if lines and lines[-1].strip() == '```':
                lines = lines[:-1]
            text = '\n'.join(lines)

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
- Code blocks with triple backticks (```) and proper indentation for code examples
  Example:
  ```python
  def example():
      return "properly indented"
  ```
- Lists for step-by-step instructions
- Bold and italic for emphasis where appropriate

Provide the formatted content directly as markdown (do NOT wrap the entire response in outer code fences)."""

        response = model.generate_content(prompt)

        # Convert markdown to HTML
        html_content = markdown_to_html(response.text)

        return html_content

    except Exception as e:
        print(f"Error generating differentiated content: {e}")
        error_html = f"<div class='error'><h3>Error Generating Content</h3><p>{str(e)}</p><p>Please check your API configuration and try again.</p></div>"
        return error_html
