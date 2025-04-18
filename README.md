# Country Viewer + User Language Tracker

## Project Summary

This Flask-based web application allows users to view information about countries and the languages spoken in each one. It connects to an AWS RDS MySQL database to retrieve country and language data, and to a DynamoDB table to store user-specific language preferences. Users can perform full CRUD operations on the `UserLanguages` table: create new users with selected languages, view all users, update user language preferences, and delete users.

Key features:
- Displays country data with associated languages.
- Allows user creation with select language input.
- Supports updating and deleting user language preferences.
- Language options are pulled dynamically from RDS and sorted alphabetically.
- User language data is stored in DynamoDB.

## Technologies Used

- **Python**
- **Flask**
- **HTML/Jinja2** (for templates)
- **AWS RDS (MySQL)**
- **AWS DynamoDB**
- **boto3** (for DynamoDB integration)
- **PyMySQL** (for RDS MySQL connection)

## Setup and Run Instructions

1. **Clone the repository**

   ```
   bash
   git clone https://github.com/yourusername/project1-country-viewer.git
   cd project1-country-viewer
   ```

2. **Install required libraries**

    ```
    pip install flask pymysql boto3
    ```

3. **Add your database credentials**

    ```
    host = 'your-rds-endpoint'
    user = 'your-rds-username'
    password = 'your-rds-password'
    db = 'world'
    ```

4. **AWS DynamoDB setup**

    Ensure you have a DynamoDB table named UserLanguages with the following:

    **Partition key:** Username (Type: String)

    **Attribute: Languages** (Type: List of Strings)

    You also need to have AWS credentials configured (via environment, AWS CLI, or IAM role) that allow access to this table.

5. **Run the flask application**

    In your terminal:

    ```
    python Project1_flaskapp.py
    ```

    Then open your browser and go to:

    ```
    http://localhost:8080/
    ```

## App Navigation

- **/ – Welcome page**

- **/countries – View all countries and their associated languages**

- **/createuser – Create a new user and select a language**

- **/readuser – View all users and their selected language**

- **/updateuser – Update a user’s language preference**

- **/deleteuser – Delete a user by name**