import cv2
import numpy as np
from pathlib import Path

# Ruta de prueba (ajústala a tu acta)
RUTA_IMAGEN = r"ACTAS\BOLIVIA\Beni\Cercado\San Javier\La Curva\U.E. La Curva\mesa_1_8004231.jpg"

def imread_unicode(path: str):
    """Lectura robusta para rutas con tildes o espacios"""
    path = Path(path)
    data = np.fromfile(str(path), dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

def order_points(pts):
    """Ordena los 4 puntos en orden TL, TR, BR, BL"""
    rect = np.zeros((4, 2), dtype="float32")
    s = pts.sum(axis=1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis=1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    rect = order_points(pts)
    (tl, tr, br, bl) = rect

    widthA = np.linalg.norm(br - bl)
    widthB = np.linalg.norm(tr - tl)
    maxWidth = int(max(widthA, widthB))

    heightA = np.linalg.norm(tr - br)
    heightB = np.linalg.norm(tl - bl)
    maxHeight = int(max(heightA, heightB))

    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")

    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def detectar_marco(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5,5), 0)
    edges = cv2.Canny(blur, 75, 200)

    cnts, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not cnts:
        return None, edges

    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    h, w = img.shape[:2]
    area_img = h * w

    for c in cnts[:5]:
        peri = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.02*peri, True)

        if len(approx) == 4:
            area = cv2.contourArea(approx)
            aspect_ratio = max(w,h)/min(w,h)
            approx_w = np.linalg.norm(approx[0][0] - approx[1][0])
            approx_h = np.linalg.norm(approx[1][0] - approx[2][0])
            if area > 0.5*area_img:  # al menos la mitad del área
                return approx.reshape(4,2), edges

    # Fallback: caja rotada
    rect = cv2.minAreaRect(cnts[0])
    box = cv2.boxPoints(rect)
    box = np.int8(box)
    return box, edges

def main():
    img = imread_unicode(RUTA_IMAGEN)
    if img is None:
        print("⚠️ No se pudo cargar la imagen")
        return

    quad, edges = detectar_marco(img)
    if quad is None:
        print("⚠️ No se detectó el marco")
        return

    # Dibujar el marco en la original
    debug = img.copy()
    cv2.drawContours(debug, [quad.astype(int)], -1, (0,255,0), 3)

    # Recortar y enderezar
    acta = four_point_transform(img, quad)

    # Mostrar resultados
    cv2.imshow("Original", img)
    cv2.imshow("Bordes", edges)
    cv2.imshow("Marco Detectado", debug)
    cv2.imshow("Acta Recortada", acta)

    cv2.imwrite("acta_debug.jpg", debug)
    cv2.imwrite("acta_recortada.jpg", acta)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
