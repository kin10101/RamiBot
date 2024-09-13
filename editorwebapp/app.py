from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Path to your intents.json file
INTENTS_FILE = 'intents.json'

def load_intents():
    """Load intents from the JSON file."""
    with open(INTENTS_FILE, 'r') as file:
        data = json.load(file)
        return data.get('intents', [])  # Access the nested 'intents' list

def save_intents(intents):
    """Save intents to the JSON file."""
    with open(INTENTS_FILE, 'w') as file:
        json.dump({"intents": intents}, file, indent=4)  # Save intents nested under 'intents'

@app.route('/')
def index():
    """Display the list of intents."""
    intents = load_intents()
    return render_template('index.html', intents=intents)

@app.route('/edit/<string:tag>', methods=['GET', 'POST'])
def edit_intent(tag):
    """Edit an existing intent or add a new one."""
    intents = load_intents()
    intent = next((i for i in intents if i['tag'] == tag), None)

    if request.method == 'POST':
        # Update or create the intent based on form input
        if intent:
            intent['patterns'] = request.form.getlist('patterns')
            intent['responses'] = request.form.getlist('responses')
        else:
            # If new intent, add it
            new_intent = {
                "tag": request.form['tag'],
                "patterns": request.form.getlist('patterns'),
                "responses": request.form.getlist('responses')
            }
            intents.append(new_intent)

        save_intents(intents)
        return redirect(url_for('index'))

    return render_template('edit.html', intent=intent, is_new=intent is None)

@app.route('/delete/<string:tag>', methods=['GET', 'POST'])
def delete_intent(tag):
    """Delete an existing intent."""
    intents = load_intents()
    intent = next((i for i in intents if i['tag'] == tag), None)

    if request.method == 'POST' and intent:
        intents.remove(intent)
        save_intents(intents)
        return redirect(url_for('index'))

    return render_template('delete.html', intent=intent)

@app.route('/add', methods=['GET', 'POST'])
def add_intent():
    """Add a new intent."""
    return redirect(url_for('edit_intent', tag=''))

if __name__ == '__main__':
    app.run(debug=True)
