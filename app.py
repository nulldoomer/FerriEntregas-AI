# #############################################################################
# ######################### EASYOCR ###########################################
# #############################################################################
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
import easyocr
import re

app = FastAPI()

origins = [
    "http://localhost:8100",
    "capacitor://localhost",
    "ionic://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # o ["*"] para permitir todos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

reader = easyocr.Reader(["es"], gpu=True)


@app.post("/extract_text")
async def extract_text(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        np_array = np.frombuffer(contents, np.uint8)
        image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)

        if image is None:
            return {"error": "No se pudo decodificar la imagen"}

        image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        results = reader.readtext(image_gray)

        extracted_text = " ".join([text for _, text, _ in results])

        ci_pattern = r"CEDIRUC[:\s]*(\d{10})"
        found_ci = re.search(ci_pattern, extracted_text, re.IGNORECASE)

        vtotal_pattern = r"VALOR TOTAL USD[:\s]*(\d+\.\d+)"
        found_vtotal = re.search(vtotal_pattern, extracted_text, re.IGNORECASE)

        nfactura_pattern = r"FACTURA Nr.[:\s]*(\d+\-\d+\-\d+)"
        found_nfactura = re.search(nfactura_pattern, extracted_text, re.IGNORECASE)

        return {
            "text": extracted_text,
            "CI": found_ci.group(1) if found_ci else None,
            "valor_total": found_vtotal.group(1) if found_vtotal else None,
            "numero_factura": found_nfactura.group(1) if found_nfactura else None,
        }

    except Exception as e:
        return {"error": str(e)}


# #############################################################################
# ############################## PYTESSERACT ##################################
# #############################################################################
# from fastapi import FastAPI, File, UploadFile
# import cv2
# import pytesseract
# import numpy as np
# import os
#
# tesseract_path = os.path.join(
#     os.path.dirname(__file__), ".venv", "Tesseract", "tesseract.exe"
# )
#
# pytesseract.pytesseract.tesseract_cmd = tesseract_path
#
# app = FastAPI()
#
#
# @app.post("/extract_text")
# async def extract_text(file: UploadFile = File(...)):
#     contents = await file.read()
#     np_array = np.frombuffer(contents, np.uint8)
#     image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
#
#     gray_scale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#
#     thresh = cv2.adaptiveThreshold(
#         gray_scale, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 2
#     )
#
#     custom_config = r"--oem 3 --psm 6 -l spa"
#     text = pytesseract.image_to_string(thresh, config=custom_config)
#
#     return {"text": text}
#


# #############################################################################
# ####################### KERAS_OCR ###########################################
# #############################################################################
# from fastapi import FastAPI, File, UploadFile
# import cv2
# import numpy as np
# import keras_ocr
#
#
# app = FastAPI()
#
# pipeline = keras_ocr.pipeline.Pipeline()
#
#
# @app.post("/extract_text")
# async def extract_text(
#     file: UploadFile = File(...),
# ):
#     try:
#         contents = await file.read()
#         np_array = np.frombuffer(contents, np.uint8)
#         image = cv2.imdecode(np_array, cv2.IMREAD_COLOR)
#
#         if image is None:
#             return {"error": "No se pudo decodificar la imagen"}
#
#         # Convertir la imagen a RGB porque keras-ocr trabaja con imágenes en este formato
#         image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#
#         # Ejecutar el pipeline de OCR
#         predictions = pipeline.recognize([image_rgb])
#
#         # Extraer el texto detectado
#         extracted_text = [word for word, _ in predictions[0]]
#
#         return {"text": " ".join(extracted_text)}
#
#     except Exception as e:
#         return {"error": str(e)}

# #############################################################################
