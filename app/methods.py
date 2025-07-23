import cv2
import os
import numpy as np

image_path = "qr_yape.jpg"

if not os.path.exists(image_path):
    print(f"⚠️ La imagen no se encuentra: {image_path}")
else:
    image = cv2.imread(image_path)
    if image is None:
        print("⚠️ No se pudo leer la imagen")
    else:
        qrDetector = cv2.QRCodeDetector()
        data, bbox, rectifiedImage = qrDetector.detectAndDecode(image)

        if data:
            print("📤 QR original:", data)

            # Reemplaza o inserta el monto fijo de 5.00
            import re
            if re.search(r'54\d{2}\d+\.\d{2}', data):
                # Ya tiene monto, reemplazamos
                new_data = re.sub(r'54\d{2}\d+\.\d{2}', '54045.00', data)
            else:
                # No tiene, insertamos antes del campo 58 (que es el país)
                new_data = re.sub(r'(58\d{2})', r'54045.00\1', data)

            print("✅ QR con monto fijo S/5.00:", new_data)
        else:
            print("⚠️ No se detectó ningún QR válido.")
            
            
import crcmod
import qrcode


# Payload base sin checksum
payload_base = (
    "000201"
    "010211"
    "3932d9495b0249855c4f9d363be4d0bd55975"
    "204561153036"
    "0454045.00"
    "5802PE"
    "5906YAPERO"
    "6004Lima"
    "6304"  # Aquí va el checksum después
)

# Calcular checksum CRC16-CCITT (False, False)
crc16 = crcmod.predefined.mkPredefinedCrcFun('crc-ccitt-false')
checksum = format(crc16(payload_base.encode('utf-8')), '04X')

# Payload final
payload_final = payload_base + checksum
print("🔐 Payload final:", payload_final)

# Generar el QR
qr = qrcode.make(payload_final)
qr.save("qr_yape_con_monto.png")
print("✅ QR generado con monto fijo S/ 5.00 y guardado como 'qr_yape_con_monto.png'")