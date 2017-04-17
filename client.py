import smtplib
import sys
import os.path
import getpass
import imaplib
import email
import datetime

os.system('clear')
print("Interesting facts from Wikipedia:\n")
print('''Beta, named after the second letter of the Greek alphabet,
is the software development phase following alpha.
Software in the beta stage is also known as betaware.
Beta phase generally begins when the software is feature complete
but likely to contain a number of known or unknown bugs.
Software in the beta phase will generally have many more bugs in it
than completed software, as well as speed/performance issues
and may still cause crashes or data loss.
The focus of beta testing is reducing impacts to users,
often incorporating usability testing.''')
print("\nBefore we start, please login to Gmail (only Gmail accounts)")
print("Note: you shoud allow less secure apps to access your account\n")
login = raw_input("email (_mail_@gmail.com): ")
password = getpass.getpass()

#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# USER INPUT for email and text
#

def user_input(text):
    '''check the user input'''
    while True:
        u_input = raw_input(text)
        if len(u_input) >= 2:
            return (u_input)
        else:
            print("length must be greater then 1")

def top_level_domain(text):
    '''check top-level domain in the end of email address'''
    my_file = "tlds-alpha-by-domain.txt"
    if not os.path.isfile(my_file):
        print("No file. Abort")
        sys.exit(1)
    dot_point = text.rfind(".")
    end = text[dot_point + 1:].upper() + '\n'
    with open(my_file) as read_file:
        for line in read_file:
            if end == line:
                return (True)
    return (False)

def email_input(text):
    '''checking the email'''
    while True:
        u_input = raw_input(text)
        if len(u_input) >= 5:
            if u_input.find('@') != -1 and u_input.find('.') != -1:
                if u_input[0] != '.' and u_input[0] != '@':
                    if u_input.count('@') == 1:
                        if top_level_domain(u_input):
                            return (u_input)
            print("bad email, try again")
        else:
            print("length must be greater then 5 (a@b.cc)")

#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# USER INPUT for menu and checker
#

def ft_input_number(max_num):
    while True:
        if max_num > 0:
            text = '\nEnter your choice [0 - ' + str(max_num) + '] '
        else:
            text = '\nEnter your choice [0] '
        u_input = raw_input(text)
        if u_input.isdigit() and int(u_input, 10) >= 0 and int(u_input, 10) <= max_num:
            print ""
            break
        print "wrong input, try again"
    return (int(u_input, 10))

def ft_input_string():
    while True:
        u_input = raw_input("input here: ")
        if len(u_input) > 0:
            return (u_input)
        print "bad imput"

#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# MENU headers
#

def show_header_menu(name):
    os.system('clear')
    print "--------------------------------------------"
    print "   ", name
    print "--------------------------------------------\n"

def show_header_message(message):
    print message, "\n"

def ft_option(num, name):
    text = "[" + str(num) + "] " + name
    print text

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# SEND SUBMENU
#

def sendto_submenu(trio):
    trio[0] = email_input("Send to (email): ")
    raw_input("\npress ENTER")

def subject_submenu(trio):
    trio[1] = user_input("Subject: ")
    raw_input("\npress ENTER")

def text_submenu(trio):
    trio[2] = user_input("Message:\n\n")
    raw_input("\npress ENTER")

## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# SEND MENU
#
def letter_review(trio):
    print("-------------------------------------------------------------------")
    print("Send to: " + str(trio[0]))
    print("-------------------------------------------------------------------")
    print("Send from: " + str(login))
    print("-------------------------------------------------------------------")
    print("Subject: " + str(trio[1]))
    print("-------------------------------------------------------------------")
    print("Body:\n\n" + str(trio[2]))
    print("-------------------------------------------------------------------")
    raw_input("\npress ENTER")

def send_menu_usage():
    show_header_menu("SEND letter \(beta\)")
    show_header_message("So, what do you want to do?")
    ft_option(0, "back to the MAIN menu")
    ft_option(1, "[Send to:]")
    ft_option(2, "[Subject:]")
    ft_option(3, "Write message")
    ft_option(4, "Review letter")
    ft_option(5, "SEND")

def send_menu(trio, history):
    arguments = 5
    while True:
        send_menu_usage()
        user_input = ft_input_number(arguments)
        if (user_input == 0):
            break
        elif (user_input == 1):
            sendto_submenu(trio)
        elif (user_input == 2):
            subject_submenu(trio)
        elif (user_input == 3):
            text_submenu(trio)
        elif (user_input == 4):
            letter_review(trio)
        elif (user_input == 5):
            if trio[0] == 'None':
                print("empty destination")
                raw_input("\npress ENTER")
                continue
            if trio[2] == 'None':
                print("empty message")
                raw_input("\npress ENTER")
                continue
            send_message(trio, history)
#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# Sent mailbox
#

def read_history(history):
    if not history:
        print("No history")
    for each in history:
        print("Send to: ", each[0])
        print("Subject: ", each[1])
        print("Message: ", each[2])
        print("-------------------------------------------")
    raw_input("\npress ENTER")

def delete_history(history):
    if not history:
        print("Nothing to clean")
        raw_input("\npress ENTER")
        return
    del history[:]
    print("History cleaned")
    raw_input("\npress ENTER")

def sent_mail_menu():
    show_header_menu("Sent letter \(beta\)")
    show_header_message("Check the history or delete it")
    ft_option(0, "back to the MAIN menu")
    ft_option(1, "Look at history")
    ft_option(2, "Clean history")

def sent_mail(history):
    arguments = 2
    while True:
        sent_mail_menu()
        user_input = ft_input_number(arguments)
        if (user_input == 0):
            break
        elif (user_input == 1):
            read_history(history)
        elif (user_input == 2):
            delete_history(history)

#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# MAIN MENU
#

def ft_choose_the_project_menu():
    show_header_menu("Main menu (beta)")
    show_header_message("So, what do you want to do?")
    ft_option(0, "EXIT")
    ft_option(1, "COMPOSE")
    ft_option(2, "CHECK mailbox")
    ft_option(3, "Sent mail")
    ft_option(4, "Known bugs")

def ft_choose_the_project(trio, history):
    while True:
        ft_choose_the_project_menu()
        user_input = ft_input_number(4)
        if (user_input == 0):
            print "bye bye then. exit"
            break
        elif (user_input == 1):
            send_menu(trio, history)
        elif (user_input == 2):
            recive_message()
        elif (user_input == 3):
            sent_mail(history)
        elif (user_input == 4):
            known_bugs()

#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# Known bugs

def show_bugs():
    bags = []
    bags.append("fail if no connection")
    bags.append("Invalid credentials (Failure)")
    bags.append("no try/catch")
    bags.append("no server statuses")
    bags.append("no logs for connections")
    bags.append("no user classes (only methods)")
    bags.append("only gmail")
    bags.append("bad trio clean after sent")
    for each in bags:
        print(each)
    raw_input("\npress ENTER")

def known_bugs_menu():
    show_header_menu("Known bugs (beta)")
    show_header_message("If you have something to add, tell me")
    ft_option(0, "back to the MAIN menu")
    ft_option(1, "show list")

def known_bugs():
    arguments = 2
    while True:
        known_bugs_menu()
        user_input = ft_input_number(arguments)
        if (user_input == 0):
            break
        elif (user_input == 1):
            show_bugs()

#
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# main
#

def bad_login_password():
    print("login/password is not set.\nPlease start again")
    raw_input("\npress ENTER")
    sys.exit(0)

def read_mailbox(mailbox):
    rv, data = mailbox.search(None, "ALL")
    index = 0
    for num in data[0].split():
        index = index + 1
        rv, data = mailbox.fetch(num, '(RFC822)')
        msg = email.message_from_string(data[0][1])
        print repr('[%s]: %s' % (num, msg['Subject']))
        if index == 10:
            return

def recive_message():
    if not login or not password:
        bad_login_password()
    mailbox = imaplib.IMAP4_SSL('imap.gmail.com')
    mailbox.login(login, password)
    rv = mailbox.list()
    rv, data = mailbox.select("staff")
    if rv == 'OK':
        read_mailbox(mailbox)
        mailbox.close()
    mailbox.logout()
    raw_input("\npress ENTER")

def send_message(trio, history):
    if not login or not password:
        bad_login_password()
    history_list = list(trio)
    history.append(history_list)
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    send_from = login
    send_to = trio[0]
    subject = trio[1]
    text = trio[2]
    msg = "\r\n".join(["From:" + login, "To:" + send_to, "Subject:" + subject, "", text])
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(login, password)
    server.sendmail(send_from, send_to, msg)
    server.quit()
    trio[0] = 'None'
    trio[1] = 'None'
    trio[2] = 'None'
    print('OK, message sent')
    raw_input("\npress ENTER")

def main():
    '''main method'''
    trio = ['None', 'None', 'None']
    history = []
    ft_choose_the_project_menu()
    ft_choose_the_project(trio, history)

if __name__ == "__main__":
    main()
