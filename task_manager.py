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


# =====Functions for program logic===========


def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def create_task_list(task_data):
    """
    The function `create_task_list` takes a list of task data strings and
    converts them into a list of dictionaries representing tasks.

    :param task_data: The `task_data` parameter is a list of strings,
    where each string represents task data
    :return: a list of dictionaries, where each dictionary represents a task.
    """
    task_list = []
    for task_str in task_data:
        curr_task = {}

        # Split by semicolon and manually add each component
        task_components = task_str.split(";")
        curr_task["username"] = task_components[0]
        curr_task["title"] = task_components[1]
        curr_task["description"] = task_components[2]
        curr_task["due_date"] = datetime.strptime(
            task_components[3], DATETIME_STRING_FORMAT
        )
        curr_task["assigned_date"] = datetime.strptime(
            task_components[4], DATETIME_STRING_FORMAT
        )
        curr_task["completed"] = True if task_components[5] == "Yes" else False

        task_list.append(curr_task)

    return task_list


def create_user_data_dict(user_data):
    """
    The function `create_user_data_dict` takes a list of user data in the
    format "username;password" and returns a dictionary where the usernames
    are the keys and the passwords are the values.

    :param user_data: A list of strings where each string represents user data
    in the format "username;password"
    :return: a dictionary where the keys are usernames and the values are
    passwords.
    """
    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    return username_password


def reg_user():
    """
    The `reg_user()` function prompts the user to enter a new username and
    password, checks if the username already exists, and adds the new user
    to a file if the passwords match.
    """
    while True:
        new_username = input("\nNew Username: ")
        if check_user_name(new_username):
            print("\nUser name already exists")
        else:
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


def check_user_name(username):
    """
    The function `check_user_name` checks if a given username is available by
    searching through a file
    called "user.txt" and returning `False` if the username is not found.

    :param new_username: The new_username parameter is a string that represents
    the username that needs to be checked for availability
    :return: `None` if the user name already exists in the `user.txt` file,
    and it is returning `False`
    if the user name is available.
    """
    """Checks through tasks.txt to see if the user name is available"""
    with open("user.txt", "r+") as check_user:
        data = check_user.read()
        # strips data and sorts into lists
        clean_data = [i.strip().split(";") for i in data.split("\n")]

    # ---- loop through lists and verifies 0-index against user input
    user_exits = False
    for i in clean_data:
        if i[0].lower() == username.lower():
            user_exits = True

    if user_exits:
        return True
    else:
        return False


def add_task():
    """The `add_task()` function allows a user to add a new task to a
    task.txt file by prompting for the following:
     - A username of the person whom the task is assigned to,
     - A title of a task,
     - A description of the task and
     - the due date of the task."""

    while True:
        task_username = input("Name of person assigned to task: ")
        if task_username not in username_password.keys():
            print("User does not exist. Please enter a valid username")
            continue
        task_title = input("Title of Task: ")
        task_description = input("Description of Task: ")
        while True:
            try:
                task_due_date = input("Due date of task (YYYY-MM-DD): ")
                due_date_time = datetime.strptime(
                    task_due_date, DATETIME_STRING_FORMAT
                    )
                break

            except ValueError:
                print(
                    "Invalid datetime format. Please use the format specified"
                    )

        # Gets the current date.
        curr_date = date.today()
        # Adds the data to the file task.txt and
        # includes 'No' to indicate if the task is complete.
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
        print("\n>>>Task successfully added<<<")
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
        disp_str += f"Task completed: {'Yes' if t['completed'] else 'No'}\n"
        print(disp_str)


def task_editor(user_tasks):
    """
    The `task_editor` function allows the user to update tasks and then saves
    the updated tasks to 'tasks.txt'.The following data can be updated by the
     user:
    * due date
    * re-assigning the user
    * mark task as complete

    :param user_tasks: user_tasks is a list of dictionaries representing
    tasks. Each dictionary contains the following keys:
    """
    try:
        select_task = int(
            input(
                "Select which task you would like to update or enter"
                + "'-1' to go back: "
            )
        )

        if select_task == -1:
            return  # This will exit the function and return to menu

        # checks user selection is valid
        if select_task >= 1 and select_task <= len(user_tasks):
            selected_task = user_tasks[select_task - 1]
            if selected_task["completed"]:
                print(
                    "\nThis task is marked as complete "
                    + "and can no longer be edited.")
            else:
                edit_task = input(
                    """Select from the following:\n
an - Assign New user
dd - New due date
c  - mark as complete\n
"""
                )
                if edit_task == "an":
                    new_user = input(
                        "\nPlease enter the name of the user you would like"
                        + "to assign this task to: "
                    ).lower()
                    if not check_user_name(
                        new_user
                    ):  # function return False if user does not exist
                        print(f"\n{new_user} does not exist")
                    else:
                        selected_task["username"] = new_user
                        print(
                            f"\n{MENU_LINES}\nTask has been allocated to "
                            + f"{new_user}\n{MENU_LINES}\n"
                        )

                elif edit_task == "dd":
                    new_due_date = input(
                        "\nEnter the new due date (YYYY-MM-DD): "
                        )
                    try:
                        due_date_time = datetime.strptime(
                            new_due_date, DATETIME_STRING_FORMAT
                        )
                        selected_task["due_date"] = due_date_time
                        print(f"\n{MENU_LINES}\nDue date updated.\n{MENU_LINES}\n")
                    except ValueError:
                        print(
                            "Invalid datetime format. Please use "
                            + "the format specified."
                        )
                elif edit_task == "c":
                    selected_task["completed"] = True
                    print(
                        f"\n{MENU_LINES}This task has been "
                        + f"marked as complete.\n{MENU_LINES}\n"
                    )

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
            print(f"\n{MENU_LINES}\nYour task list has been updated.\n{MENU_LINES}\n")

    except ValueError:
        print("Invalid input. Please enter a valid number.")


def view_mine(current_user):
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
        disp_str += f"Task completed: {'Yes' if t['completed'] else 'No'}\n"
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
        with open("task_overview.txt", "w+") as overview_file:
            pass

    with open("task_overview.txt", "r+") as overview_file:
        overview_file.write(
            f"\n{MENU_LINES}\nTotal number of tasks: {len(task_list)}\n"
        )
        # Loops through task_list and extracts completed tasks
        completed_tasks = [task for task in task_list if task["completed"]]
        overview_file.write(
            f"Total number of completed tasks: {len(completed_tasks)}\n"
        )
        # Loops through task_list and extracts INcompleted tasks
        incomplete_tasks = [task for task in task_list if not task["completed"]]
        overview_file.write(
            f"Total number of incomplete tasks: {len(incomplete_tasks)}\n"
        )

        # check current date in datetime object
        current_date = datetime.today()

        # creat list and compare current date vs due date
        overdue_tasks = [
            task
            for task in task_list
            if not task["completed"] and task["due_date"] < current_date
        ]
        overview_file.write(
            "Total number of of incomplete and overdue"
            + f"due tasks: {len(overdue_tasks)}\n"
        )

        # Calculate % of incomplete tasks
        overview_file.write(
            "Percentage of incompete tasks: "
            + f"{(len(incomplete_tasks))/(len(task_list)) * 100:.2f}%\n"
        )
        overview_file.write(
            "Percentage of overdue tasks: "
            + f"{(len(overdue_tasks))/(len(task_list)) * 100:.2f}%\n{MENU_LINES}\n"
        )
        overview_file.seek(0)
        data = overview_file.read()
        print(data)


def user_report():
    """The `user_report` function reads task data and generates performance
    data for each user

    * Total number of users
    * Total tasks
    * Total tasks allocated to each user
    * % of tasks allocated to each user
    * Number of completed tasks for each user
    * number of incompelte tasks per user
    * number of incomplete and overdue tasks per user

    Data will be printed when admin calls 'uo' from the generate reports menu
    """
    with open("user_overview.txt", "r+") as user_overview_file:
        total_users = len(
            username_password.keys()
        )  # Get total num of users stored in dict

        current_date = datetime.today()

        task_count = {}
        for task in task_list:
            username = task["username"]
            task_count[username] = task_count.get(username, 0) + 1

        total_num_users = (
            f"\n{MENU_LINES}\nTotal users " + f"registered: {total_users}\n"
        )

        total_tasks = f"Total number of tasks: {len(task_list)}\n{MENU_LINES}\n"

        user_overview_file.write(total_num_users)
        user_overview_file.write(total_tasks)

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

            task_per_user = f"\nTotal tasks assigned to {username.title()}: {count}\n"

            task_per_user_per = (
                "Percentage of tasks assigned to "
                + f"{username.title()}: {count/len(task_list)*100:.2f}%\n"
            )

            task_per_user_complete = (
                "Percentage of tasks assigned to "
                + f"{username.title()} completed: "
                + f"{completed_tasks/count*100:.2f}%\n"
            )

            task_per_user_incomplete = (
                "Percentage of tasks assigned to"
                + f"{username.title()} incomplete: "
                + f"{incomplete_tasks/count*100:.2f}%\n"
            )

            incomplete_overdue = (
                "Percentage of tasks assigned to "
                + f"{username.title()} incomplete and overdue: "
                + f"{incomplete_overdue/count*100:.2f}%\n\n{MENU_LINES}\n"
            )

            user_overview_file.write(task_per_user)
            user_overview_file.write(task_per_user_per)
            user_overview_file.write(task_per_user_complete)
            user_overview_file.write(task_per_user_incomplete)
            user_overview_file.write(incomplete_overdue)

        user_overview_file.seek(0)
        file_data = user_overview_file.read()
        print(file_data)


def user_stats():
    """
    The function `user_stats` reads data from a file called "user.txt" and
    returns the total number of
    users.
    :return: the total number of users stored in the "user.txt" file.
    """

    with open("user.txt", "r") as fd:
        user_data = fd.readlines()

    total_users = len(user_data)

    return total_users


def task_stats():
    """
    The function "task_stats" reads a file called "tasks.txt" and
    returns the total number of tasks listed in the file.
    :return: the total number of tasks in the "tasks.txt" file.
    """

    with open("tasks.txt", "r") as task_file:
        tasks_data = task_file.readlines()

    total_tasks = len(tasks_data)

    return total_tasks


# =====Creat files in case of error===========

# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

# If no task_overview.txt file, write one with a default account
if not os.path.exists("task_overview.txt"):
    with open("task_overview.txt", "w") as default_file:
        pass

# If no user_overview.txt file, write one with a default account
if not os.path.exists("user_overview.txt"):
    with open("user_overview.txt", "w") as default_file:
        pass

# Read in user_data
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

# calls function to create task list
task_list = create_task_list(task_data)
# calls function to create username_password dictionary
username_password = create_user_data_dict(user_data)


def log_in():
    """
    The function `log_in()` prompts the user to enter a username and
    password, checks if the user exists and if the password is correct,
    and grants admin rights if the user is the admin.
    """
    clear_terminal()
    logged_in = False
    admin_rights = False
    while not logged_in:

        print(f"{MENU_LINES}\n Welcome to Task Manager Pro \n{MENU_LINES}")
        print("\nPlease login using your username and password:\n")
        current_user = input("Username: ")
        current_password = input("Password: ")
        if current_user not in username_password.keys():
            print("User does not exist\n")
            continue
        elif username_password[current_user] != current_password:
            print("Password is incorrect\n")
            continue
        elif current_user == "admin":
            admin_rights = True
        print("\n>>>Login Successful<<<\n")
        print(f"Welcome back {current_user}")
        logged_in = True
    user_menu(admin_rights, current_user)


def user_menu(admin_rights, current_user):
    """
    The function `user_menu` presents a menu to the user based on their admin
    rights and current user,
    and performs different actions based on the user's input.

    :param admin_rights: The parameter `admin_rights` is a boolean value that
    indicates whether the
    current user has admin rights or not. If `admin_rights` is `True`, menu
    displays additional functions
    :param current_user: The current_user parameter represents the username of
    the user who is currently logged in.
    """
    while True:
        # presenting the menu to the user and
        # making sure that the user input is converted to lower case.
        print(f"\nCurrent user: {current_user.title()}\n")
        if admin_rights:
            menu = input(
                """Select one of the following options below:

    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    gr - generate reports
    ds - Display statistics
    s - switch user
    e - Exit
    \n: """
            ).lower()
        else:
            menu = input(
                """Select one of the following Options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my task
    s- switch user
    e - Exit
    \n: """
            ).lower()

        if menu == "r":
            reg_user()

        elif menu == "a":
            add_task()

        elif menu == "va":
            view_all()

        elif menu == "vm":
            view_mine(current_user)

        elif menu == "gr" and current_user == "admin":
            report = input(
                """\nWhich reports would you like to view?\n
to - Overview of all tasks assinged to team
uo - Current state of tasks assigned to the team\n
: """
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
            """If the user is an admin they can display statistics
            about number of users and tasks."""

            print(MENU_LINES)
            print(f"Number of users: \t\t {user_stats()}")
            print(f"Number of tasks: \t\t {task_stats()}")
            print(MENU_LINES)

        elif menu == "s":
            log_in()
        elif menu == "e":
            print("Goodbye!!!")
            exit()

        else:
            print("You have made a wrong choice, Please Try again")


def start_task_manager():
    log_in()


start_task_manager()
