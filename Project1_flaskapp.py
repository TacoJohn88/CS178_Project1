# author: Nathan Oelsner

from flask import Flask
from flask import render_template
from flask import request
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
    return ('<h1>Welcome to the Country Viewer</h1>'
    '<p>Go to <a href="/countries">/countries</a> to see the list.</p>'
    )

@app.route('/countries')
def countries():
    try:
        all_countries = dbCode.execute_query("""
                                             SELECT 
                                                country.Name, 
                                                country.Continent, 
                                                country.Region, 
                                                country.Population, 
                                                GROUP_CONCAT(countrylanguage.Language SEPARATOR ', ') AS Languages
                                             FROM country 
                                             JOIN countrylanguage WHERE country.code = countrylanguage.countrycode 
                                             GROUP BY country.Code, country.Name, country.Continent, country.Region, country.Population""")
        return render_template('countries.html', countries=all_countries)
    except Exception as e:
        return f"An error occurred: {e}"
    

@app.route('/popsearch', methods=['GET'])
def show_pop_form():
    return render_template('popsearch.html')


@app.route('/largepop', methods=['POST'])
def popsearch():
    try:
        pop = request.form.get('pop', type=int)

        if pop is None:
            return "Invalid population input."

        query = "SELECT * FROM country WHERE Population >= %s ORDER BY Population DESC"
        largepop = dbCode.execute_query(query, (pop,))

        return render_template('largepop.html', countries=largepop, pop=pop)

    except Exception as e:
        return f"An error occurred: {e}"


# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
