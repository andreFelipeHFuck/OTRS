import numpy as np
import os
import cv2
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"/usr/bin/tesseract"
os.environ["TESSDATA_PREFIX"] = "/usr/share/tessdata/"

debug = True


def show_image(image, window_name="image"):
    if debug:
        cv2.imshow(window_name, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    else:
        pass


# Função para calcular porcentagem de pixels pretos em um quadrante
def calculate_black_pixel_percentage(image, x1, y1, x2, y2, qx):
    quadrant = image[y1:y2, x1:x2]
    show_image(quadrant, f"Quadrante {qx + 1}")

    total_pixels = quadrant.size

    white_pixel_count = cv2.countNonZero(quadrant)
    black_pixels_count = total_pixels - white_pixel_count

    return (black_pixels_count / total_pixels) * 100


def process_image_manometro(image_path):
    img = cv2.imread(image_path)

    show_image(img, "Original")

    # Convertendo para escala de cinza
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    show_image(gray, "Cinza")

    # Aplicando CLAHE para melhorar o contraste
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    enhanced_img = clahe.apply(gray)

    show_image(enhanced_img, "CLAHE")

    # Aplicando blur para suavizar a imagem
    blurred = cv2.GaussianBlur(enhanced_img, (9, 9), 2)

    # Utilizando a Transformada de Hough para detectar círculos
    circles = cv2.HoughCircles(
        blurred,
        cv2.HOUGH_GRADIENT,
        dp=1.2,
        minDist=100,
        param1=100,
        param2=30,
        minRadius=50,
        maxRadius=150,
    )

    if circles is None:
        print("Nenhum círculo encontrado.")
        return

    circles = np.round(circles[0, :]).astype("int")
    for c_x, c_y, radius in circles:
        cv2.circle(img, (c_x, c_y), radius, (0, 255, 0), 4)
        cv2.rectangle(img, (c_x - 5, c_y - 5), (c_x + 5, c_y + 5), (0, 128, 255), -1)

    show_image(img, "Circulo Encontrado")

    # Definindo a região de interesse
    x1, y1 = max(0, c_x - radius), max(0, c_y - radius)
    x2, y2 = min(gray.shape[1], c_x + radius), min(gray.shape[0], c_y + radius)

    if x1 >= x2 or y1 >= y2:
        print("Coordenadas de recorte inválidas.")
        return

    crop_image = gray[y1:y2, x1:x2]

    if crop_image.size == 0:
        print("A imagem recortada está vazia.")
        return

    show_image(crop_image, "Imagem Recortada")

    # Aplicando filtro gaussiano
    gaussian_blurred_image = cv2.GaussianBlur(crop_image, (5, 5), 0)

    # Thresholding para binarização
    _, gaussian_thresh_image = cv2.threshold(
        gaussian_blurred_image, 107, 255, cv2.THRESH_BINARY
    )

    show_image(gaussian_thresh_image, "Imagem Binaria")

    # Rotacionando a imagem
    (h, w) = gaussian_thresh_image.shape[:2]
    center = (w // 2, h // 2)
    angle = 27
    scale = 1.0

    M = cv2.getRotationMatrix2D(center, angle, scale)

    rotated_image = cv2.warpAffine(gaussian_thresh_image, M, (w, h))

    show_image(rotated_image, "Imagem Rotacionada")

    # Detectando o ponteiro usando a Transformada de Hough para linhas
    edges = cv2.Canny(rotated_image, 50, 150)
    lines = cv2.HoughLinesP(
        edges, 1, np.pi / 180, threshold=50, minLineLength=30, maxLineGap=25
    )

    if lines is None:
        print("Nenhuma linha detectada.")
        return

    # Encontrando a linha mais longa
    longest_line = max(
        lines,
        key=lambda line: np.linalg.norm(
            [line[0][2] - line[0][0], line[0][3] - line[0][1]]
        ),
    )
    x1, y1, x2, y2 = longest_line[0]

    # Recortando a área ao redor do ponteiro
    padding = 10
    x_min = max(0, min(x1, x2) - padding)
    x_max = min(w, max(x1, x2) + padding)
    y_min = max(0, min(y1, y2) - padding)
    y_max = min(h, max(y1, y2) + padding)

    pointer_crop = rotated_image[y_min:y_max, x_min:x_max]

    show_image(pointer_crop, "Ponteiro Recortado")

    # Redimensionando a imagem cortada para 120x120 pixels
    size = (120, 120)
    image_resized = cv2.resize(pointer_crop, size)

    show_image(image_resized, "Imagem Redimensionada")

    # Calculando porcentagem de pixels pretos em cada quadrante
    quadrants = [
        (0, 0, 60, 60),  # Q1
        (60, 0, 120, 60),  # Q2
        (0, 60, 60, 120),  # Q3
        (60, 60, 120, 120),  # Q4
    ]

    percentages = [
        calculate_black_pixel_percentage(image_resized, *q, i)
        for i, q in enumerate(quadrants)
    ]

    # Exibindo os resultados
    for i, perc in enumerate(percentages, 1):
        print(f"Porcentagem de pixels pretos no Quadrante {i}: {perc:.2f}%")

    perc_2 = percentages[1]

    if perc_2 > 30:
        print("Nível de gás baixo!")

    # [perc_1, perc_2, perc_3, perc_4]
    return percentages


def process_image_digital(image_path):
    # Carregar a imagem
    imagem = cv2.imread(image_path)

    # Converter a imagem para escala de cinza
    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Aplicar threshold para melhorar o contraste do texto
    _, imagem_binaria = cv2.threshold(imagem_cinza, 150, 255, cv2.THRESH_BINARY)

    # Usar Tesseract para detectar os números na imagem
    detect_num = pytesseract.image_to_string(imagem_binaria, config="digits")

    detect_num = detect_num.replace("\n", "").strip()

    if detect_num.isdigit():
        detect_num = detect_num[:-1] + "." + detect_num[-1]

    return float(detect_num)
