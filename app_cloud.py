from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage
import json
from uuid import uuid4
import os

app = Flask(__name__)

# Configurations
LOCAL_JSON_FILE = 'notes.json'
BUCKET_NAME = os.getenv("BUCKET")


if BUCKET_NAME == None :
	print("LA VARIABLE EST VIDE !!!!!!")
	exit()



# Gestion des notes locales
def load_notes():
    """Charge les notes depuis le fichier JSON local."""
    try:
        with open(LOCAL_JSON_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_notes(notes):
    """Sauvegarde les notes dans le fichier JSON local."""
    with open(LOCAL_JSON_FILE, 'w') as file:
        json.dump(notes, file, indent=4)

# Gestion des notes dans le bucket
def get_storage_client():
    """Initialise le client Google Cloud Storage."""
    return storage.Client()

def list_notes_from_bucket():
    """Récupère les notes depuis le bucket Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blobs = bucket.list_blobs()
    notes = []
    for blob in blobs:
        content = blob.download_as_text()
        note = json.loads(content)
        notes.append(note)

    return notes

def save_note_to_bucket(note):
    """Enregistre une note dans le bucket Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    note_id = str(uuid4())  # Génère un ID unique pour chaque note
    blob = bucket.blob(f"{note_id}.json")
    blob.upload_from_string(json.dumps(note), content_type='application/json')

# Routes Flask
@app.route('/')
def index():
    """Affiche la liste des notes."""
    # Changez `list_notes_from_bucket` par `load_notes` si vous voulez des notes locales
    notes = list_notes_from_bucket()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=('GET', 'POST'))
def add_note():
    """Ajoute une nouvelle note."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = {"id": str(uuid4()), "title": title, "content": content}
        # Changez `save_note_to_bucket` par `save_note` pour sauvegarder localement
        save_note_to_bucket(note)
        return redirect(url_for('index'))
    return render_template('add_note.html')

@app.route('/delete/<note_id>', methods=['POST'])
def delete(note_id):
    """Supprime une note."""
    # Fonction à implémenter pour supprimer une note dans le bucket si nécessaire.
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
