#!/usr/bin/env python3
"""Simple verification of cache token count without requiring dependencies"""

import os
import re

# Read the curriculum file
curriculum_path = 'Intro_CS.md'
with open(curriculum_path, 'r', encoding='utf-8') as f:
    curriculum_text = f.read()

# Read the gemini_api.py file to extract cached content
api_file_path = 'differentiation_tool/gemini_api.py'
with open(api_file_path, 'r', encoding='utf-8') as f:
    api_code = f.read()

# Extract the cached content between the specific markers
# Find the differentiation guide section
guide_start = api_code.find('DIFFERENTIATION BEST PRACTICES AND GUIDELINES:')
guide_end = api_code.find('Please confirm you have reviewed these comprehensive standards')

if guide_start > 0 and guide_end > 0:
    differentiation_guide = api_code[guide_start:guide_end + 150]
else:
    differentiation_guide = ""
    print("Warning: Could not extract differentiation guide")

# Extract the model response
response_start = api_code.find('I have thoroughly reviewed the Introduction to Computer Science')
response_end = api_code.find('will ensure all suggestions are feasible')

if response_start > 0 and response_end > 0:
    model_response = api_code[response_start:response_end + 200]
else:
    model_response = ""
    print("Warning: Could not extract model response")

# Simple token estimate (rough approximation: 1 token ≈ 4 characters)
curriculum_tokens = len(curriculum_text) // 4
guide_tokens = len(differentiation_guide) // 4
response_tokens = len(model_response) // 4
system_instruction_tokens = 150  # Estimated

total_tokens = curriculum_tokens + guide_tokens + response_tokens + system_instruction_tokens

print("=" * 70)
print("CACHE TOKEN COUNT VERIFICATION")
print("=" * 70)
print(f"\nCurriculum file ({curriculum_path}):")
print(f"  Characters: {len(curriculum_text):,}")
print(f"  Estimated tokens: ~{curriculum_tokens:,}")

print(f"\nDifferentiation guide:")
print(f"  Characters: {len(differentiation_guide):,}")
print(f"  Estimated tokens: ~{guide_tokens:,}")

print(f"\nModel response:")
print(f"  Characters: {len(model_response):,}")
print(f"  Estimated tokens: ~{response_tokens:,}")

print(f"\nSystem instruction:")
print(f"  Estimated tokens: ~{system_instruction_tokens:,}")

print(f"\n{'-' * 70}")
print(f"TOTAL ESTIMATED TOKENS: ~{total_tokens:,}")
print(f"Minimum required: 4,096 tokens")
print(f"{'-' * 70}")

if total_tokens >= 4096:
    print(f"✓ PASS - Cache content is {total_tokens - 4096:,} tokens above minimum")
    print("  The cache should be created successfully!")
else:
    print(f"✗ FAIL - Cache content is {4096 - total_tokens:,} tokens below minimum")
    print("  You will see: 'Error creating cache: 400 Cached content is too small'")

print("\nNote: These are estimates using ~4 characters per token.")
print("Actual token counts may vary slightly based on tokenization.")
print("=" * 70)
