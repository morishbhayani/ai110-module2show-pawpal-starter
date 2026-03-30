# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
## Testing PawPal+

Run the automated test suite with:

```bash
python -m pytest

## Features

- Add and manage multiple pets for one owner
- Add pet care tasks with priority, time, frequency, and due date
- Sort tasks by time in chronological HH:MM order
- Filter tasks by pet name
- Filter tasks by completion status
- Generate a daily schedule based on priority, task time, due date, and available owner time
- Automatically create the next instance of daily and weekly recurring tasks
- Detect task conflicts when two tasks are scheduled at the same time
- Show schedule explanations and conflict warnings in the Streamlit UI

## 📸 Demo

<a href="/course_images/ai110/your_screenshot_name.png" target="_blank"><img src='/course_images/ai110/your_screenshot_name.png' title='PawPal App' width='' alt='PawPal App' class='center-block' /></a>