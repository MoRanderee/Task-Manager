'''
This program has been designed to help small businesses manage their staff
and the particular tasks that have been assigned to them.

All users must login and to add new tasks, view all tasks with its details 
or view tasks allocated to them with its details.
Only user's with administrator access have the ability to add new users 
and view the total number of users and tasks.'''

# defining functions:
def reg_user():

    newuser_valid = False # use to verify if username is already in use
    all_users = [] # list to store details of all users
    while newuser_valid == False:

        new_username = input("Please enter new username: ") # variable to store username requested

        path = 'user.txt'
        with open(path, 'r') as f:

            # read in all existing users and passwords
            for line in f:
                info = line.split(", ")
                all_users.append(info[0])
        
        # check if the username is already being used
        if new_username in all_users:
            print("Username is already taken. Please try a different username.")
        
        else:
            # otherwise dont ask for a different username
            newuser_valid = True

    newpass_valid  = False # used to verify if password is entered correctly
    while newpass_valid == False: 

        new_pass = input(f"Please enter password for {new_username}: ") # variable to store password requested
        confirm_pass = input(f"Please confirm password for {new_username}: ") # variable used to verify password
        
        # Check if the passwords match 
        if new_pass == confirm_pass:
            newpass_valid = True
            path = 'user.txt'
            f = open(path, 'a')
            f.write(f"\n{new_username}, {new_pass}") # add new user to the file of users
            f.close()

            print("New user has been registered.")

        else:
            print("The passwords do not match. Please try again.")

def add_task():

    # Get all task details from the user
    task_user = input("Who do you want to assign the task to? ")
    task_title = input("Please enter the name of this task: ")
    task_descr = input("Please enter a description for this task: ")
    date_due = input("Please enter a due date for this task (Day/Month/Year): ")
    date_assigned = datetime.datetime.now().strftime("%d "+ calendar.month_abbr[date.today().month] +" %Y")
    complete = "No"

    # add new task to the tasks file
    path = 'tasks.txt'
    f = open(path,'a')
    f.write(f"\n{task_user}, {task_title}, {task_descr}, {date_assigned}, {date_due}, {complete}")
    f.close()

def view_all():

# read all tasks and their details from the task file
    path = 'tasks.txt'
    with open(path, 'r') as f:
        for line in f:
            info = line.split(", ")

            task_user = info[0]
            task_title = info[1]
            task_descr = info[2]
            date_assigned = info[3]
            date_due = info[4]
            complete = info[5]

            # display tasks in suitable format
            print(f'''_____________________________________________________
Task: \t\t {task_title}
Assigned to: \t {task_user}
Date assigned: \t {date_assigned}
Due date: \t {date_due}
Task complete? \t {complete}
Task description: \n {task_descr}
_____________________________________________________
                ''')

def view_mine():

    # read all tasks and their details from the task file
    path_task = 'tasks.txt'

    # initialize list variables to store data
    task_user = []
    task_title = []
    task_descr = []
    date_assigned = []
    date_due = []
    complete = []
    
    task_num = []
    num = 0

    # open the task file and store all lines
    with open(path_task, 'r') as f: 
        
        lines = f.readlines()

    # open the task file 
    with open(path_task, 'r') as f: 
        # iterate through each line
        for line in f:

            info = line.split(", ")

            # check if the task is assigned to the user logged in
            if username == info[0]:
                
                # store the info of the user's tasks
                task_user.append(info[0])
                task_title.append(info[1])
                task_descr.append(info[2])
                date_assigned.append(info[3])
                date_due.append(info[4])
                complete.append(info[5])

                # increment the task number
                num += 1
                task_num.append(num)

    f.close()

    # add the option to return to menu
    task_num.append('-1')
    task_title.append("Return to main menu")

    # ask user to select task 
    print("Please select a task:")
    
    # print each task on a new line with a corresponding number
    for i in range(len(task_num)):
        print(f'{task_num[i]}', ' : ', task_title[i])
    
    # get input from user
    select_task = int(input(""))

    # if the user selects to go to main menu
    if select_task == -1:
        return

    # check if the user entered a valid task number
    elif select_task in task_num:

        # retrieve the status of the task
        complete_status = complete[select_task-1].strip("\n")

        # show additional options for selected task
        print(f"Select one of the actions below for '{task_title[select_task-1]}':")
        task_actions = input(''' 
'M': Mark the task complete,
'E': Edit the task
''').upper()

        # if the user selected to mark the task complete and its not already complete
        if task_actions == 'M' and complete_status == "No":
            
            # execute the function to mark the task complete
            mark_complete(complete, select_task, path_task,
                        task_title, task_user, task_descr, date_assigned, date_due, lines)
        
        # if the user selected to mark the task complete and its already complete
        elif task_actions == 'M' and complete_status == "Yes":
            print("Task is already complete.\n")
            return

        # if the user selected to edit the task and its not already complete
        elif task_actions == 'E' and complete_status == "No":

            # show additional options to edit the task
            print(f"Select one of the actions below to edit '{task_title[select_task-1]}':")         
            edit_action = input('''
'1': Change the user the task is assigned to,
'2': Change the due date of the task
    ''')

            # if the user wants to edit the assigned user
            if edit_action == '1':
                
                # execute function to change assigned user - send all variables required
                edit_task_assigned(complete, select_task, path_task,
                                        task_title, task_user, task_descr, date_assigned, date_due, lines)

            # if the user wants to edit the task due date
            elif edit_action == '2':

                # execute function to change task due date - send all variables required
                edit_task_duedate(complete, select_task, path_task,
                                    task_title, task_user, task_descr, date_assigned, date_due, lines)
            
            # for an invalid entry of editing task
            else:
                print("Please select a valid option.\n")
                return

        # if the user selected to edit the task and its already complete
        elif task_actions == 'E' and complete_status == 'Yes':
            print("Sorry, you are not allowed to edit tasks that are complete.\n")
        
        # for an invalid entry of M or E
        else:
            print("Please select a valid option.\n")
        

    # for an invalid entry of task selection
    else:
        print("Please select a valid option.\n")
        return
        
def mark_complete(complete, select_task, path_task,
                    task_title, task_user, task_descr, date_assigned, date_due, lines):
    
    # change the task completed status
    complete_status = 'Yes'
    complete[select_task-1] = complete_status

    # create a new task file - overide previous
    with open(path_task, "w") as g:

        # iterate through the task file lines that was previously stored
        for line in lines:
            
            info = line.split(", ")

            # for the task that was edited or the specific user, write back the updated info
            if info[0] == task_user[select_task-1] and info[1] == task_title[select_task-1]:
                g.write(f"{task_user[select_task-1]}, {task_title[select_task-1]}, {task_descr[select_task-1]}, {date_assigned[select_task-1]}, {date_due[select_task-1]}, {complete[select_task-1]}\n")

            # for the tasks that were not edited, write back the original line
            else:
                g.write(line)  

    print("Success - Task has been marked complete.\n")

def edit_task_assigned(complete, select_task, path_task,
                        task_title, task_user, task_descr, date_assigned, date_due, lines):

    new_user = input("Who would you like to assign this task to?\n")
                    
    # verify if the user is registered
    valid_user = False

    # iterate through all users in user list
    for details in users:

        # check if the user is registered
        if new_user == details[0]: 
            valid_user = True
        
    # once the user is verified, the task can be updated
    if valid_user == True:
        
        # change the assigned user for the task that was selected
        task_user[select_task-1] = new_user

        # create a new task file - overide previous
        with open(path_task, "w") as g:

            # iterate through the task file lines that was previously stored
            for line in lines:
                
                info = line.split(", ")

                # for the task that was edited or the specific user, write back the updated info
                if info[0] == task_user[select_task-1] and info[1] == task_title[select_task-1]:
                    g.write(f"{task_user[select_task-1]}, {task_title[select_task-1]}, {task_descr[select_task-1]}, {date_assigned[select_task-1]}, {date_due[select_task-1]}, {complete[select_task-1]}")

                # for the tasks that were not edited, write back the original line
                else:
                    g.write(line)

        print(f"Success - the task has been assigned to {new_user}.\n")

    # if the assigned user is not registered
    else:
        print("Sorry, that is not an existing user.\n")              

def edit_task_duedate(complete, select_task, path_task,
                        task_title, task_user, task_descr, date_assigned, date_due, lines):
    
    # ask the user for a new due date
    new_duedate = input("Please enter a new due date (Day/Month/Year):\n")

    # change the due date for the selected task
    date_due[select_task-1] = new_duedate

    # create a new task file - overide previous
    with open(path_task, "w") as g:

        # iterate through the task file lines that was previously stored
        for line in lines:
            
            info = line.split(", ")

            # for the task that was edited, write back the updated info
            if info[0] == task_user[select_task-1] and info[1] == task_title[select_task-1]:
                g.write(f"{task_user[select_task-1]}, {task_title[select_task-1]}, {task_descr[select_task-1]}, {date_assigned[select_task-1]}, {date_due[select_task-1]}, {complete[select_task-1]}\n")

            # for the tasks that were not edited, write back the original line
            else:
                g.write(line)                    

    print("Success - the due date for this task has been updated.\n")

def gen_reports():
    
    path_task = 'tasks.txt'
    path_users = 'user.txt'
    path_task_overview = 'task_overview.txt'
    path_user_overview = 'user_overview.txt'

     # initialise variables:
    tot_tasks = 0
    tot_complete_tasks = 0
    tot_incomplete_tasks = 0
    tot_overdue_tasks = 0
    perc_incomplete = 0
    perc_overdue = 0

    # get current date
    current_date = datetime.datetime.now().strftime("%d "+ calendar.month_abbr[date.today().month] +" %Y")

    # open task file to read info
    with open(path_task, "r") as f:

        # iterate through lines in file
        for line in f:
            line = line.strip("\n")
            info = line.split(", ")
            
            # substring the due date to get the month 
            month_due = info[4][3:6]
            # convert the month into a number
            month_due = datetime.datetime.strptime(month_due, "%b").month
            
            # substring the current date to get the month 
            month_current = current_date[3:6]
            # convert the month into a number
            month_current = datetime.datetime.strptime(month_current, "%b").month
            
            # check if the due date has lapsed and increment counter
            if (current_date[len(current_date)-4:len(current_date)] < info[4][len(current_date)-4:len(current_date)]): 
                tot_overdue_tasks += 1
            elif (month_current < month_due):
                tot_overdue_tasks += 1
            elif (current_date[0:2] < info[4][0:2]):
                tot_overdue_tasks += 1

            # check if task is complete and increment counter
            if info[5] == "Yes":
                tot_complete_tasks += 1

            # increment counter for tasks
            tot_tasks += 1

    # calc number of incomplete tasks
    tot_incomplete_tasks = tot_tasks - tot_complete_tasks

    # calc percentage of incompleted tasks
    perc_incomplete = round((tot_incomplete_tasks/tot_tasks)*100)
    
    # calc percentage of overdue tasks
    perc_overdue = round((tot_overdue_tasks/tot_tasks)*100)

    # create a new file to store the overview of tasks
    with open(path_task_overview, "w") as f:

            f.write(f'''
Total tasks: {tot_tasks}
Total complete tasks: {tot_complete_tasks}
Total incomplete tasks: {tot_incomplete_tasks}
Total overdue tasks: {tot_overdue_tasks}
Percentage tasks incomplete: {perc_incomplete}
Percentage tasks overdue: {perc_overdue}
            ''')

    # initialise variables:
    num_users = 0
    user_tasks = 0
    complete_tasks = 0
    overdue_tasks = 0
    perc_tasks = 0
    perc_complete = 0
    perc_incomplete = 0
    perc_overdue = 0

    user_info = []
    all_user_info = []

    # open user file to read info
    with open(path_users, "r") as f:

        # iterate through each user
        for line_1 in f:
            info = line_1.split(", ")
            user = info[0]

            # increment counter of users
            num_users += 1

            # reset counter of tasks and overdue tasks
            user_tasks = 0
            overdue_tasks = 0

            # open task file to read info
            with open(path_task, "r") as g:

                # iterate through each task
                for line_2 in g:
                    line_2 = line_2.strip("\n")
                    info = line_2.split(", ")

                    # look at each task allocated to a specific user
                    if user == info[0]:
                        # increment the task counter for the user
                        user_tasks +=1                            

                        # check if task is complete and increment counter for user
                        if info[5] == "Yes":
                            complete_tasks += 1
                        
                        # substring the due date to get the month 
                        month_due = info[4][3:6]
                        # convert the month into a number
                        month_due = datetime.datetime.strptime(month_due, "%b").month
                        
                        # substring the current date to get the month 
                        month_current = current_date[3:6]
                        # convert the month into a number
                        month_current = datetime.datetime.strptime(month_current, "%b").month

                        # check if the due date has lapsed and increment counter
                        if (current_date[len(current_date)-4:len(current_date)] < info[4][len(current_date)-4:len(current_date)]): 
                            overdue_tasks += 1
                        elif (month_current < month_due):
                            overdue_tasks += 1
                        elif (current_date[0:2] < info[4][0:2]):
                            overdue_tasks += 1

                # after going through all tasks for a specific user, calc the required output for each user
                if user_tasks == 0:
                    perc_tasks = perc_complete = perc_incomplete = perc_overdue = 0
                else:
                    perc_tasks = round((user_tasks/tot_tasks)*100)
                    perc_complete = round((complete_tasks/user_tasks)*100)
                    perc_incomplete = 100-perc_complete
                    perc_overdue = round((overdue_tasks/user_tasks)*100)

                # store task info for each user in a list
                user_info = [user, user_tasks, perc_tasks,perc_complete,perc_incomplete,perc_overdue]

                # store task info for all users in a list
                all_user_info.append(user_info)

        # create a new file to store the overview of users
        with open(path_user_overview, "w") as f:

            # record the total number of users
            f.write(f"Total number of users: {num_users}.\n")

            # iterate through each user's task info
            for user in all_user_info:
                
                # record the info of each user's tasks
                f.write(f'''
    User: {user[0]}
    Total tasks: {user[1]}
    Percentage of total tasks: {user[2]}
    Percentage complete tasks: {user[3]}
    Percentage incomplete tasks: {user[4]}
    Percentage overdue tasks: {user[5]}
                    ''')

    print("Success - reports have been generated\n")

#=====importing libraries===========
# These libraries will be used to get the current date
 
import datetime 
from datetime import date
import calendar

#====Login Section====        
users = [] # create an empty list to store user details
path = 'user.txt'
with open(path, 'r') as f:
    for line in f: # iterate through each line in the user file

        line = line.strip("\n") # remove the \n that is read in from the text file
        user_details = line.split(", ") # split the username from the password - store as a list
        users.append(user_details) # store all usernames and passwords as a list of lists

username = "" # variable to store the entered username
password = "" # variable to store the entered password
user_valid = False # set username as invalid if password is invalid
pass_valid = False # set password as invalid if username is invalid

while user_valid == False: # repeat while the username and password is incorrect

    username = input("Please enter your username: ") # request user to enter username

    for details in users: #iterate through the list of user details

        if username == details[0]: # if the entered username matches a username in the list
            user_valid = True # set username to valid

            # only run if the username is valid
            while pass_valid == False:
                
                password = input("Please enter your password: ") # request user to enter password

                if password == details[1]: # if the entered password matches the password linked to the username 
                    pass_valid = True # set password as valid

                else:
                    print("Incorrect password.")
        
    if user_valid == False: # if there is no mathching username in the list
        print("Please enter a valid username.")


while True: # repeat this code block until the exit option is selected
    
    #presenting the menu to the user and 
    # making sure that the user input is coneverted to lower case.
    
    if username == "admin": # present special menu for admin user
        menu = input('''Select one of the following options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my tasks
    gr - Generate reports
    ds - Display statistics
    e - Exit
    : ''').lower()

    else: # present standard menu for other users

        menu = input('''Select one of the following options below:
    r - Registering a user
    a - Adding a task
    va - View all tasks
    vm - View my tasks
    e - Exit
    : ''').lower()

    if menu == 'r' and username == "admin":
        
        reg_user()

    if menu == 'gr' and username == "admin":
        
        gen_reports()

    elif menu == 'a':
        
        add_task()

    elif menu == 'va':
        
        view_all()

    elif menu == 'vm':

        view_mine()

    elif menu == 'ds' and username == "admin":
        tasks = 0 # set task counter to 0
        users = 0 # set user counter to 0

        path = 'tasks.txt'
        with open(path, 'r') as f:
            for line in f: # iterate through each task in the file
                tasks += 1 # increment the task counter by 1
        
        path = 'user.txt'
        with open(path, 'r') as f:
            for line in f: # iterate through each user in the file
                users += 1 # increment the user counter by 1

        print(f'''______________________________________
Total tasks: {tasks}
Total users: {users}
______________________________________''')

    elif menu == 'e':
        print('Goodbye!!!')
        exit() # exit out of the loop and stop running the program

    else:
        print("You have made a invalid selection, please try again")