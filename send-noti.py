import smtplib
server = smtplib.SMTP('smtp.gmail.com', 465)
server.starttls()
server.login('jenkins.noti.mail@gmail.com',"mtaeykdhgtfwagzu")
mail_body = "Jenkins-notification"
server.sendmail('jenkins.noti.mail@gmail.com','jenkins.noti.mail@gmail.com',mail_body)



