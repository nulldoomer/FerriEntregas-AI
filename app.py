from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
import keras_ocr


app = FastAPI()

pipeline = keras_ocr.pipeline.Pipeline()


@app.post("/extract_text")
async def extract_text(
    file: UploadFile = File(...),
):
    try:
        contents = await file.read()
        np_array = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            return {"error": "No se pudo decodificar la imagen"}

        # Convertir la imagen a RGB porque keras-ocr trabaja con imágenes en este formato
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Ejecutar el pipeline de OCR
        predictions = pipeline.recognize([image_rgb])

        # Extraer el texto detectado
        extracted_text = [word for word, _ in predictions[0]]

        return {"text": " ".join(extracted_text)}

    except Exception as e:
        return {"error": str(e)}
