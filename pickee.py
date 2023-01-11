import pickle
import pyfiglet # used for fancy text
print(pyfiglet.figlet_format("DPSI")) # prints DPSI in fancy text
# Below is the try and except statement for the Password file.
# If it exists, it will read the password stored and use that as the password variable
# If it doesn't exist (FileNotFoundError), it will create a file with the default password (DPSI TEACHER PASS)
# If the passsword file is empty, it will display a warning.
try:
    fil = open('Password', 'rb')
    Password = pickle.load(fil)
    if Password == '':
        print("There is no password entered. So, just press enter. Please set a password after this program.")
    fil.close()
except FileNotFoundError:
    Password = 'DPSI TEACHER PASS'
    with open('Password', 'wb') as f:
        pickle.dump(Password, f, pickle.HIGHEST_PROTOCOL)
# this portion of the code creates a list for the names of the students.
# if the file exists, it reads the names in it and stores them into the names list.
# if the file doesn't exist, it creates a blank file.
names = []
try:
    with open('List of names', 'rb') as f:
        try:
            names.append(pickle.load(f).split(', '))
        except EOFError:
            names.append('')
except FileNotFoundError:
    with open('List of names', 'wb') as fi:
        pickle.dump('', fi, pickle.HIGHEST_PROTOCOL)
Admin = None # used for the password system.
def grades(input): # self explanatory, a dictionary is used to prevent constant if: conditions
    marksDict = {
        range(90,101): 'A',
        range(80,90): 'B',
        range(70,80): 'C',
        range(60,70): 'D',
        range(0,60): 'Fail'
    }
    # takes out the grade by checking if the input is in the key
    for key in marksDict:
        grade = marksDict[key]
        if round(input) in key:
            return grade
def ra(input):
    with open(f'{input}', 'rb') as f:
        while True:
            try:
                l = pickle.load(f)
            except EOFError:
                return l
# checks entered values for errors.
# dtype is used to check the input type ({str}, {int}, {float}, {bool})
# r1, r2 are the range of values
# cLimit is used to prevent too much memory being used and too many inputs being provided.
def valueCheckedInput(dtype=str, inputMessage="", r1=-100000000000, r2=100000000000, cLimit=10000):
    dtypeList = [str, int, float, bool]
    count = 0
    while count < cLimit:
        if dtype in dtypeList:
            try:
                x = dtype(input(f"{inputMessage}"))
                if x >= r1 and x <= r2:
                    return x
                else:
                    print(f"value must be between {r1} and {r2}")
                    continue
            except:
                count+=1
                print(f"value must be a {str(dtype)}")
                continue
        else:
            return 0
# checks if the name is valid
def nameCheck(val: str):
    strings = val.split()
    checkList = [i.isalpha() for i in strings]
    count = len([val for val in checkList if val == False])
    if count == 0: return True
    else: return False
# Used to write the report cards.
def cardWriter():
    # takes name input without breaking if the input is invalid
    while True:
        name = input("Enter the student's name: ")
        if nameCheck(name) == True: break
        else: continue
    names.append(name)
    n = str(names).replace('[', '').replace(']', '').replace("'", '')
    # Marks for each subject
    math_grade = valueCheckedInput(float, "Enter grade for Mathematics: ", 0, 100)
    computer_grade = valueCheckedInput(float, "Enter grade for Computer Science: ", 0, 100)
    english_grade = valueCheckedInput(float, "Enter grade for English: ", 0, 100)
    # Calculation part
    total_marks = math_grade + computer_grade + english_grade
    average_marks = total_marks / 3
    grade = grades(average_marks)
    # Create the report card for the student
    report_card = f"---------------------\n" \
                  f"{name}'s report card:\n" \
                  f"maths marks: {math_grade}\n" \
                  f"computer marks: {computer_grade}\n" \
                  f"english marks: {english_grade}\n" \
                  f"Total marks: {total_marks}\n" \
                  f"Average marks: {average_marks:.2f}\n" \
                  f"Grade: {grade}\n---------------------\n"
    # open the card for the student with encoding and writes the report card into it.
    # opens the class card and appends the report card into it.
    report_card_l = report_card.split("\n")
    with open(f'{name} report card', 'wb') as card:
        pickle.dump(report_card_l, card, pickle.HIGHEST_PROTOCOL)
    with open('Class Card', 'wb') as cc:
        pickle.dump(report_card_l, cc, pickle.HIGHEST_PROTOCOL)
    temp = open('Class Card', 'rb')
    c = pickle.load(temp)
    print(type(c))
    if type(c) == "<class 'list'>":
        ce = ''
        for i in c:
            ce += (i + '\n')
        final = ''
        for i in report_card_l:
            final += (i + '\n')
        ce += final
        temp.close()
    else:
        ce = ''
        final = ''
        for i in report_card_l:
            final += (i + '\n')
        ce += final
        temp.close()
    with open('Class Card', 'wb') as cc:
        pickle.dump(ce, cc, pickle.HIGHEST_PROTOCOL)
    # adds the names into list of names.
    with open('List of names', 'wb') as l:
        pickle.dump(n, l, pickle.HIGHEST_PROTOCOL)
# Used to edit the report card of a student.
def cardEditor():
    # Reads the list of names
    # {f.close()} is not required since we're using {with open()} which automatically closes the file.
    with open("List of names", "rb") as f:
        namesList = pickle.load(f)
    # Checks if there is no card
    if not names or namesList == "":
        print("No student cards were found, please write a new student card first")
    # Main portion of the code.
    # Uses cont1 variable since we are working with nested loops

    else:
        cont1 = True
        while cont1:
            print(f"Students who have a card are {n}")
            name = input("please enter the student's name who's card you wish to edit: ")
            # if the student has a file, it will proceed to read the file.
            # if the student doesn't have a file {FileNotFoundError}, it will display an error message.
            try:
                lines = ra(f'{name} report card')
                print(lines)
            except FileNotFoundError:
                print("please enter a name from the list\n")
                print("--------------------------------------------------------------------")
                continue
            # Asks which marks you want to change
            # Then, checks if the subject entered is valid.
            # After, asks for the number you want to change it to.
            # Finally, updates the card and class card and asks if you want to edit another grade
            # If yes, it will proceed to change another grade. If no, then it will exit.
            while True:
                # inputs
                subject = input("please enter which subject's marks you wish to change (maths for maths, computer for computer science and english for english.): ")
                if subject.lower() == "maths":
                    num = valueCheckedInput(float, 'Please enter the marks you want to change it to: ', 0, 100)
                    lines[2] = f'maths marks: {num}\n'
                    break
                elif subject.lower() == "computer":
                    num = valueCheckedInput(float, 'Please enter the marks you want to change it to: ', 0, 100)
                    lines[3] = f'computer marks: {num}\n'
                    break
                elif subject.lower() == "english":
                    num = valueCheckedInput(float, 'Please enter the marks you want to change it to: ', 0, 100)
                    lines[4] = f'english marks: {num}\n'
                    break
                else:
                    print("invalid value")
                    continue
            # Editing of the card.
            with open(f"{name} report card", "wb") as f:
                pickle.dump(lines, f, pickle.HIGHEST_PROTOCOL)
            l = ra(f'{name} report card')
            math = float(l[2].replace("maths marks: ", '').replace('\n', ''))
            cs = float(l[3].replace("computer marks: ", '').replace('\n',''))
            eng = float(l[4].replace("english marks: ", '').replace('\n', ''))
            b = open(f'{name} report card', 'wb')
            total = math + cs + eng
            avg = round((total / 3), 2)
            grade = grades(avg)
            card = f"---------------------\n{name}'s report card:\nmaths marks: {math}\ncomputer marks: {cs}\nenglish marks: {eng}\nTotal marks: {total}\nAverage: {avg}\nGrade: {grade}\n---------------------\n"
            li = open('Class Card', 'rb')
            ln = pickle.load(li)
            le = ''
            for i in ln:
                le += (i + '\n')
            le = le + card
            pickle.dump(le,b,pickle.HIGHEST_PROTOCOL)
            b.close()
            a = open('Class Card', 'wb')
            pickle.dump(le,a,pickle.HIGHEST_PROTOCOL)
            a.close()
            # choice
            while True:
                choice = input("would you like to change another grade? (Y/N): ")
                if choice.lower() == 'y':
                    cont1 = True
                    break
                elif choice.lower() == 'n':
                    cont1 = False
                    break
                else:
                    print("The input is invalid")
                    continue
# Reads the card of students
# If the list of names doesn't have any names, it will display an error.
# Otherwise, it will continue with the rest of the code
# It asks for the student name.
# If the file for the student exists, then it will open the file and print it into console.
# If the file doesn't exist, it will show an error.
def cardReader():
    with open("List of names", "rb") as f:
        namesList = pickle.load(f)
    if not names or namesList == "":
        print("No student cards were found, please write a new student card first")
    else:
        while True:
            print(f"The students are: {n}")
            name = input("Enter the student's name of whose report card you want: ").capitalize()
            try:
                with open(f"{name} report card", "rb") as f:  # making it easier to work with
                    report_card = pickle.load(f) 
                    print(report_card)
                    report_card = report_card.split('\n') # reads the report card and stores it into a variable
                    final = ''
                    for i in report_card:
                        final = (i + '\n')
                print(final)  # prints the report card
                break
            except FileNotFoundError:  # If there is a FileNotFoundError
                print(f"Report card for {name} not found.") # This is printed.
                continue
# Reads the classCard and prints it into console.
# If the Class card exists, it will read and print it into the console.
# If it doesn't exist {FileNotFoundError}, it will send an error.
def classCard():
    try:
        with open('Class Card', 'rb') as card:
            print(pickle.load(card))
    except FileNotFoundError:
        print("Class card has not yet been generated")
# Changes the password.
# Since the password file is created in the start, there is no need for a {try:} and {except:} statement.
def changePass():
    changedPass = input("Enter the new password: ")
    with open('Password', 'wb') as f:
        pickle.dump(changedPass, f, pickle.HIGHEST_PROTOCOL)
        print(f"Successfully changed password. The new password is {changedPass}")
# List of functions (who would've guessed)
functionsList = [cardWriter, cardEditor, changePass, cardReader, classCard]
# contains the main UI (user interface) of the code.
# It checks if the user is an admin with the admin flag.
# If the user is an admin, it will open all functions.
# If the user is not an admin, it will open only the {readCard()} and {classCard()} functions.
# If the admin flag is neither True or False, it will continue and ask for the admin password.
# If the user inputs the password correctly, the admin flag is set to True
# If the user inputs the password incorrectly, they are given 3 tries to get it right.
# If the user still doesn't get the password correctly, the program continues with the non-administrative mode.
# If the user says that they aren't an Admin, the program will continue in non-Administrative mode.
error_check = 0 # used for error checking in the admin section of the code.
while True:
    n = str(names).replace('[', '').replace(']', '').replace("'", '')
    if Admin == True:
        print("---------------------------------------------------------------------\n"
        "press 1 if you want to write to a new file\n"
        "press 2 if you want to append the marks of an existing file\n"
        "press 3 if you want to change the password\n"
        "press 4 if you want to read the report card of a specific student\n"
        "press 5 if you want the class report\n"
        "press 0 if you want to exit\n")

        choice = valueCheckedInput(int, "please enter your choice: ", 0, 5)
        if choice in range(1, 6):
            print("-----------------------------------------------------------------")
            functionsList[choice - 1]()
        else:
            print("now exiting the program\n"
                "-----------------------------------------------------------------")
            break
    elif Admin == False:
        print("---------------------------------------------------------------------\n"
            "press 1 if you want to read the report card of a student.\n"
            "press 2 if you want to read the class report card\n"
            "press 0 if you want to exit\n")
        choice = valueCheckedInput(int, "please enter your choice: ", 0, 2)
        if choice in range(1,3):
            print("-----------------------------------------------------------------")
            functionsList[choice+2]()
        else:
            print("Exiting")
            print("-----------------------------------------------------------------")
            break
    else:
        while True:
            Passcheck = input("Please enter the administrative password: ")
            if Passcheck == Password:
                print("Okay, confirmed.\nWelcome Admin.")
                Admin = True
                break
            else:
                error_check += 1
                print(f"You have {4-error_check} attempt(s) remaining.")
                if error_check <= 3:
                    check = input("Are you sure you're an administrator? (Y/N)") # used to make sure that the user didn't input the incorrect password on accident.
                    if check.lower() == 'y' or check.lower() == 'yes': # if it is yes
                        print("Okay, reloading.")
                        continue # reloads the password entering screen.
                    elif check.lower() == 'n' or check.lower() == 'no': # if it is no
                        print("Okay, no problem.")
                        Admin = False # sets admin to false
                        break # and breaks the while loop to continue with non admin version of the code.
                    else: # if neither
                        print("Invalid Input.") # error message
                        continue # prompt is re-asked
                elif error_check > 3:
                    print("Sorry but the password is incorrect and you have ran out of attempts.\n""Opening in non-administrator mode.")
                    Admin = False
                    break
