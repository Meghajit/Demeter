# import necessary packages
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import smtplib
from string import Template
    
def get_contacts(filename):
        names = []
        emails = []
        with open(filename, mode='r', encoding='utf-8') as contacts_file:
            for a_contact in contacts_file:
                names.append(a_contact.split()[0])
                emails.append(a_contact.split()[1])
        return names, emails
     
def read_template(filename):
        with open(filename, 'r', encoding='utf-8') as template_file:
           template_file_content = template_file.read()
        return Template(template_file_content)

def sendemail():

    MY_ADDRESS = "put real email id here"
    PASSWORD = "put real password here"
    files = ['files/mutualfund']
    	
    # set up the SMTP server
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(MY_ADDRESS, PASSWORD)
    
    time.sleep(60) #Sleep for 5 minutes
    
    names, emails = get_contacts('files/contactslist.txt')  # read contacts
    message_template = read_template('files/getNAV.out')
    filename = "mutualfund.jpg"
    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message
        print(name, email)
        # add in the actual person name to the message template
        message = message_template.substitute(PERSON_NAME=name.title())
    
        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        msg['Subject']="Daily Net Asset Value Mailer"  #Change to  Body  ltr
    
        # add in the message body
        msg.attach(MIMEText(message, 'plain'))
       # msg.attach(files)
        attachment = open("files/mutualfund.jpg" , "rb")
        p = MIMEBase('application', 'octet-stream')
        # To change the payload into encoded form
        p.set_payload((attachment).read())
		# encode into base64
        encoders.encode_base64(p)
   
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
  
        # attach the instance 'p' to instance 'msg'
        msg.attach(p)
		
		# send the message via the server set up earlier.
        s.send_message(msg)
        
        del msg

if __name__ == '__main__':
    sendemail()
