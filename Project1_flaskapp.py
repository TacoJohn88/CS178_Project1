# author: Nathan Oelsner

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
import dbCode
import boto3
import creds
from dbCode import user_table


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
    

@app.route('/createuser', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        name = request.form['name']
        languages = request.form.getlist('languages')  # no '[]' in name!

        try:
            user_table.put_item(
                Item={
                    'Username': name,
                    'Languages': languages  # DynamoDB will store this as a list
                }
            )
            return redirect('/readuser')
        except Exception as e:
            return f"An error occurred while creating user: {e}"

    # Fetch distinct languages from RDS to populate the dropdown
    language_query = "SELECT DISTINCT Language FROM countrylanguage ORDER BY Language"
    language_data = dbCode.execute_query(language_query)
    languages = [row['Language'] for row in language_data]

    return render_template('createuser.html', languages=languages)



@app.route('/readuser')
def read_users():
    response = user_table.scan()
    users = response.get('Items', [])
    return render_template('readuser.html', users=users)


@app.route('/updateuser', methods=['GET', 'POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        selected_languages = request.form.getlist('languages')

        try:
            user_table.update_item(
                Key={'Username': name},
                UpdateExpression='SET Languages = :langs',
                ExpressionAttributeValues={':langs': selected_languages}
            )
            return redirect('/readuser')
        except Exception as e:
            return f"An error occurred while updating user: {e}"

    # Get language options from RDS
    try:
        all_languages = dbCode.execute_query("SELECT DISTINCT Language FROM countrylanguage ORDER BY Language")
        language_list = [lang['Language'] for lang in all_languages]
    except Exception as e:
        return f"An error occurred loading languages: {e}"

    return render_template('updateuser.html', languages=language_list)



@app.route('/deleteuser', methods=['GET', 'POST'])
def delete_user():
    if request.method == 'POST':
        name = request.form['Username']
        # Use 'Username' as the partition key here
        user_table.delete_item(Key={'Username': name})
        return redirect('/readuser')
    return render_template('deleteuser.html')



# these two lines of code should always be the last in the file
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
