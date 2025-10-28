# DiffTool User Guide

## Table of Contents
1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Managing Students](#managing-students)
4. [Creating Differentiated Materials](#creating-differentiated-materials)
5. [Best Practices](#best-practices)
6. [Examples](#examples)
7. [Library & Reusing Materials](#library--reusing-materials)
8. [Tips & Troubleshooting](#tips--troubleshooting)

---

## Introduction

**DiffTool** is an AI-powered differentiation assistant for high school computer science teachers. It helps you create customized curriculum materials for students with IEPs, 504 plans, and special accommodations using Google's Gemini AI.

### What DiffTool Does

- **Analyzes** your lesson plans and assignments
- **Generates** differentiation suggestions based on student needs
- **Creates** customized materials that maintain academic rigor while addressing accommodations
- **References** curriculum standards to ensure alignment with course objectives
- **Saves** your differentiated lessons for future use

### Key Features

- 4-phase AI-assisted differentiation workflow
- Student profile management with accommodation tracking
- Group organization for common assignments
- Lesson library for reusing materials
- Mobile-friendly interface for on-the-go access
- Print-optimized output for classroom use

---

## Getting Started

### 1. Account Creation

1. Navigate to the DiffTool landing page
2. Click "Sign Up"
3. Fill in your information:
   - Email address
   - Password (minimum 8 characters)
   - First and last name
4. Click "Create Account"

**Note:** New accounts require admin approval before you can log in. You'll receive a message indicating your account is pending activation.

### 2. First Login

Once your account is activated by an administrator:

1. Click "Login"
2. Enter your email and password
3. You'll be taken to your dashboard

### 3. Dashboard Overview

Your dashboard shows:
- **Quick Stats**: Number of students, groups, and saved lessons
- **Quick Actions**: Create new differentiation, manage students/groups
- **Active Sessions**: Drafts you've started but not completed
- **Recent Lessons**: Your last 5 saved differentiated materials

---

## Managing Students

Before creating differentiated materials, you need to add student profiles. Student information helps the AI generate appropriate accommodations.

### Adding a Student

1. From the dashboard, click "Manage Students"
2. Click "Add New Student"
3. Fill in the student information:
   - **First & Last Name** (required)
   - **Grade Level**: Student's current grade
   - **Accommodations**: Specific accommodations (extended time, assistive tech, etc.)
   - **IEP/504 Information**: Learning disabilities, processing issues, etc.
   - **Additional Needs**: Communication preferences, learning styles, strengths

**Example Student Profile:**
```
Name: Alex Johnson
Grade: 10
Accommodations: Extended time (1.5x), Use of speech-to-text software,
                Frequent breaks, Preferential seating
IEP Information: ADHD, Processing speed challenges, Working memory deficits
Additional Needs: Strong visual learner, Excels with hands-on activities,
                  Needs clear step-by-step instructions
```

### Editing Students

1. Go to "Manage Students"
2. Click "Edit" next to any student
3. Update information as needed
4. Click "Update Student"

**Tip:** Keep student profiles updated as you learn more about their needs and strengths throughout the year.

### Organizing Students into Groups

Groups let you quickly select multiple students who often work together or share accommodations.

1. From the dashboard, click "Manage Groups"
2. Click "Add New Group"
3. Give the group a name (e.g., "Period 3 Advanced", "Resource Room Students")
4. Select students to include
5. Click "Create Group"

**Common Group Types:**
- Class periods
- Ability levels
- Students with similar accommodations
- Project teams

---

## Creating Differentiated Materials

The differentiation process has 4 phases:

### Phase 1: Input Material & Select Students

1. From the dashboard, click "Create New Differentiation"
2. **Paste your original material**: This can be:
   - A lesson plan
   - An assignment description
   - A project outline
   - Assessment instructions
   - Reading material with comprehension questions

3. **Select students**: Choose individual students or entire groups
4. Click "Continue to Suggestions"

**What happens:** The AI analyzes your material and student profiles, then generates differentiation suggestions.

### Phase 2: Review AI Suggestions

The AI presents suggested modifications. Each suggestion:
- Explains what to change and why
- Lists which students it applies to
- Maintains alignment with curriculum standards

**Your options:**
- **Review each suggestion**: Read and understand the proposed changes
- **Select/Deselect**: Check or uncheck suggestions you want to apply
- **Select All/Deselect All**: Quick buttons for bulk selection

**Example Suggestions:**
```
✓ Break the project into smaller milestones with checkpoints after each phase
  Applies to: Alex Johnson, Maria Garcia

✓ Provide a code template with comments indicating where students should
  write their solutions
  Applies to: Alex Johnson

✓ Allow verbal explanation of code logic as alternative to written comments
  Applies to: Maria Garcia
```

Click "Continue to Generate Content" when you've selected your preferred suggestions.

### Phase 3: Generate Final Content

The AI creates a complete, differentiated version of your material incorporating all approved suggestions.

**What you get:**
- Fully rewritten lesson/assignment
- Integrated accommodations
- Clear instructions
- Formatted for readability
- Print-optimized layout

### Phase 4: Save & Use

**Review the output:**
- Read through the differentiated material
- Check that all accommodations are properly integrated
- Verify content accuracy

**Save to library:**
1. Give your lesson a descriptive title
2. Click "Save to Library"
3. The material is now available for future use

**Or skip saving:**
- Click "Print" to print the material immediately
- Navigate away if you don't want to save

---

## Best Practices

### Writing Effective Original Materials

The better your input, the better the AI's suggestions. Include:

**✓ Clear objectives**
```
Students will be able to:
- Implement a binary search algorithm
- Analyze time complexity
- Compare binary search to linear search
```

**✓ Specific instructions**
```
Write a Python function that accepts a sorted list and target value,
returns the index of the target using binary search algorithm.
```

**✓ Assessment criteria**
```
Rubric:
- Correct implementation: 40 points
- Proper documentation: 20 points
- Time complexity analysis: 20 points
- Testing & edge cases: 20 points
```

**✗ Avoid vague descriptions**
```
Bad: "Do a programming thing with searching"
Good: "Implement binary search in Python with a sorted integer array"
```

### Creating Detailed Student Profiles

**Include:**
- Specific diagnosis/disability information
- Concrete accommodation needs
- Learning strengths and preferences
- Communication needs
- Technology requirements

**Example - Strong Profile:**
```
Name: Jordan Lee
Accommodations: Extended time (2x), Noise-canceling headphones,
                Calculator allowed, Separate testing location
IEP Information: Dyscalculia, Anxiety disorder, Auditory processing disorder
Additional Needs: Needs written instructions in addition to verbal,
                  Strong with visual diagrams and flowcharts,
                  Prefers working alone,
                  Benefits from examples before starting work
```

**Example - Weak Profile:**
```
Name: Jordan Lee
Accommodations: Extra time
IEP Information: Learning disability
Additional Needs: Needs help
```

### Getting the Best AI Suggestions

**Do:**
- Provide complete original materials with context
- Include learning objectives
- Specify skills being assessed
- Note any prerequisites
- Mention if this builds on previous lessons

**Don't:**
- Submit single-sentence descriptions
- Leave out important details
- Assume the AI knows your classroom context
- Skip student profile details

### Working with Suggestions

**Review critically:**
- Some suggestions may not fit your teaching style
- Some accommodations may duplicate existing supports
- Consider implementation feasibility

**Deselect suggestions that:**
- Oversimplify content inappropriately
- Create more work than benefit
- Don't align with your classroom management
- Duplicate accommodations you're already providing

**You're the expert:** The AI assists your professional judgment—it doesn't replace it.

---

## Examples

### Example 1: Simple Coding Assignment

**Scenario:** You're assigning a basic Python loops exercise to Period 2. Alex (ADHD, processing speed issues) and Sam (dyslexia, working memory challenges) need accommodations.

**Step 1 - Original Material:**
```
Python Loops Practice

Write a program that:
1. Asks the user for a number
2. Uses a for loop to print all even numbers from 0 to that number
3. Uses a while loop to calculate the sum of odd numbers from 1 to that number
4. Prints both results

Requirements:
- Proper variable names
- Comments explaining your code
- Input validation (handle non-numeric input)

Due: Friday, submit via Google Classroom
```

**Step 2 - AI Suggestions:**
```
✓ Provide a code template with function stubs and TODO comments
  Applies to: Alex, Sam

✓ Break into three separate files: Part 1 (even numbers),
  Part 2 (odd sum), Part 3 (input validation)
  Applies to: Alex

✓ Include a visual flowchart showing the program logic
  Applies to: Alex, Sam

✓ Allow submission in multiple parts with individual deadlines
  (Part 1: Wednesday, Part 2: Thursday, Part 3: Friday)
  Applies to: Alex

✓ Provide example output to clarify expectations
  Applies to: Sam

✓ Allow code comments to be verbal explanations recorded as audio files
  Applies to: Sam
```

**Step 3 - Generated Output:**
The AI creates a version with:
- Separate starter files for each part
- Visual flowchart included
- Code templates with TODO markers
- Example input/output shown
- Staggered deadlines noted
- Alternative comment options explained

### Example 2: Complex Project with Multiple Students

**Scenario:** You're assigning a final project—build a text-based game. Your resource room group (5 students with varied needs) will work on this.

**Step 1 - Original Material:**
```
Final Project: Text-Based Adventure Game

Create an interactive text-based adventure game in Python that includes:

Required Features:
- At least 5 rooms/locations
- Inventory system
- At least 3 items to collect and use
- Puzzle elements requiring items
- Win and lose conditions
- Save/load game state

Technical Requirements:
- Object-oriented design (classes for Room, Item, Player)
- File I/O for save system
- Error handling
- Comprehensive documentation

Deliverables:
- Source code (properly commented)
- UML class diagram
- Written design document (2-3 pages)
- 5-minute presentation

Grading:
- Functionality: 40%
- Code quality: 25%
- Documentation: 20%
- Presentation: 15%

Timeline: 3 weeks, check-ins each Friday
```

**Step 2 - Select Resource Room Group**
Group includes students with:
- ADHD
- Dysgraphia
- Autism spectrum
- Anxiety disorder
- Processing speed challenges

**Step 3 - AI Suggestions Include:**
```
✓ Provide a complete class structure template with method stubs

✓ Break the project into weekly milestones:
  Week 1: Basic room navigation
  Week 2: Inventory and items
  Week 3: Puzzles, win/lose, save/load

✓ Create a detailed checklist breaking each requirement into subtasks

✓ Allow alternative to written design document:
  - Recorded video explanation, OR
  - Visual presentation with minimal text, OR
  - Interview-based assessment

✓ Provide UML diagram template to fill in (vs. creating from scratch)

✓ Allow pair programming with clearly defined roles

✓ Extend timeline to 4 weeks with weekly (vs. daily) work expectations

✓ Provide example code for save/load functionality as reference

✓ Allow presentation to be done one-on-one instead of to class

✓ Create optional "extension features" for advanced students vs.
  increasing core requirements

✓ Provide debugging guide with common errors and solutions
```

**Step 4 - Result:**
Complete project packet with:
- Scaffolded milestones
- Code templates
- Visual checklists
- Alternative assessment options
- Clear weekly goals
- Support resources
- Flexible presentation options

### Example 3: Quick Differentiation During Planning

**Scenario:** You just found a great coding challenge online but realize it needs modifications for your 3rd period inclusion class.

**Step 1 - Paste the Challenge:**
```
Code Golf Challenge: FizzBuzz Variations

Write the shortest possible code that prints:
- "Fizz" for multiples of 3
- "Buzz" for multiples of 5
- "FizzBuzz" for multiples of both
- The number otherwise
- For numbers 1-100

Bonus: Fewest characters wins!
```

**Step 2 - Select Period 3 Students**

**Step 3 - AI Suggestions:**
```
✓ Remove "code golf" competitive element—focus on correctness over brevity
✓ Provide pseudocode outline
✓ Break into steps: First get basic FizzBuzz working, then add variations
✓ Allow longer, readable code vs. shortest possible
✓ Provide test cases
✓ Allow use of helper functions and comments (don't count toward length)
```

**Result:** You get a modified version appropriate for students with disabilities without spending 30 minutes rewriting it yourself.

---

## Library & Reusing Materials

### Accessing Saved Lessons

1. From dashboard, click "View Library"
2. Browse your saved differentiated materials
3. Click "View" to see any lesson
4. Print or reference as needed

### When to Save Materials

**Save when:**
- You'll teach this unit again next semester/year
- Multiple periods need the same material
- You want to build a resource collection
- The differentiation was particularly effective

**Don't need to save:**
- One-time assignments
- Materials specific to students who've moved/graduated
- Draft attempts that didn't work well

### Organizing Your Library

**Use clear, descriptive titles:**
```
Good: "Unit 3 - Binary Search Lab (Extended Time + Visual Aids)"
Bad: "Lab 5 Modified"

Good: "Final Project - Text Game (Resource Room Group, Fall 2024)"
Bad: "Project Thing"
```

**Include date and students/groups in title when relevant**

---

## Tips & Troubleshooting

### The AI is Too Simplistic

**Problem:** Suggestions remove too much challenge

**Solutions:**
- Be more specific about maintaining rigor in your original material
- Note explicitly: "Maintain grade-level expectations"
- Deselect over-simplified suggestions
- In student profiles, emphasize strengths along with challenges

### Suggestions Don't Match Student Needs

**Problem:** AI suggests accommodations that don't fit

**Solutions:**
- Review student profiles—add more specific details
- Include information about what HAS worked for this student
- Note accommodations that should NOT be used
- Add context about the student's current skill level

### Generated Content is Too Long

**Problem:** Differentiated version is 3x longer than original

**Solutions:**
- This is often intentional (breaking down steps)
- Print and provide as multi-page handout
- Use digital format (Google Classroom) to avoid paper
- Ask AI to condense in a refinement round

### I Want to Modify the AI Output

**Problem:** Generated content is good but needs tweaks

**Solutions:**
- Copy output to Google Docs for editing
- Save the version, then manually modify your printed copies
- Print and annotate by hand
- Use output as inspiration for your own rewrite

### Session Was Accidentally Deleted

**Problem:** Clicked away and lost work

**Solutions:**
- Check "Active Sessions" on dashboard—may still be saved
- If not saved to library, it's unfortunately lost
- Save important work immediately to library
- Active sessions persist until you explicitly delete them

### Formatting Looks Wrong

**Problem:** Code blocks or formatting is weird

**Solutions:**
- Try printing—print view often fixes layout
- Copy to a word processor and reformat
- Check on mobile vs. desktop (different layouts)
- Report consistent issues for bug fixes

### AI Suggests Impossible Accommodations

**Problem:** "Allow student to use telepathy to communicate"

**Solutions:**
- AI isn't perfect—use your judgment
- Deselect unrealistic suggestions
- Focus on practical modifications
- Consider what inspired the weird suggestion—there may be a good idea underneath

### How Much Detail Should Student Profiles Have?

**Answer:** More is better, but focus on:
- Specific diagnoses relevant to CS work
- Concrete accommodation needs
- How the student learns best
- Communication/processing needs
- Technology accommodations

You don't need:
- Medical details unrelated to learning
- Private family information
- Unrelated accommodations (like "sits near door for quick exit")

### Can I Use This for Non-CS Classes?

**Answer:** The tool is optimized for computer science curriculum, but you can:
- Try it with related STEM content
- Use for general technology lessons
- Experiment, but expect varying quality
- Best results come from programming/CS assignments

### How Do I Replace the Sample Curriculum?

**Answer:** Replace the `Intro_CS.md` file in the repository with your actual curriculum standards. The AI will automatically reference it in all suggestions.

**Format tips:**
- Use markdown formatting
- Include clear unit titles
- List learning objectives
- Note any differentiation guidance
- Specify assessment standards

---

## Need Help?

### Technical Issues
- Check with your system administrator
- Verify your Gemini API key is valid
- Try logging out and back in
- Clear browser cache

### Pedagogical Questions
- Use your professional judgment
- Consult with special education staff
- Review student IEP/504 plans
- Consider your classroom context

### Feature Requests or Bugs
- Contact the tool administrator
- Document the specific issue
- Include screenshots if relevant
- Note what you expected vs. what happened

---

## Quick Start Checklist

Your first week with DiffTool:

**Day 1:**
- [ ] Create account and wait for activation
- [ ] Log in once activated
- [ ] Explore the dashboard

**Day 2:**
- [ ] Add 2-3 student profiles (start with students you know well)
- [ ] Make profiles detailed and complete

**Day 3:**
- [ ] Create your first group (start with one class period)

**Day 4:**
- [ ] Run your first differentiation with a simple assignment
- [ ] Go through all 4 phases
- [ ] Save the result to your library

**Day 5:**
- [ ] Try a more complex differentiation
- [ ] Experiment with selecting/deselecting suggestions
- [ ] Print and use in your classroom

**Week 2 and beyond:**
- Add remaining students and groups
- Build your library of differentiated materials
- Refine student profiles as you learn what works
- Integrate into your regular lesson planning workflow

---

## Remember

**DiffTool is a teaching assistant, not a replacement for your expertise.**

- The AI generates suggestions based on best practices and your input
- YOU decide which accommodations are appropriate
- YOU know your students, classroom, and context best
- Use the tool to save time and get ideas, then apply your professional judgment

**Your feedback makes the tool better:**
- Note what works well
- Report what doesn't
- Share suggestions for improvement
- Help train the AI by using it consistently

**Happy differentiating!**
