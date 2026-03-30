import streamlit as st
from datetime import date
from pawpal_system import Owner, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

if "owner" not in st.session_state:
    st.session_state.owner = Owner(
        owner_name="",
        available_time=60,
        preferences=[]
    )

st.title("🐾 PawPal+")

st.markdown(
    """
Welcome to PawPal+.

This app connects the Streamlit UI to the backend scheduling logic. You can add pets,
assign tasks, generate a schedule, and view conflict warnings.
"""
)

with st.expander("Scenario", expanded=True):
    st.markdown(
        """
**PawPal+** is a pet care planning assistant. It helps a pet owner plan care tasks
for their pet(s) based on constraints like time, priority, and preferences.

The app stores pets and tasks in session state and uses the backend classes to
sort tasks, filter tasks, detect conflicts, and generate a daily plan.
"""
    )

st.subheader("Owner Information")

owner_name_input = st.text_input(
    "Owner Name",
    value=st.session_state.owner.owner_name
)

available_time_input = st.number_input(
    "Available Time Today (minutes)",
    min_value=0,
    max_value=600,
    value=st.session_state.owner.available_time
)

if st.button("Save Owner Info"):
    st.session_state.owner.owner_name = owner_name_input
    st.session_state.owner.set_available_time(int(available_time_input))
    st.success("Owner information updated!")

st.divider()

st.subheader("Add a New Pet")

with st.form("add_pet_form"):
    pet_name = st.text_input("Pet Name")
    pet_type = st.text_input("Pet Type")
    pet_age = st.number_input("Pet Age", min_value=0, step=1)
    care_notes = st.text_area("Care Notes")

    submitted = st.form_submit_button("Add Pet")

    if submitted:
        if pet_name.strip() and pet_type.strip():
            new_pet = Pet(
                pet_name=pet_name,
                pet_type=pet_type,
                age=int(pet_age),
                care_notes=care_notes
            )
            st.session_state.owner.add_pet(new_pet)
            st.success(f"{pet_name} added successfully!")
        else:
            st.error("Please enter both pet name and pet type.")

st.subheader("Your Pets")

if st.session_state.owner.pets:
    pet_rows = []
    for pet in st.session_state.owner.pets:
        pet_rows.append(
            {
                "Pet Name": pet.pet_name,
                "Type": pet.pet_type,
                "Age": pet.age,
                "Notes": pet.care_notes,
                "Task Count": len(pet.tasks),
            }
        )
    st.table(pet_rows)
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")

if st.session_state.owner.pets:
    pet_names = [pet.pet_name for pet in st.session_state.owner.pets]
    selected_pet_name = st.selectbox("Select a Pet", pet_names)

    selected_pet = next(
        pet for pet in st.session_state.owner.pets
        if pet.pet_name == selected_pet_name
    )

    with st.form("add_task_form"):
        task_description = st.text_input("Task Description")
        task_duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority_label = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        task_frequency = st.selectbox("Frequency", ["none", "daily", "weekly"], index=1)
        task_time = st.text_input("Task Time (HH:MM)", value="08:00")
        task_due_date = st.date_input("Due Date", value=date.today())

        task_submitted = st.form_submit_button("Add Task")

        if task_submitted:
            if task_description.strip():
                priority_map = {"low": 1, "medium": 2, "high": 3}

                new_task = Task(
                    description=task_description,
                    duration=int(task_duration),
                    priority=priority_map[priority_label],
                    frequency=task_frequency,
                    time=task_time,
                    due_date=task_due_date
                )
                selected_pet.add_task(new_task)
                st.success(f"Task added to {selected_pet.pet_name}!")
            else:
                st.error("Please enter a task description.")

    st.markdown(f"### Tasks for {selected_pet.pet_name}")
    if selected_pet.tasks:
        task_rows = []
        for task in selected_pet.tasks:
            task_rows.append(
                {
                    "Task": task.description,
                    "Time": task.time,
                    "Due Date": str(task.due_date),
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Completed" if task.completed else "Incomplete",
                }
            )
        st.table(task_rows)
    else:
        st.info(f"No tasks yet for {selected_pet.pet_name}.")
else:
    st.info("Add a pet first before adding tasks.")

st.divider()

st.subheader("Task Filters")

if st.session_state.owner.pets:
    scheduler = Scheduler(st.session_state.owner)
    all_tasks = []
    for pet in st.session_state.owner.pets:
        all_tasks.extend(pet.tasks)

    filter_pet = st.selectbox("Filter by Pet", ["All Pets"] + [pet.pet_name for pet in st.session_state.owner.pets])
    filter_status = st.selectbox("Filter by Status", ["All", "Incomplete", "Completed"])

    filtered_tasks = all_tasks

    if filter_pet != "All Pets":
        filtered_tasks = scheduler.filter_by_pet_name(filtered_tasks, filter_pet)

    if filter_status == "Incomplete":
        filtered_tasks = scheduler.filter_by_status(filtered_tasks, False)
    elif filter_status == "Completed":
        filtered_tasks = scheduler.filter_by_status(filtered_tasks, True)

    if filtered_tasks:
        filtered_rows = []
        for task in scheduler.sort_by_time(filtered_tasks):
            filtered_rows.append(
                {
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Time": task.time,
                    "Due Date": str(task.due_date),
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Completed" if task.completed else "Incomplete",
                }
            )
        st.table(filtered_rows)
    else:
        st.info("No tasks match the selected filters.")

st.divider()

st.subheader("Mark a Task Complete")

if st.session_state.owner.pets:
    pet_options = [pet.pet_name for pet in st.session_state.owner.pets]
    completion_pet_name = st.selectbox("Choose Pet", pet_options, key="completion_pet")

    completion_pet = next(
        pet for pet in st.session_state.owner.pets
        if pet.pet_name == completion_pet_name
    )

    incomplete_pet_tasks = [task for task in completion_pet.tasks if not task.completed]

    if incomplete_pet_tasks:
        completion_task_label = st.selectbox(
            "Choose Task",
            [task.description for task in incomplete_pet_tasks],
            key="completion_task"
        )

        if st.button("Mark Task Complete"):
            scheduler = Scheduler(st.session_state.owner)
            new_task = scheduler.mark_task_complete(completion_pet_name, completion_task_label)

            completed_task = next(
                (task for task in completion_pet.tasks if task.description == completion_task_label and task.completed),
                None
            )

            if completed_task:
                st.success(f"Marked '{completion_task_label}' as complete for {completion_pet_name}.")

            if new_task:
                st.info(
                    f"Recurring task created: '{new_task.description}' is now scheduled for "
                    f"{new_task.due_date} at {new_task.time}."
                )
    else:
        st.info(f"No incomplete tasks available for {completion_pet_name}.")

st.divider()

st.subheader("Build Schedule")
st.caption("Generate a daily care schedule using backend sorting and conflict detection.")

if st.button("Generate Schedule"):
    scheduler = Scheduler(st.session_state.owner)

    due_today_tasks = scheduler.get_due_today_tasks()
    sorted_tasks = scheduler.sort_by_time(due_today_tasks)
    conflicts = scheduler.detect_conflicts(sorted_tasks)
    plan = scheduler.generate_plan()

    if conflicts:
        for warning in conflicts:
            st.warning(warning)

    if sorted_tasks:
        st.markdown("### Tasks Due Today (Sorted by Time)")
        due_rows = []
        for task in sorted_tasks:
            due_rows.append(
                {
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Time": task.time,
                    "Due Date": str(task.due_date),
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Frequency": task.frequency,
                    "Status": "Completed" if task.completed else "Incomplete",
                }
            )
        st.table(due_rows)
    else:
        st.info("No tasks are due today.")

    if plan:
        st.success("Today's Schedule")
        plan_rows = []
        for task in plan:
            plan_rows.append(
                {
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Time": task.time,
                    "Duration": task.duration,
                    "Priority": task.priority,
                    "Due Date": str(task.due_date),
                }
            )
        st.table(plan_rows)
        st.info(scheduler.explain_plan())
    else:
        st.warning("No tasks could be scheduled for today.")

st.divider()

with st.expander("What you need to build", expanded=False):
    st.markdown(
        """
At minimum, the system should:
- Represent pet care tasks with time, priority, due date, and completion state
- Represent the pet and the owner with useful details
- Build a daily plan based on constraints like available time
- Explain why the selected tasks were added to the final schedule
- Detect simple scheduling conflicts and warn the user
"""
    )