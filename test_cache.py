#!/usr/bin/env python3
"""Simple test script to verify Gemini API cache creation"""

import os
import sys

# Set a dummy API key for testing (won't actually create cache without real key)
if 'GEMINI_API_KEY' not in os.environ:
    print("GEMINI_API_KEY not set - this test will verify token count logic")
    os.environ['GEMINI_API_KEY'] = 'test_key'

# Import the module
from differentiation_tool import gemini_api

# Load curriculum and calculate token estimate
curriculum_text = gemini_api.load_curriculum_standards()

# Simple token estimate (rough approximation: 1 token ≈ 4 characters)
curriculum_chars = len(curriculum_text)
curriculum_tokens_estimate = curriculum_chars // 4

print(f"Curriculum file loaded: {len(curriculum_text)} characters")
print(f"Estimated curriculum tokens: ~{curriculum_tokens_estimate}")

# Create the full cached content text (user message + model response)
differentiation_guide_sample = """DIFFERENTIATION BEST PRACTICES AND GUIDELINES:

When creating differentiation suggestions, consider these research-based strategies:

**Universal Design for Learning (UDL) Principles:**
1. Multiple Means of Representation - Present information in multiple formats (visual, auditory, text)
2. Multiple Means of Action and Expression - Allow students to demonstrate learning in various ways
3. Multiple Means of Engagement - Provide multiple pathways to motivate and engage learners
"""

# Estimate total cached content size
user_message = f"Curriculum standards + Differentiation guide"
# The actual user message would include both curriculum_text and the full differentiation guide
# which is several pages long in the actual code

# Rough estimate for the full cached content
system_instruction_estimate = 150  # tokens
differentiation_guide_estimate = 2300  # Expanded guide with detailed examples for all accommodation types
user_message_estimate = curriculum_tokens_estimate + differentiation_guide_estimate  # curriculum + differentiation guide
model_response_estimate = 350  # tokens (expanded response)

total_estimate = system_instruction_estimate + user_message_estimate + model_response_estimate

print(f"\nToken count estimates:")
print(f"  System instruction: ~{system_instruction_estimate} tokens")
print(f"  User message (curriculum + guide): ~{user_message_estimate} tokens")
print(f"  Model response: ~{model_response_estimate} tokens")
print(f"  TOTAL: ~{total_estimate} tokens")
print(f"\nMinimum required: 4096 tokens")
print(f"Status: {'✓ PASS - Above minimum' if total_estimate >= 4096 else '✗ FAIL - Below minimum'}")

# Try to actually create the cache if API key is valid
if os.environ.get('GEMINI_API_KEY') and os.environ['GEMINI_API_KEY'] != 'test_key':
    print("\n" + "="*60)
    print("Attempting to create actual cache with Gemini API...")
    print("="*60)
    try:
        cache = gemini_api.get_or_create_curriculum_cache()
        if cache:
            print(f"✓ SUCCESS: Cache created: {cache.name}")
        else:
            print("✗ FAILED: Cache creation returned None (fell back to non-cached mode)")
    except Exception as e:
        print(f"✗ ERROR: {e}")
else:
    print("\nSkipping actual cache creation (no valid GEMINI_API_KEY)")
    print("To test actual cache creation, set GEMINI_API_KEY environment variable")
