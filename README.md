# DiffF - AI-Powered Curriculum Differentiation Tool

An AI-powered Flask blueprint that helps high school computer science teachers create differentiated curriculum for students with accommodations, IEPs, and 504 plans using the Google Gemini API.

## Features

- **Teacher Account Management**: Secure signup and login system
- **Student Profile Management**: Store student information, accommodations, and learning needs
- **Group Management**: Organize students into groups for easier differentiation
- **4-Phase Differentiation Workflow**:
  1. **Input**: Enter lesson material and select students
  2. **Suggestions**: AI generates differentiation suggestions
  3. **Refine**: Review and select which suggestions to apply
  4. **Generate**: Create final differentiated content
- **Lesson Library**: Save and manage differentiated lessons
- **Mobile-Friendly**: Fully optimized for mobile devices including iPhone SE
- **Self-Contained**: SQLite database included in blueprint directory

## Project Structure

```
differentiation_tool/
├── app.py                          # Standalone test application
├── requirements.txt                # Python dependencies
├── README.md                       # This file
├── user_flow.md                    # User workflow documentation
├── difff_landing.png               # Design mockup
└── differentiation_tool/           # Blueprint directory
    ├── __init__.py                 # Blueprint initialization
    ├── routes.py                   # All route handlers
    ├── db.py                       # Database functions (auto-initializes)
    ├── gemini_api.py               # Google Gemini API integration
    ├── differentiation.db          # SQLite database (created on first run)
    ├── templates/
    │   └── differentiation_tool/   # HTML templates
    │       ├── base.html
    │       ├── landing.html
    │       ├── login.html
    │       ├── signup.html
    │       ├── dashboard.html
    │       ├── students.html
    │       ├── groups.html
    │       ├── new_differentiation.html
    │       ├── suggestions.html
    │       ├── final_content.html
    │       ├── library.html
    │       └── view_lesson.html
    └── static/
        └── differentiation_tool/   # CSS and JavaScript
            ├── style.css           # Main styles with dark theme
            ├── mobile.css          # Mobile-specific styles
            └── script.js           # Client-side functionality
```

## Setup Instructions

### Local Development (Windows)

1. **Clone or download this repository**

2. **Install Python 3.8 or higher**
   - Download from [python.org](https://www.python.org/downloads/)
   - Make sure to check "Add Python to PATH" during installation

3. **Open PowerShell or Command Prompt and navigate to the project directory**
   ```powershell
   cd path\to\differentiation-tool
   ```

4. **Create a virtual environment (recommended)**
   ```powershell
   python -m venv venv
   .\venv\Scripts\activate
   ```

5. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

6. **Get a Google Gemini API key**
   - Visit [https://makersuite.google.com/app/apikey](https://makersuite.google.com/app/apikey)
   - Create a new API key
   - Copy the key

7. **Set environment variables**

   **PowerShell:**
   ```powershell
   $env:GEMINI_API_KEY="your-api-key-here"
   $env:SECRET_KEY="any-random-secret-key-for-sessions"
   ```

   **Command Prompt:**
   ```cmd
   set GEMINI_API_KEY=your-api-key-here
   set SECRET_KEY=any-random-secret-key-for-sessions
   ```

8. **Run the application**
   ```powershell
   python app.py
   ```

9. **Open your browser and visit**
   ```
   http://localhost:5000/diff
   ```

### Deployment on PythonAnywhere

1. **Upload the `differentiation_tool` directory** to your PythonAnywhere account

2. **In your main Flask application file** (usually `flask_app.py` or similar):
   ```python
   from flask import Flask
   import sys

   app = Flask(__name__)
   app.config['SECRET_KEY'] = 'your-production-secret-key'

   # Add the directory containing differentiation_tool to Python path
   sys.path.insert(0, '/home/yourusername')

   # Import and register the blueprint
   from differentiation_tool import bp
   app.register_blueprint(bp)

   # Your other blueprints...
   ```

3. **Set environment variables** in PythonAnywhere:
   - Go to the "Web" tab
   - Scroll to "Environment variables"
   - Add `GEMINI_API_KEY` with your API key

4. **Reload your web app**

The blueprint will be available at `/diff` (e.g., `https://yourusername.pythonanywhere.com/diff`)

## Usage Guide

### Getting Started

1. **Sign Up**: Create a teacher account on the landing page
2. **Add Students**: Go to "Students" and add your students with their accommodations and needs
3. **Create Groups** (Optional): Organize students into groups like "504 Group" or "IEP Group"
4. **Differentiate a Lesson**: Click "Differentiate a New Lesson" on the dashboard

### The 4-Phase Workflow

#### Phase 1: Input
- Enter your lesson title (e.g., "OOP Project: Design a 'Pet' class")
- Paste your original lesson material
- Select individual students and/or groups

#### Phase 2: Suggestions
- The AI analyzes your material and student profiles
- View differentiation suggestions tailored to each student's needs
- Each suggestion shows which students it applies to

#### Phase 3: Refine
- Review all suggestions
- Use "Select All" or choose specific suggestions to apply
- Deselect any suggestions you don't want

#### Phase 4: Generate
- The AI creates a complete differentiated lesson
- Review the final content
- Save to your Lesson Library
- Print or use the lesson with your students

### Managing Your Content

- **Students Page**: Add, edit, or delete student profiles
- **Groups Page**: Create and manage student groups
- **Lesson Library**: Access all your saved differentiated lessons
- **Dashboard**: Overview of your account and quick access to recent work

## Mobile Usage

The app is fully optimized for mobile devices:
- Hamburger menu for navigation on small screens
- Tables convert to stacked cards on mobile
- All forms optimized for touch input
- Tested on iPhone SE and larger devices

## Database

The app uses SQLite with the following tables:
- `users` - Teacher accounts
- `students` - Student profiles with accommodations
- `groups` - Student groups
- `group_members` - Students in each group
- `diff_sessions` - Differentiation workflow sessions
- `session_students` - Students involved in each session
- `lessons` - Saved differentiated lessons

The database is automatically created when the blueprint is imported.

## API Usage

The app uses Google Gemini API for:
- Analyzing lesson material
- Generating differentiation suggestions based on student profiles
- Creating final differentiated content

**Important**: The Gemini API has usage limits and costs. Check [Google's pricing](https://ai.google.dev/pricing) for current rates.

## Troubleshooting

### API Key Not Working
- Verify your key is set: `echo $env:GEMINI_API_KEY` (PowerShell)
- Make sure there are no extra spaces or quotes
- Check that your API key is active at Google AI Studio

### Database Errors
- The database file is created automatically in the blueprint directory
- If you get permission errors, check folder permissions
- Delete `differentiation.db` to reset the database

### Import Errors
- Make sure all files are in the correct directory structure
- Verify `requirements.txt` packages are installed
- Check that Python is finding the blueprint directory

### Mobile Menu Not Working
- Clear your browser cache
- Make sure `script.js` is loading (check browser console)
- Try a different browser

## Security Notes

- Change the `SECRET_KEY` in production
- Never commit API keys to version control
- Use HTTPS in production
- The app uses password hashing with Werkzeug

## Credits

- Built with Flask
- Powered by Google Gemini API
- Designed for high school computer science teachers

## License

This project is designed as an MVP for teacher feedback and iteration.

## Support

For issues or questions, please refer to the project documentation or contact the developer.
