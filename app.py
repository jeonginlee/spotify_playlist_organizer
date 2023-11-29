from flask import Flask
import controllers

app = Flask(__name__)

app.register_blueprint(controllers.authorize, url_prefix='/authorize')
app.register_blueprint(controllers.dataBP, url_prefix='/data')
app.register_blueprint(controllers.services, url_prefix='/services')

# Main deployment -------------------------------------------------------------
if __name__ == '__main__':
    print("Deploying Flask...")
    app.run(port=3000)
