# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design focused on the main actions the system needed to support for PawPal+. The design was centered around storing pet and owner information, managing care tasks, and generating a daily care schedule.

The system was designed to support three core user actions:
- The user should be able to enter and manage basic owner and pet information.
- The user should be able to add and edit pet care tasks, including duration and priority.
- The user should be able to generate and view a daily care plan based on constraints and priorities.


- What classes did you include, and what responsibilities did you assign to each?
The main classes in the initial design were Owner, Pet, Task, and Scheduler.

Owner stored the owner's name, available time, and preferences. Its responsibility was to manage owner-related information and constraints.
Pet stored details such as the pet's name, type, age, and care notes. Its responsibility was to represent the pet and its basic care needs.
Task stored task information such as task name, duration, priority, and category. Its responsibility was to represent individual care activities like feeding, walks, medication, or grooming.
Scheduler stored the list of tasks, available time, and the generated daily plan. Its responsibility was to organize tasks, apply constraints and priorities, and create the daily care schedule.
The main classes in the initial design were Owner, Pet, Task, and Scheduler.

- Owner stored the owner's name, available time, and preferences. Its responsibility was to manage owner-related information and constraints.
  Methods: update_preferences(), set_available_time()

- Pet stored details such as the pet's name, type, age, and care notes. Its responsibility was to represent the pet and its basic care needs.
  Methods: update_pet_info()

- Task stored task information such as task name, duration, priority, and category. Its responsibility was to represent individual care activities like feeding, walks, medication, or grooming.
  Methods: edit_task(), mark_complete()

- Scheduler stored the list of tasks, available time, and the generated daily plan. Its responsibility was to organize tasks, apply constraints and priorities, and create the daily care schedule.
  Methods: add_task(), generate_plan(), explain_plan()
  

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
