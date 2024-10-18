import cv2
import queue
from ultralytics import YOLO
from connection import process_commands
import multiprocessing
import time

# Definir cores
VERMELHO = (0, 0, 255)
VERDE = (0, 255, 0)
desired_width = 1280# Definir a largura desejada para a saída
desired_height =720  # Definir a altura desejada para a saída
# Carregar o modelo YOLO e classes
model = YOLO('runs/detect/train2/weights/best.pt')
class_names = model.names

# Definir limiares iniciais
CONFIDENCE_THRESHOLD = 0.6  # Limite de confiança inicial
IOU_THRESHOLD = 0.5  # Limite de IoU inicial

def update_confidence(val):
    global CONFIDENCE_THRESHOLD
    CONFIDENCE_THRESHOLD = val / 100  # Normalizando o valor para o intervalo 0.0 - 1.0
    print(f"Confidence Threshold ajustado para: {CONFIDENCE_THRESHOLD:.2f}")

def update_iou(val):
    global IOU_THRESHOLD
    IOU_THRESHOLD = val / 100  # Normalizando o valor para o intervalo 0.0 - 1.0
    print(f"IoU Threshold ajustado para: {IOU_THRESHOLD:.2f}")

def process_frame(frame):
    # Redimensionar o frame ANTES da inferência para garantir que ele esteja no tamanho desejado
    frame_resized = cv2.resize(frame, (desired_width, desired_height))

    # Realizar inferência com YOLO no frame redimensionado
    results = model(frame_resized, conf=CONFIDENCE_THRESHOLD, iou=IOU_THRESHOLD, imgsz=(desired_width, desired_height))
    alert_count = 0

    for result in results:
        for box in result.boxes:
            conf = box.conf[0]
            if conf >= CONFIDENCE_THRESHOLD:  # Aplicar o limiar de confiança
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                class_name = class_names[int(box.cls[0])]
                color = VERMELHO if class_name in ["lata_invertida", "lata_tombada"] else VERDE
                label = f"{class_name} {conf:.2f}"

                # Desenhar as caixas de detecção no frame
                cv2.rectangle(frame_resized, (x1, y1), (x2, y2), color, 2)
                cv2.putText(frame_resized, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

                # Contar alertas para as classes específicas
                if class_name in ["lata_invertida", "lata_tombada"]:
                    alert_count += 1

    return frame_resized, alert_count

def main():
    global CONFIDENCE_THRESHOLD, IOU_THRESHOLD

    # Inicialização do vídeo
    video_path = r'C:\Users\kingm\Desktop\VisionAlign\testes\videos\Video1.mp4'
    output_path = r'C:\Users\kingm\Desktop\VisionAlign\testes\videos\detectado\video_detectado.mp4'

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Erro ao abrir o vídeo.")
        exit()

    # Obter largura, altura e FPS do vídeo original
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:  # Em alguns casos, o OpenCV não consegue detectar o FPS
        fps = 30  # Define um valor padrão de FPS (30)

    # Inicializar o gravador de vídeo com a resolução desejada (1280x720)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec de vídeo
    out = cv2.VideoWriter(output_path, fourcc, fps, (desired_width, desired_height))

    command_queue = multiprocessing.Queue(maxsize=10)  # Use multiprocessing.Queue for inter-process communication

    # Processo para processar comandos do CLP
    process = multiprocessing.Process(target=process_commands, args=(command_queue,))
    process.start()

    # Criar uma janela para as barras deslizantes
    cv2.namedWindow('Sliders')

    # Criar as barras deslizantes para Confidence e IoU Thresholds
    cv2.createTrackbar('Confidence Threshold', 'Sliders', int(CONFIDENCE_THRESHOLD * 100), 100, update_confidence)
    cv2.createTrackbar('IoU Threshold', 'Sliders', int(IOU_THRESHOLD * 100), 100, update_iou)

    frame_time = int(1000 / fps)  # Tempo para exibir cada quadro (em milissegundos)

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Fim do vídeo.")
            break

        # Processar o quadro e redimensionar
        processed_frame, alert_count = process_frame(frame)

        # Mostrar o quadro processado
        cv2.imshow("Processed Frame", processed_frame)

        # Gravar o quadro processado no vídeo de saída
        out.write(processed_frame)

        # Aguardar o tempo correto para cada frame
        if cv2.waitKey(frame_time) & 0xFF == ord('q'):
            break

    # Liberar o vídeo, o gravador de vídeo e fechar as janelas
    cap.release()
    out.release()  # Certifique-se de liberar o gravador de vídeo
    cv2.destroyAllWindows()

    # Esperar o processo terminar antes de encerrar o programa
    process.join()

if __name__ == "__main__":
    multiprocessing.freeze_support()  # Use this if you're freezing the program with PyInstaller or similar
    main()
