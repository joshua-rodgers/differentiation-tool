"""
Standalone Flask application for testing the Differentiation Tool blueprint locally.

This file is for development/testing purposes. On PythonAnywhere, the blueprint
will be registered in the main application file.

To run locally:
1. Set your GEMINI_API_KEY environment variable
2. Run: python app.py
3. Visit: http://localhost:5000/differentiation
"""

from flask import Flask, redirect
import os
import sys
import importlib.util

# Create Flask app
app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Import the blueprint from the hyphenated directory name
# Using importlib since "differentiation-tool" can't be imported directly
blueprint_path = os.path.join(os.path.dirname(__file__), 'differentiation-tool', '__init__.py')
spec = importlib.util.spec_from_file_location("differentiation_tool", blueprint_path)
differentiation_module = importlib.util.module_from_spec(spec)
sys.modules['differentiation_tool'] = differentiation_module
spec.loader.exec_module(differentiation_module)

# Register the blueprint - this will automatically initialize the database
app.register_blueprint(differentiation_module.bp)

# Root route redirects to blueprint
@app.route('/')
def index():
    return redirect('/differentiation')

if __name__ == '__main__':
    # Check for Gemini API key
    if not os.environ.get('GEMINI_API_KEY'):
        print("\n" + "="*70)
        print("WARNING: GEMINI_API_KEY environment variable not set!")
        print("="*70)
        print("\nThe differentiation suggestions will not work without a valid API key.")
        print("\nTo set it on Windows (PowerShell):")
        print('  $env:GEMINI_API_KEY="your-api-key-here"')
        print("\nTo set it on Windows (Command Prompt):")
        print('  set GEMINI_API_KEY=your-api-key-here')
        print("\nTo set it on Linux/Mac:")
        print('  export GEMINI_API_KEY="your-api-key-here"')
        print("\nGet your API key at: https://makersuite.google.com/app/apikey")
        print("="*70 + "\n")

    print("\n" + "="*70)
    print("Starting Differentiation Tool - Local Development Server")
    print("="*70)
    print("\nAccess the application at: http://localhost:5000/differentiation")
    print("\nPress CTRL+C to stop the server\n")
    print("="*70 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)
