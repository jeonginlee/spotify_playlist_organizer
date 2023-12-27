from flask import Flask
import extensions
import controllers

import webbrowser

app = Flask(__name__)

app.register_blueprint(controllers.authorize, url_prefix='/authorize')
app.register_blueprint(controllers.dataBP, url_prefix='/data')
app.register_blueprint(controllers.services, url_prefix='/services')
app.register_blueprint(controllers.playlist, url_prefix='/playlist')
app.register_blueprint(controllers.main)

# Main deployment -------------------------------------------------------------
if __name__ == '__main__':
    webbrowser.open('http://localhost:3000/') # Make it easier for development

    print("Deploying Flask...")
    app.run(port=3000)
