# Notes:
# 1. Use the following username and password to access the admin rights
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the
# program will look in your root directory for the text files.

# =====importing libraries===========
import os
from datetime import date, datetime

DATETIME_STRING_FORMAT = "%Y-%m-%d"
MENU_LINES = "=" * 40

# =====Creat files in case of error===========





# If no task_overview.txt file, write one with a default account
if not os.path.exists("task_overview.txt"):
    with open("task_overview.txt", "w") as default_file:
        pass
# If no user_overview.txt file, write one with a default account
if not os.path.exists("user_overview.txt"):
    with open("user_overview.txt", "w") as default_file:
        pass


# =====Functions for program logic===========
# ---- Function to register new users
def reg_user():
    """Registers new users in the database"""
    # --- initiate loop to verfiy username is available
    while True:
        new_username = input("New Username: ").lower()
        if check_user_name(new_username):
            print("user already exists")
            break

    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    """Add a new user to the user.txt file"""

    # ---- Verify passwords match
    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print(f"\n{MENU_LINES}\n New user added \n{MENU_LINES}\n")
        username_password[new_username] = new_password
        # --- Open and write user data to file
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))
    # ---- Otherwise you present a relevant message.
    else:
        print(f"\n{MENU_LINES}\n Passwords do no match \n{MENU_LINES}\n")


def check_user_name(new_username):
    """Checks through tasks.txt to see if the user name is available"""
    with open("user.txt", "r+") as check_user:
        data = check_user.read()
        # strips data and sorts into lists
        clean_data = [i.strip().split(";") for i in data.split("\n")]

    # ---- loop through lists and verifies 0-index against user input
    user_exists = False  # create a boolean logic to test
    for i in clean_data:
        if i[0].lower() == new_username.lower():
            user_exists = True

    if user_exists:
        return
    else:
        # breaks loop if username is available
        return False


def add_task():
    """Allow a user to add a new task to task.txt file
    Prompt a user for the following:
     - A username of the person whom the task is assigned to,
     - A title of a task,
     - A description of the task and
     - the due date of the task."""

    while True:
        task_username = input("Name of person assigned to task: ").lower()
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
                break

            except ValueError:
                print("Invalid datetime format. Please use the format specified")

        # Then get the current date.
        curr_date = date.today()
        """ Add the data to the file task.txt and
                    Include 'No' to indicate if the task is complete."""
        new_task = {
            "username": task_username,
            "title": task_title,
            "description": task_description,
            "due_date": due_date_time,
            "assigned_date": curr_date,
            "completed": False,
        }

        task_list.append(new_task)
        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t["username"],
                    t["title"],
                    t["description"],
                    t["due_date"].strftime(DATETIME_STRING_FORMAT),
                    t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t["completed"] else "No",
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
        print("Task successfully added.")
        break


def view_all():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """

    for j, t in enumerate(task_list, start=1):
        disp_str = f"{j}.Task: \t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n".title()
        disp_str += (
            f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        )
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task completed: {'Yes' if t['completed'] else 'No' }\n"
        print(disp_str)


def task_editor(user_tasks):
    """Takes user input and allows them to update any task allocated by either
    * Due date
    * Re-assign user
    * Mark as complete

    Data is then returned to tasks.txt
    """
    try:
        select_task = int(input("Select which task you would like to update: "))

        if select_task == -1:
            return  # This will exit the function and return to menu

        if select_task >= 1 and select_task <= len(
            user_tasks
        ):  # checks user selection is valid
            selected_task = user_tasks[select_task - 1]
            if selected_task["completed"]:
                print("\nThis task is marked as complete and can no longer be edited.")
            else:
                edit_task = input(
                    """Select from the following:
            an - Assign New user
            dd - New due date
            c  - mark as complete
            """
                )
                if edit_task == "an":
                    new_user = input(
                        "Please enter the name of the user you would like to assign this task to: "
                    ).lower()
                    if check_user_name(new_user):  # function return False
                        print(f"\n{new_user} does not exist")
                    else:
                        selected_task["username"] = new_user
                        print(f"\nTask has been allocated to {new_user}")

                elif edit_task == "dd":
                    new_due_date = input("Enter the new due date (YYYY-MM-DD): ")
                    try:
                        due_date_time = datetime.strptime(
                            new_due_date, DATETIME_STRING_FORMAT
                        )
                        selected_task["due_date"] = due_date_time
                        print("Due date updated.")
                    except ValueError:
                        print(
                            "Invalid datetime format. Please use the format specified."
                        )
                elif edit_task == "c":
                    selected_task["completed"] = True
                    print("\nThis task has been marked as complete.")

                else:
                    print("Invalid option. Please choose a valid option from the list")
        else:
            print("Invalid task number. Please enter a valid task number.")

        with open("tasks.txt", "w") as task_file:
            task_list_to_write = []
            for t in task_list:
                str_attrs = [
                    t["username"],
                    t["title"],
                    t["description"],
                    t["due_date"].strftime(DATETIME_STRING_FORMAT),
                    t["assigned_date"].strftime(DATETIME_STRING_FORMAT),
                    "Yes" if t["completed"] else "No",
                ]
                task_list_to_write.append(";".join(str_attrs))
            task_file.write("\n".join(task_list_to_write))
            print("\nYour task list has been updated.")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def view_mine():
    """Reads the task from task.txt file and prints to the console in the
    format of Output 2 presented in the task pdf (i.e. includes spacing
    and labelling)
    """

    j = 1  # Create numbers for tasks
    # if current_user in task_list:
    user_tasks = [t for t in task_list if t.get("username") == current_user]
    for t in user_tasks:
        disp_str = f"\n{j}.Task: \t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += (
            f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        )
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task completed: {'Yes' if t['completed'] else 'No' }\n"
        print(disp_str)

        j += 1  # Increases task index display
    task_editor(user_tasks)
    # else:
    #     print("Something is wrong")


def task_report():
    """Reads data from tasks and returns and stores them in task_overview.txt
    data is then printed when admin calls "generate reports"
    """
    if not os.path.exists("task_overview.txt"):
        with open("task_overview.txt", "w+") as default_file:
            pass

    with open("task_overview.txt", "w+") as overview_file:
        overview_file.write(f"Total number over tasks: {len(task_list)}\n")
        # create new list from task_list with key values
        completed_tasks = [task for task in task_list if task["completed"]]
        overview_file.write(f"Total number over tasks: {len(completed_tasks)}\n")

        incomplete_tasks = [task for task in task_list if not task["completed"]]
        overview_file.write(f"Total number over tasks: {len(incomplete_tasks)}\n")

        # check current date in datetime object
        current_date = datetime.today()
        # creat list and compare current date vs due date
        overdue_tasks = [
            task
            for task in task_list
            if not task["completed"] and task["due_date"] < current_date
        ]
        overview_file.write(f"Total number of over due tasks: {len(overdue_tasks)}\n")

        # Calculate % of incomplete tasks
        overview_file.write(
            f"Percentage of incompete tasks: {(len(incomplete_tasks))/(len(task_list)) * 100:.2f}\n"
        )
        overview_file.write(
            f"Percentage of overdue tasks: {(len(overdue_tasks))/(len(task_list)) * 100:.2f}\n"
        )
        overview_file.seek(0)
        data = overview_file.read()
        print(data)


def user_report():
    """Reads task data and and generates performance data for the following
    * Total number of users
    * Total tasks
    * Total tasks allocated to each user
    * % of tasks allocated to each user
    * Number of completed tasks for each user
    * number of incompelte tasks per user
    * number of incomplete and overdue tasks per user

    Data will be printed when admin calls 'uo' from the generate reports menu
    """
    with open("user_overview.txt", "w") as user_overview_file:
        total_users = len(
            username_password.keys()
        )  # Get total num of users stored in dict

        current_date = datetime.today()

        task_count = {}
        for task in task_list:
            username = task["username"]
            task_count[username] = task_count.get(username, 0) + 1

        for username, count in task_count.items():
            completed_tasks = sum(
                True
                for task in task_list
                if task["username"] == username and task["completed"]
            )
            incomplete_tasks = sum(
                True
                for task in task_list
                if task["username"] == username and not task["completed"]
            )
            incomplete_overdue = sum(
                True
                for task in task_list
                if task["username"] == username
                and not task["completed"]
                and task["due_date"] < current_date
            )
            total_num_users = f"Total users registered: {total_users}\n"
            total_tasks = f"Total number of tasks: {len(task_list)}\n"
            task_per_user = f"Total tasks assigned to {username.title()}: {count}\n"
            task_per_user_per = f"Percentage of tasks assigned to {username.title()}: {count/len(task_list)*100:.2f}%\n"
            task_per_user_complete = f"Number of tasks assigned to {username.title()} completed: {completed_tasks}\n"
            task_per_user_incomplete = f"Percentage of tasks assigned to {username.title()} incomplete: {incomplete_tasks/count*100:.2f}%\n"
            incomplete_overdue = f"Percentage of tasks assigned to {username.title()} incomplete and overdue: {incomplete_overdue/count*100:.2f}%\n\n"

            user_overview_file.write(total_num_users)
            user_overview_file.write(total_tasks)
            user_overview_file.write(task_per_user)
            user_overview_file.write(task_per_user_per)
            user_overview_file.write(task_per_user_complete)
            user_overview_file.write(task_per_user_incomplete)
            user_overview_file.write(incomplete_overdue)
        user_overview_file.seek(0)
        file_data = user_overview_file.read()
        print(file_data)


def user_stats():
    # If no user.txt file, write one with a default account
    if not os.path.exists("user.txt"):
        with open("user.txt", "w") as default_file:
            default_file.write("admin;password")

    with open("user.txt", "r") as fd:
        user_data = fd.readlines()

    total_users = len(user_data)

    return total_users


def task_stats():
    # Create tasks.txt if it doesn't exist
    if not os.path.exists("tasks.txt"):
        with open("tasks.txt", "w") as default_file:
            pass
    with open("tasks.txt", "r") as task_file:
        tasks_data = task_file.readlines()

    total_tasks = len(tasks_data)

    return total_tasks


with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for task_str in task_data:
    current_task = {}

    # Split by semicolon and manually add each component
    task_components = task_str.split(";")
    current_task["username"] = task_components[0]
    current_task["title"] = task_components[1]
    current_task["description"] = task_components[2]
    current_task["due_date"] = datetime.strptime(
        task_components[3], DATETIME_STRING_FORMAT
    )
    current_task["assigned_date"] = datetime.strptime(
        task_components[4], DATETIME_STRING_FORMAT
    )
    current_task["completed"] = True if task_components[5] == "Yes" else False

    task_list.append(current_task)


# Read in user_data
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password


# ====Login Section====
"""This code reads usernames and password from the user.txt file to 
allow a user to login.
"""
logged_in = False
while not logged_in:
    print("LOGIN")
    current_user = input("Username: ")
    current_password = input("Password: ")
    if current_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[current_user] != current_password:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input(
        """Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - generate reports
ds - Display statistics
t - task list
e - Exit
: """
    ).lower()

    if menu == "r":
        reg_user()

    elif menu == "a":
        add_task()

    elif menu == "va":
        view_all()

    elif menu == "vm":
        view_mine()

    elif menu == "gr" and current_user == "admin":
        report = input(
            """Which reports would you like to view?
        to - Overview of all tasks assinged to team
        uo - Current state of tasks assigned to the team
        :"""
        )
        if report.lower() == "to":
            task_report()
        elif report.lower() == "uo":
            user_report()
        elif report == "-1":
            continue
        else:
            print("Please choose a valid function")
    elif menu == "ds" and current_user == "admin":
        """If the user is an admin they can display statistics about number of users
        and tasks."""

        print(MENU_LINES)
        print(f"Number of users: \t\t {user_stats()}")
        print(f"Number of tasks: \t\t {task_stats()}")
        print(MENU_LINES)

    elif menu == "t":
        print(task_list)
    elif menu == "e":
        print("Goodbye!!!")
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
