import datetime
from flask import Flask, send_file, request, jsonify, render_template, redirect, url_for, Blueprint
import os
import subprocess
import chatbot
import sql_module
import json
from api_routes import api_routes

# if nothing is being encoded onto the audio file, try pip install piper-tts.

app = Flask(__name__)
app.secret_key = 'secret'
app.register_blueprint(api_routes)

# Image directory path
image_directory = 'Image_Infos/'
# Model path
MODEL_PATH = "Voices/en_US-lessac-low.onnx"
INTENTS_FILE = 'Model/intents.json'


def load_intents():
    """Load intents from the JSON file."""
    with open(INTENTS_FILE, 'r') as file:
        data = json.load(file)
        return data.get('intents', [])  # Access the nested 'intents' list


def save_intents(intents):
    """Save intents to the JSON file."""
    with open(INTENTS_FILE, 'w') as file:
        json.dump({"intents": intents}, file, indent=4)


def log_last_modified_date_and_username(intent_tag, username='admin'):
    """Update the last_modified_date and last_modified_by of the given intent."""
    intents = load_intents()

    for intent in intents:
        print(intent)
        if intent['tag'] == intent_tag:
            print("found intent")
            print(f"Updated 'last_modified_date' and 'last_modified_by' for intent '{intent_tag}'")
            break

    save_intents(intents)

@app.route('/')
def index():
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        pass


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    elif request.method == 'POST':
        pass


@app.route('/home')
def home():
    return render_template('home.html', active_page='home')


@app.route('/upload_images')
def upload_images():
    return render_template('upload_images.html', active_page='upload_images')


@app.route('/conversation_history')
def conversation_history():
    # Get table, sort order, rows per page, and current page from the request arguments
    selected_table = request.args.get('table', 'chatbot_results')
    sort_by = request.args.get('sortBy', 'date_desc')
    rows_per_page = int(request.args.get('rowsPerPage', 10))  # Default to 10 rows per page
    current_page = int(request.args.get('page', 1))  # Default to page 1

    # Determine the sort order
    order_by = "ORDER BY query_date DESC" if sort_by == 'date_desc' else "ORDER BY query_date ASC"

    # Validate the selected table
    if selected_table not in ['chatbot_results', 'voicebot_results']:
        selected_table = 'chatbot_results'

    # Calculate the offset for pagination
    offset = (current_page - 1) * rows_per_page

    # Fetch the total number of rows to calculate the number of pages
    total_query = f"SELECT COUNT(*) as total_count FROM {selected_table}"

    # Execute the query and handle potential errors
    total_result = sql_module.sql_query(total_query)

    if total_result is None or len(total_result) == 0:
        total_rows = 0  # Default to 0 if the query failed
    else:
        total_rows = total_result[0]['total_count']  # Access the count using dictionary key

    # Calculate total pages and ensure at least 1 page exists
    total_pages = max((total_rows + rows_per_page - 1) // rows_per_page, 1)



    # Adjust the query based on the selected table
    if selected_table == 'chatbot_results':
        query = f"""
            SELECT query_id, intent_recognized, confidence_score, received_text, bot_response, 
                   response_time, query_time, query_date 
            FROM {selected_table} 
            {order_by} 
            LIMIT {rows_per_page} OFFSET {offset}
        """
    elif selected_table == 'voicebot_results':
        query = f"""
            SELECT query_id, intent_recognized, confidence_score, transcribed_text AS received_text, bot_response, 
                   response_time, query_time, query_date 
            FROM {selected_table} 
            {order_by} 
            LIMIT {rows_per_page} OFFSET {offset}
        """

    # Fetch the paginated results from the database

    results = sql_module.sql_query(query)

    if results is None:
        results = []  # Handle case where no results are returned

    # Render the template with pagination, row limits, and sorting
    return render_template(
        'conversation_history.html',
        active_page='conversation_history',
        conversations=results,
        sort_order=sort_by,
        table=selected_table,
        rows_per_page=rows_per_page,
        current_page=current_page,
        total_pages=total_pages
    )


@app.route('/modify_intents')
def modify_intents():
    intents = load_intents()
    return render_template('modify_intents.html', active_page='modify_intents', intents=intents)

@app.route('/edit_buttons')
def edit_buttons():
    return render_template('edit_buttons.html', active_page='edit_buttons')



# Update the edit_intents function
@app.route('/edit_intents/<string:tag>', methods=['GET', 'POST'])
def edit_intents(tag):
    intents = load_intents()
    intent = next((i for i in intents if i['tag'] == tag), None)

    if request.method == 'POST':
        if intent:
            intent['last_modified_by'] = request.form['last_modified_by']
            intent['last_modified_date'] = request.form['last_modified_date']
            intent['patterns'] = request.form.getlist('patterns')
            intent['responses'] = request.form.getlist('responses')
            log_last_modified_date_and_username(intent['tag'])
        else:
            new_intent = {
                "last_modified_by": request.form['last_modified_by'],
                "last_modified_date": request.form.get('last_modified_date'),
                "tag": request.form['tag'],
                "patterns": request.form.getlist('patterns'),
                "responses": request.form.getlist('responses')
            }
            intents.append(new_intent)
            log_last_modified_date_and_username(new_intent['tag'])

        save_intents(intents)
        return redirect(url_for('modify_intents'))

    return render_template('intent_form.html', intent=intent, is_new=intent is None)

@app.route('/delete_intents/<string:tag>', methods=['POST'])
def delete_intents(tag):
    """Delete an existing intent and redirect to the Modify Intents page."""
    intents = load_intents()
    intent = next((i for i in intents if i['tag'] == tag), None)

    if intent:
        intents.remove(intent)  # Remove the selected intent
        save_intents(intents)  # Save the updated list

    return redirect(url_for('modify_intents'))


@app.route('/add_intents', methods=['GET', 'POST'])
def add_intent():
    """Add a new intent."""
    return redirect(url_for('edit_intents', tag='new_intent'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5050)
