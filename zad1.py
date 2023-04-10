import smtplib
from email.mime.text import MIMEText


def save_changes(student_list):
    save_path = 'data_saved.txt'
    with open(save_path, "w") as file_object_saver:
        for curr_student in student_list:
            tmp = ''
            for data in curr_student.values():
                tmp = tmp + data + ','
            tmp = tmp[:-1]
            file_object_saver.write(tmp + '\n')


def send_email(subject, body, sender, recipients, password):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender
    msg['To'] = recipients
    smtp_server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtp_server.login(sender, password)
    smtp_server.sendmail(sender, recipients, msg.as_string())
    smtp_server.quit()


def grade_students(student_list):
    if student_list[len(student_list) - 1].get('status') != 'GRADED' and student_list[len(student_list) - 1].get(
            'status') != 'MAILED':
        if int(student_list[len(student_list) - 1].get('points')) >= 91:
            student_list[len(student_list) - 1]['final_grade'] = str(5)
        elif 91 > int(student_list[len(student_list) - 1].get('points')) >= 81:
            student_list[len(student_list) - 1]['final_grade'] = str(4.5)
        elif 81 > int(student_list[len(student_list) - 1].get('points')) >= 71:
            student_list[len(student_list) - 1]['final_grade'] = str(4)
        elif 71 > int(student_list[len(student_list) - 1].get('points')) >= 61:
            student_list[len(student_list) - 1]['final_grade'] = str(3.5)
        elif 61 > int(student_list[len(student_list) - 1].get('points')) >= 51:
            student_list[len(student_list) - 1]['final_grade'] = str(3)
        else:
            student_list[len(student_list) - 1]['final_grade'] = str(2)
        student_list[len(student_list) - 1]['status'] = 'GRADED'


def student_remover(student_list, email):
    for student_check in student_list:
        if student_check['mail'] == email:
            student_list.remove(student_check)
            print('Student removed')
            return
    print('Student doesnt exist')


def student_adder(student_list, curr_line):
    curr_line = curr_line.rstrip().rsplit(',')
    for student_check in student_list:
        if curr_line[0] in student_check.values():
            print('Student already exists')
            return
    student_list.append('student{}'.format(len(student_list) + 1))
    if len(curr_line) <= 4:
        student_list[len(student_list) - 1] = {'mail': curr_line[0], 'name': curr_line[1], 'surname': curr_line[2],
                                               'points': curr_line[3],
                                               'final_grade': '',
                                               'status': ''}
    elif len(curr_line) == 5:
        student_list[len(student_list) - 1] = {'mail': curr_line[0], 'name': curr_line[1], 'surname': curr_line[2],
                                               'points': curr_line[3],
                                               'final_grade': curr_line[4], 'status': ''}
    elif len(curr_line) == 6:
        student_list[len(student_list) - 1] = {'mail': curr_line[0], 'name': curr_line[1], 'surname': curr_line[2],
                                               'points': curr_line[3],
                                               'final_grade': curr_line[4], 'status': curr_line[5]}
    grade_students(student_list=students)
    if student_list[len(student_list) - 1]['status'] != 'MAILED':
        subject = 'Python email'
        body = 'You got a grade based on the amount of points you got. Your grade: ' + student_list[len(student_list) - 1]['final_grade']
        sender = "sender"
        recipients = student_list[len(student_list) - 1]['mail']
        password = "password"
        send_email(subject, body, sender, recipients, password)
        student_list[len(student_list) - 1]['status'] = 'MAILED'


filepath = "student_data.txt"
students = []
with open(filepath) as file_object:
    for line in file_object:
        student_adder(student_list=students, curr_line=line)
file_object.close()
while True:
    checker = input('Do you want to input more students? y - yes, anything else - no\n')
    if checker == 'y':
        line = input('Please input data seperated by commas (e.g. asd@gmail.com,mark,johnson,41)\n')
        student_adder(student_list=students, curr_line=line)
    else:
        break
while True:
    checker = input('Do you want to delete students? y - yes, anything else - no\n')
    if checker == 'y':
        mail = input('Please input email of student you want to delete\n')
        student_remover(student_list=students, email=mail)
    else:
        break
save_changes(student_list=students)
