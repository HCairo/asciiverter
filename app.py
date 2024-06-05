# Importation des modules nécessaires
from flask import Flask, request, render_template, send_file
from flask_cors import CORS   # Import the CORS module
from PIL import Image
import os

# Initialisation de l'application Flask
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Liste des caractères ASCII utilisés pour générer l'art ASCII
ASCII_CHARS = ["@", "#", "S", "%", "?", "*", "+", ";", ":", ",", "."]

# Fonction pour redimensionner l'image à une nouvelle largeur
def resize_img(image, new_width=100):
    width, height = image.size
    ratio = height / width / 1.65
    new_height = int(new_width * ratio)
    resized_image = image.resize((new_width, new_height))
    return resized_image

# Fonction pour convertir l'image en niveaux de gris
def grayifi(image):
    grayscale_image = image.convert("L")
    return grayscale_image

# Fonction pour convertir les pixels de l'image en caractères ASCII
def pixels_to_ascii(image):
    pixels = image.getdata()
    characters = "".join([ASCII_CHARS[pixel // 25] for pixel in pixels])
    return characters

# Fonction principale pour convertir une image en art ASCII
def image_to_ascii(path, new_width=100):
    try:
        image = Image.open(path)
    except Exception as e:
        return ""
    new_img_data = pixels_to_ascii(grayifi(resize_img(image)))
    pixel_count = len(new_img_data)
    ascii_img = "\n".join(new_img_data[i:(i + new_width)] for i in range(0, pixel_count, new_width))
    return ascii_img

# Route pour la page d'accueil qui affiche le formulaire de téléchargement
@app.route('/')
def index():
    return render_template('index.html')

# Route pour gérer le téléchargement et la conversion de l'image
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)
        ascii_art = image_to_ascii(file_path)
        os.remove(file_path)
        return render_template('result.html', ascii_art=ascii_art)

# Lancement de l'application Flask
if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)