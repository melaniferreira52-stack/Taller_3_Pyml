from flask import Flask, request, jsonify, send_from_directory
import cv2
import numpy as np
import base64
import os

app = Flask(__name__, static_folder="../public")

# Cargar el clasificador de rostros (Haar Cascade)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")
face_classifier = cv2.CascadeClassifier(CASCADE_PATH)


@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(app.static_folder, path)


@app.route("/api/detect", methods=["POST"])
def detect_faces():
    if "image" not in request.files:
        return jsonify({"error": "No se proporcionó ninguna imagen"}), 400

    file = request.files["image"]

    try:
        filestr = file.read()
        npimg = np.frombuffer(filestr, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        if img is None:
            return jsonify({"error": "Formato de imagen inválido"}), 400

        output_img = img.copy()
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Se ajustan parámetros para mejorar la precisión de detección
        faces = face_classifier.detectMultiScale(
            gray_image, scaleFactor=1.1, minNeighbors=3, minSize=(20, 20)
        )

        for x, y, w, h in faces:
            cv2.rectangle(output_img, (x, y), (x + w, y + h), (0, 255, 0), 3)

        _, buffer = cv2.imencode(".jpg", output_img)
        encoded_image = base64.b64encode(buffer).decode("utf-8")

        return jsonify(
            {
                "success": True,
                "faces_detected": len(faces),
                "image": f"data:image/jpeg;base64,{encoded_image}",
            }
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500


app.debug = False