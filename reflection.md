# PawPal+ Project Reflection

## 1. System Design

### a. Initial design

The initial UML design focused on the core functionality required for PawPal+. The system was designed to manage pet care tasks and generate a daily schedule based on constraints.

The design supported three main user actions:
- The user can enter and manage owner and pet information.
- The user can add and manage pet care tasks with priority, duration, and frequency.
- The user can generate a daily care schedule based on constraints.

The main classes were Owner, Pet, Task, and Scheduler.

Owner stores the owner's name, available time, and preferences. Its role is to manage system-level constraints. Methods: update_preferences(), set_available_time()

Pet stores pet details such as name, type, age, and care notes. It also maintains a list of tasks associated with the pet. Methods: update_pet_info(), add_task(), get_incomplete_tasks()

Task represents individual care activities such as feeding, walking, or medication. It stores duration, priority, frequency, time, due date, and completion status. Methods: mark_complete(), mark_incomplete(), update_task()

Scheduler is responsible for organizing tasks, applying constraints, detecting conflicts, and generating the daily plan. Methods: sort_by_time(), filter_by_status(), filter_by_pet_name(), detect_conflicts(), mark_task_complete(), generate_plan(), explain_plan()


### b. Design changes

The design evolved during implementation.

Initially, tasks were treated as simple objects, but later additional attributes such as time, due_date, frequency, and pet_name were added to support scheduling logic and recurrence.

The Scheduler class also expanded significantly. It originally only generated a plan, but later included sorting, filtering, recurrence handling, and conflict detection. This change was necessary to support more realistic scheduling behavior.

The relationship between classes also became clearer, with Owner managing multiple pets, and each pet managing multiple tasks.

---

## 2. Scheduling Logic and Tradeoffs

### a. Constraints and priorities

The scheduler considers the following constraints:
- Available time of the owner
- Task priority (higher priority tasks are selected first)
- Task time for ordering
- Task due date (only tasks due today are considered)

Priority was given the highest importance because it directly reflects urgency. Time was used as a secondary factor to organize tasks within the schedule.

### b. Tradeoffs

One key tradeoff is that conflict detection only checks for exact time matches instead of overlapping durations.

This simplifies the logic and keeps the system easy to understand and implement. While it does not handle complex scheduling conflicts, it is reasonable for this scenario where tasks are relatively short and discrete.

Another tradeoff is that scheduling is greedy. The system selects tasks based on priority until available time is exhausted, rather than optimizing globally.

---

## 3. AI Collaboration

### a. How you used AI

AI tools such as VS Code Copilot were used throughout the project for:
- Generating initial class structures and method templates
- Writing test cases
- Suggesting refactoring for cleaner code
- Helping debug errors and align tests with updated code

Prompts that were most useful were specific and targeted, such as:
- "Write tests for sorting and conflict detection"
- "How can this function be simplified"
- "What edge cases should I test"

Using precise prompts helped get more relevant and usable suggestions.

### b. Judgment and verification

One example of rejecting an AI suggestion was related to simplifying the conflict detection logic. Copilot suggested a more compact implementation using grouping techniques, but that version reduced readability.

The simpler nested loop version was kept because it was easier to understand, debug, and explain.

All AI suggestions were verified by:
- Running the code and checking outputs
- Running pytest to validate behavior
- Manually reviewing logic to ensure correctness

---

## 4. Testing and Verification

### a. What you tested

The main behaviors that were tested were:
- Task completion
- Task addition
- Time-based sorting
- Recurring task creation
- Conflict detection

The scheduler was also tested against edge cases such as:
- Pets with no tasks
- Owners with no pets
- Tasks scheduled at the same time
- Already completed tasks
- Tasks exceeding available time

These tests were important because they ensured both normal functionality and boundary conditions were handled correctly.

### b. Confidence

Confidence Level: ★★★★☆ (4/5)

The system performs reliably for the tested scenarios, including core scheduling behavior and edge cases.

If more time were available, additional testing would include:
- Overlapping task durations
- Invalid time formats
- Large-scale task lists
- More complex recurrence patterns

---

## 5. Reflection

### a. What went well

The most successful part of the project was building the Scheduler class. It integrates multiple features such as sorting, filtering, recurrence, and conflict detection into a cohesive system.

The transition from a simple backend to a more intelligent scheduling system worked well.

### b. What you would improve

If another iteration were done, the system would be improved by:
- Supporting overlapping time conflict detection
- Adding better input validation for time formats
- Improving the scheduling algorithm to optimize task selection
- Enhancing the UI for better user experience and clarity

### c. Key takeaway

One important takeaway from this project is the role of the developer as the "lead architect" when working with AI tools.

AI can generate code quickly, but it does not fully understand system design or tradeoffs. It is important to guide the AI, validate its outputs, and make decisions based on clarity, maintainability, and correctness.

Using separate chat sessions for different phases helped maintain focus and avoid mixing concerns, making the development process more structured and organized.