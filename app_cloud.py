from flask import Flask, render_template, request, redirect, url_for
from google.cloud import storage
import json
from uuid import uuid4
import os

app = Flask(__name__)

# Configurations
LOCAL_JSON_FILE = 'notes.json'
BUCKET_NAME = os.getenv("BUCKET")

print(f"BUCKET_NAME: '{BUCKET_NAME}'")

if BUCKET_NAME is None:
    print("LA VARIABLE BUCKET EST VIDE !!!!!!")
    exit()

# Gestion des notes locales
def ensure_local_file():
    """Vérifie si le fichier local existe, sinon le crée avec une liste vide."""
    if not os.path.exists(LOCAL_JSON_FILE):
        with open(LOCAL_JSON_FILE, 'w') as file:
            json.dump([], file)
        print(f"{LOCAL_JSON_FILE} créé avec une liste vide.")

def load_notes():
    """Charge les notes depuis le fichier JSON local."""
    ensure_local_file()
    with open(LOCAL_JSON_FILE, 'r') as file:
        return json.load(file)

def save_notes(notes):
    """Sauvegarde les notes dans le fichier JSON local."""
    with open(LOCAL_JSON_FILE, 'w') as file:
        json.dump(notes, file, indent=4)

# Gestion des notes dans le bucket
def get_storage_client():
    """Initialise le client Google Cloud Storage."""
    return storage.Client()

def ensure_bucket_file():
    """Vérifie si le fichier JSON existe dans le bucket, sinon l'initialise."""
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(LOCAL_JSON_FILE)

    if not blob.exists():
        ensure_local_file()
        blob.upload_from_filename(LOCAL_JSON_FILE, content_type='application/json')
        print(f"Fichier {LOCAL_JSON_FILE} créé et uploadé dans le bucket.")

def list_notes_from_bucket():
    """Récupère les notes depuis le bucket Google Cloud Storage."""
    ensure_bucket_file()
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(LOCAL_JSON_FILE)

    content = blob.download_as_text()
    return json.loads(content) if content else []

def save_notes_to_bucket(notes):
    """Enregistre les notes dans le bucket Google Cloud Storage."""
    client = get_storage_client()
    bucket = client.bucket(BUCKET_NAME)
    blob = bucket.blob(LOCAL_JSON_FILE)
    blob.upload_from_string(json.dumps(notes, indent=4), content_type='application/json')

@app.route('/')
def index():
    """Affiche la liste des notes."""
    notes = list_notes_from_bucket()
    return render_template('index.html', notes=notes)

@app.route('/add', methods=('GET', 'POST'))
def add_note():
    """Ajoute une nouvelle note."""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        note = {"id": str(uuid4()), "title": title, "content": content}

        notes = list_notes_from_bucket()
        notes.append(note)
        save_notes_to_bucket(notes)

        return redirect(url_for('index'))
    return render_template('add_note.html')

@app.route('/delete/<note_id>', methods=['POST'])
def delete(note_id):
    """Supprime une note du bucket."""
    notes = list_notes_from_bucket()
    notes = [note for note in notes if note["id"] != note_id]
    save_notes_to_bucket(notes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)

