"""
Differentiation Tool Blueprint

A Flask blueprint for creating differentiated curriculum using Google Gemini API.
Designed for high school computer science teachers to adapt lessons for students
with accommodations, IEPs, and 504 plans.

Usage:
    from differentiation_tool import bp
    app.register_blueprint(bp)
"""

from . import db  # This will auto-initialize the database
from .routes import bp

__version__ = '1.0.0'
__all__ = ['bp']
