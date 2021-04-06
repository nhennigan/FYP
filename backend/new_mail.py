import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def sendmail(receiver_address):
    mail_content = 'Dear student,\n\nThis is an automated email from the exam timetabling service.\n\nThere has been a change to an exam(s) you are enrolled for. Please be advised to check the website to note these changes to your timetable.\n\nIf you have any questions regarding this change please contact the exams office at examsoffice@nuigalway.ie or call 091-493024.'
    
    #The mail addresses and password
    sender_address = 'exam.timetable.updates@gmail.com'
    sender_pass = 'Examtimetable'
#    receiver_address = ['niamhhennigan@gmail.com','n.hennigan3@nuigalway.ie']
    #Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = ", ".join(receiver_address[0])
    message['Subject'] = 'Change to exam timetable'   #The subject line
    #The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    #Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
    session.starttls() #enable security
    session.login(sender_address, sender_pass) #login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
   # print('Mail Sent')
