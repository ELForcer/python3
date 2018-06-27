########################################################################
## Модуль отправки письма через Python3
## Автор: ELForcer
## Версия: 0.2
## Возможности:
## - Отправка письма через SMTP SSL
## - Отправка вложения (если есть)
########################################################################

#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import cgi #основной модуль 
import datetime #Дата и время
import os
import base64  #Модул кодирования в Base64

# Работа с почтой
import smtplib 
from smtplib import SMTP_SSL 
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders

#Загружаем PNG-файл для логотипа (справа)
def GetLogo():
	F = open("Logo.png", "rb").read()  
    Base64= base64.standard_b64encode(F)
	return str(Base64.decode("utf-8"))

def StartHTML(Title):
	Text = "<html><title>" + Title + """</title><meta http-equiv="Content-Type" content="text/html; charset=windows-1251"><meta http-equiv="Content-Language" content="ru">"""
	return Text
 
#Модуль отправки файла
def send_email(Mail_To,Subject,EMailText,AttachFileName):
	today = datetime.datetime.today() #текущая дата и время
	HTMLDateTime= today.strftime("%d.%m.%Y %H:%M:%S") #Преобразуем текущую дату и время в человеческий вид
	
	Mail_From="***-b@ya.ru" #Логин и наша почта
	password = '***' #Пароль 
	mail_adr = 'smtp.yandex.ru' #SMTP-сервер
	mail_port = 465 #SSL
	
	# Создаем  заголовки
	msg = MIMEMultipart() 
	msg.add_header('Content-type', 'text/html charset=utf-8')  #Добавляем заголовок, говорим что у нас HTML-страничка
	msg['From'] =  "Бэкапер <"+Mail_From+">" #От кого (от нас)
	msg['To'] = Mail_To #Кому
	msg['Subject'] = Subject #Тема
	
	# Добавление вложения
	if (AttachFileName!="" and os.path.isfile(AttachFileName)==True):
		part = MIMEBase('application', "octet-stream")
		part.set_payload(open(AttachFileName, "rb").read())
		encoders.encode_base64(part)
		part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(AttachFileName))
		msg.attach(part)	
	
	# Текстовая часть сообщения
	#---------------------------------------------------------------------------------------------------
	msgAlternative = MIMEMultipart('alternative')
	msg.attach(msgAlternative)
	
	# присоединяем HTML
	#----------------------------------------------------------------------------------------------------
	# Добавление текста сообщения
	HTMLmsg = StartHTML("Бэкапер на Python") + "<body>" + """<table border = 0 width = 100% height=20><tr> <td>
<img src ="data:image/png;base64,"""+GetLogo()+"""" align=right width=256>
<h1>""" + Subject + """</h1> </td></tr></table>""" + EMailText + """
<hr>
<table border=0 width=100%>
<tr><td align=left><b>Дата сообщения:</b> <br>"""+HTMLDateTime+"""</td> <td></td><td align=right><br></td></tr></table></body></html>"""

	to_attach = MIMEText(HTMLmsg,"html","UTF-8") #Присоединяем HTML 
	msgAlternative.attach(to_attach) #к телу письма
	 
	# Непосредственная отправка почты
	smtp = SMTP_SSL() #Создаем ЗАЩИЩЕННОЕ подключение
	smtp.set_debuglevel(1) #Уровень журанирования. 
	smtp.connect(mail_adr, mail_port) #Подключаемся
	smtp.login(Mail_From, password) #Авторизуемся
	smtp.sendmail(Mail_From, Mail_To, msg.as_string()) #Передаем письмо
	smtp.quit() #Отключаемся
	print("Письмо успешно отправлено!")

########################################################################
## Точка входа в программу
########################################################################
#send_email( "***@yandex.ru", "Test", "This test text! <b>See you!</b>",'')

