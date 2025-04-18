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

   ```bash
   git clone https://github.com/yourusername/project1-country-viewer.git
   cd project1-country-viewer
