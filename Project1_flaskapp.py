# author: Nathan Oelsner

from flask import Flask
from flask import render_template
import dbCode
import creds


app = Flask(__name__)
app.secret_key = 'your_secret_key' # this is an artifact for using flash displays; 
                                   # it is required, but you can leave this alone

db_config = {
    'host': creds.host,
    'user': creds.user,
    'password': creds.password,
    'database': creds.db
}

@app.route('/')
def home():
    return '<h1>Welcome to the Country Viewer</h1><p>Go to <a href="/countries">/countries</a> to see the list.</p>'


@app.route('/countries')
def countries():
    try:
        countries_list = dbCode.execute_query("SELECT Name, Population FROM country LIMIT 10")
        return render_template('countries.html', countries=countries_list)
    except Exception as e:
        return f"An error occurred: {e}"


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
