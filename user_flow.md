### **The "Material-First" Workflow**

This flow is for when a teacher has a new lesson and wants to adapt it for multiple students or groups simultaneously.

1. **Login & Dashboard:** The teacher logs in.  
2. **Initiate Differentiation:** From the main dashboard, the teacher clicks "Differentiate a New Lesson."  
3. **Phase 1 (Analyze):** The teacher pastes in the original assignment (e.g., "OOP Project: Design a 'Pet' class").  
4. **Select Students/Groups:** *Before* generating suggestions, the app asks, "Who is this for?" The teacher sees their student list and can select:  
   * Individual students: "Jane D." and "Mike K."  
   * A saved group: "504 Accommodations Group" (which includes 4 students).  
5. **Phase 2 (Suggest):** The Gemini API analyzes the material and *all selected student profiles* at once. It generates a single, consolidated list of suggestions, noting which student(s) each suggestion applies to.  
   * "Provide a code template for the class constructor. \[Applies to: Jane D., 504 Group\]"  
   * "Add a glossary of terms (e.g., 'class', 'object', 'method'). \[Applies to: Mike K.\]"  
   * "Chunk the project into 3 smaller, distinct milestones. \[Applies to: Jane D.\]"  
6. **Phase 3 (Refine):** The teacher reviews the consolidated list. They like all the suggestions and click "Approve All."  
7. **Phase 4 (Generate):** The teacher clicks "Generate." The tool creates *one* "master" differentiated document that incorporates all the approved modifications. (An advanced version might generate separate files, but for an MVP, one consolidated file is simpler).  
8. **Review & Save:** The teacher reviews the new document, which now has the glossary, the code template, and the milestones. They save it to their "Lesson Library."

