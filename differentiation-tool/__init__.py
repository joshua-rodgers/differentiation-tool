"""
Differentiation Tool Blueprint

A Flask blueprint for creating differentiated curriculum using Google Gemini API.
Designed for high school computer science teachers to adapt lessons for students
with accommodations, IEPs, and 504 plans.
"""

from flask import Blueprint
from . import db  # This will auto-initialize the database
from .routes import bp

__version__ = '1.0.0'

def init_app(app):
    """
    Initialize the blueprint with the Flask app

    Usage in main app:
        from differentiation-tool import bp, init_app
        app.register_blueprint(bp)
        init_app(app)
    """
    pass
