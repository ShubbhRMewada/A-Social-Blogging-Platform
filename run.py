#This imports the package "flaskblog" which will by default execute the "__init__.py" file to initialize the package.
# The "app" is declared and initialized inside "__init__.py".
from flaskblog import app

#This will initialize the localhost and will run our website on "http://127.0.0.1:5000/"
if __name__ == "__main__":

    # debugger can be enabled on while production and development phase, will disabled during deployment.
    app.run()
