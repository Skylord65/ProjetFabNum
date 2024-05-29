import os
import cv2
from picamera import PiCamera
from PIL import Image
import pytesseract
import time
import serial

# Configuration de la caméra
camera = PiCamera()
camera.resolution = (1280, 720)
camera.framerate = 30
camera.contrast = 10
camera.brightness = 60
camera.sharpness = 100
camera.ISO = 800

# Configuration du port série pour la communication avec l'Arduino
arduino = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
time.sleep(2)  # Attendre un peu pour que la connexion série soit établie

# Prend une photo avec la caméra après un délai de 3 secondes
def take_photo_with_delay(filename):
    camera.start_preview()
    time.sleep(3)
    camera.capture(filename)
    camera.stop_preview()

# Prétraitement de l'image pour améliorer la reconnaissance de texte
def preprocess_image(image_path):
    img = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    preprocessed_path = "preprocessed.png"
    cv2.imwrite(preprocessed_path, thresh)
    return preprocessed_path

# Reconnaissance de texte avec Tesseract OCR
def recognize_text(filename):
    preprocessed_image_path = preprocess_image(filename)
    img = Image.open(preprocessed_image_path)
    custom_config = r'--oem 3 --psm 6 -l fra'
    text = pytesseract.image_to_string(img, config=custom_config)
    return text

# Sauvegarde du texte extrait dans un fichier texte
def save_text_to_file(text, filename):
    with open(filename, 'w') as f:
        f.write(text)

# Main function
def main():
    while True:
        # Lire les données envoyées par l'Arduino
        if arduino.in_waiting > 0:
            line = arduino.readline().decode('utf-8').strip()
            if line == "ButtonPressed":
                # Définir le nom du fichier de la photo
                photo_filename = "photo.jpg"
                
                # Prendre une photo avec un délai de 3 secondes
                take_photo_with_delay(photo_filename)
                
                # Reconnaître le texte dans la photo
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
