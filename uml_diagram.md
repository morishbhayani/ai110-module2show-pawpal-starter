```mermaid
classDiagram
    class Owner {
        owner_name
        available_time
        preferences
        update_preferences()
        set_available_time()
    }

    class Pet {
        pet_name
        pet_type
        age
        care_notes
        update_pet_info()
    }

    class Task {
        task_name
        duration
        priority
        category
        completed
        edit_task()
        mark_complete()
    }

    class Scheduler {
        task_list
        available_time
        daily_plan
        add_task()
        generate_plan()
        explain_plan()
    }

    Owner --> Pet : has
    Pet --> Task : needs
    Scheduler --> Task : organizes
    Scheduler --> Owner : uses constraints from
    Scheduler --> Pet : creates plan for