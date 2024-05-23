import os
from picamera import PiCamera
from PIL import Image
import pytesseract
import time

# Configuration de la caméra
camera = PiCamera()

# Ajustements des paramètres pour une meilleure qualité d'image
camera.resolution = (1280, 720)  # Résolution HD
camera.framerate = 30  # Taux de trame
camera.contrast = 10  # Ajustement du contraste (0 à 100)
camera.brightness = 60  # Ajustement de la luminosité (0 à 100)
camera.sharpness = 100  # Ajustement de la netteté (0 à 100)
camera.ISO = 800  # Ajustement de l'ISO pour une meilleure sensibilité à la lumière

# Prend une photo avec la caméra après un délai de 3 secondes
def take_photo_with_delay(filename):
    camera.start_preview()
    # Pause de 3 secondes pour permettre à l'utilisateur de placer la caméra
    time.sleep(3)
    camera.capture(filename)
    camera.stop_preview()

# Reconnaissance de texte avec Tesseract OCR
def recognize_text(filename):
    img = Image.open(filename)
    text = pytesseract.image_to_string(img)
    return text

# Sauvegarde du texte extrait dans un fichier texte
def save_text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

# Main function
def main():
    # Définir le nom du fichier de la photo
    photo_filename = "photo.jpg"
    
    # Prend une photo avec un délai de 3 secondes
    take_photo_with_delay(photo_filename)
    
    # Reconnaît le texte dans la photo
    text = recognize_text(photo_filename)

    # Si le texte est vide, afficher "Le texte de l'image est introuvable ou illisible"
    if text.strip() == "":
        print("Le texte de l'image est introuvable ou illisible")
    else:
        # Afficher le texte extrait dans le terminal
        print("Texte extrait de l'image :\n")
        print(text)
        
    # Enregistrer le texte extrait dans un fichier texte
    text_file = "extracted_text.txt"
    save_text_to_file(text, text_file)
    print(f"Texte extrait enregistré dans {text_file}")

if __name__ == "__main__":
    main()
