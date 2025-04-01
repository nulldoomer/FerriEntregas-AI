from fastapi import FastAPI, File, UploadFile, HTTPException
import cv2
import numpy as np
import keras_ocr

app = FastAPI()

# Inicializar el pipeline una sola vez
pipeline = keras_ocr.pipeline.Pipeline()


@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        # Leer los bytes de la imagen
        contents = await file.read()
        np_array = np.frombuffer(contents, np.uint8)

        # Decodificar la imagen
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
        if image is None:
            raise HTTPException(
                status_code=400,
                detail="Archivo inválido. No se pudo decodificar como imagen.",
            )

        # Convertir la imagen a RGB para keras-ocr
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Ejecutar OCR
        predictions = pipeline.recognize([image_rgb])

        # Extraer texto
        extracted_text = [word for word, _ in predictions[0]]

        return {"text": " ".join(extracted_text)}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error procesando la imagen: {str(e)}"
        )
