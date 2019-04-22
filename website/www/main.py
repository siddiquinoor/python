r"""
    - Python web can run in it's own Virtual HTTP server and can have needed python library within project in a virtual directory
        -- First install it
            pip install virtualenv
        -- Then install virtual environment
            python -m venv virtual
    - Installing the web development framework for Python
        pip install flask
    - Heroku need gunicorn http server so, Installing gunicorn
        pip install gunicorn
    - Generating a requirements.txt file
        virtual\Scripts\pip freeze > requirements.txt
    - Uploading website into Heroku
        -- Lets first create a .git repository in local drive
            git init
            git add .
            git commit -m 'Commit message'
        -- Now point to the Heroku app
            heroku login
            heroku create siddiquinoor #app name siddiquinoor
            heroku git:remote --app siddiquinoor
            git push heroku master

"""

from flask import Flask, render_template

app=Flask(__name__)

@app.route('/')
def home():
    return render_template("home.html")


@app.route('/about/')
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
