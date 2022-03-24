# coding=utf-8

# import libraries for sending an email
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

'''
Function to send emails
email_to: list of emails to sendt it to
subject: subject string of email
attachment: string file path to file to send
'''
def sendEmail(email_to, subject, calculation_string):


    # Send email Configuration
    emailfrom = "htmbot2@gmail.com"
    emailto = email_to
    #fileToSend = month+year+"_payment_times_report.csv"
    username = "htmbot2@gmail.com"
    password = "PASSWORDHERE"

    # Send email configuration
    msg = MIMEMultipart()
    msg["From"] = emailfrom
    msg["To"] = ", ".join(emailto)
    msg["Subject"] = subject
    # fileToSend = file_attachment
    msg.preamble = "HTM-bot"

    # ctype, encoding = mimetypes.guess_type(fileToSend)
    # if ctype is None or encoding is not None:
    #     ctype = "application/octet-stream"
    #
    # maintype, subtype = ctype.split("/", 1)

    # if maintype == "text":
    #     fp = open(fileToSend)
    #     # Note: we should handle calculating the charset
    #     attachment = MIMEText(fp.read(), _subtype=subtype)
    #     fp.close()
    # elif maintype == "image":
    #     fp = open(fileToSend, "rb")
    #     attachment = MIMEImage(fp.read(), _subtype=subtype)
    #     fp.close()
    # elif maintype == "audio":
    #     fp = open(fileToSend, "rb")
    #     attachment = MIMEAudio(fp.read(), _subtype=subtype)
    #     fp.close()
    # else:
    #     fp = open(fileToSend, "rb")
    #     attachment = MIMEBase(maintype, subtype)
    #     attachment.set_payload(fp.read())
    #     fp.close()
    #     encoders.encode_base64(attachment)
    # attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
    # msg.attach(attachment)

    # Create the body of the message (a plain-text and an HTML version).
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttps://www.python.org" # plain text attachment
    # part1 = MIMEText(text, 'plain')
    html = "<html><head></head><body> </div>" +  calculation_string   + "</div>  </body></html>"

    # Record the MIME types of both parts - text/plain and text/html.

    part2 = MIMEText(html, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    # msg.attach(part1)
    msg.attach(part2)

    server = smtplib.SMTP("smtp.gmail.com:587")
    server.starttls()
    server.login(username,password)
    server.sendmail(emailfrom, emailto, msg.as_string())
    server.quit()

