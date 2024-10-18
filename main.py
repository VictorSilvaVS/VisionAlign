import cv2
import queue
from ultralytics import YOLO
from connection import process_commands
import multiprocessing
import time

# Definir cores
VERMELHO = (0, 0, 255)
VERDE = (0, 255, 0)

# Carregar o modelo YOLO e classes
model = YOLO('detect/train2/weights/best.pt')
class_names = model.names

def process_frame(frame):
    try:
        results = model(frame)
    except Exception as e:
        print(f"Erro ao processar o frame: {e}")
        return frame, 0

    alert_count = sum(1 for result in results for box in result.boxes 
                      if class_names[int(box.cls[0])] in ["lata_invertida", "lata_tombada"])

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            conf = box.conf[0]
            class_name = class_names[int(box.cls[0])]
            color = VERMELHO if class_name in ["lata_invertida", "lata_tombada"] else VERDE
            label = f"{class_name} {conf:.2f}"

            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            cv2.putText(frame, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    return frame, alert_count

def main():
    cap = cv2.VideoCapture(0)  # Tenta capturar da webcam (índice 0)
    
    if not cap.isOpened():
        print("Erro ao abrir a câmera. Verifique se a câmera está conectada corretamente.")
        return
    
    command_queue = multiprocessing.Queue(maxsize=10)

    # Processo para processar comandos do CLP
    process = multiprocessing.Process(target=process_commands, args=(command_queue,))
    process.start()

    stop_signal_sent = False  # Variável para controlar o envio do sinal de parada

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Erro ao capturar vídeo da webcam.")
                break

            processed_frame, alert_count = process_frame(frame)

            cv2.imshow("Processed Frame", processed_frame)

            # Se o número de alertas for maior ou igual a 10 e o sinal de parada não foi enviado
            if alert_count >= 10 and not stop_signal_sent:
                command_queue.put('stop_machine')  # Enviar comando para parar a máquina
                print("Alerta acionado: Máquina parando.")
                stop_signal_sent = True  # Marca que o sinal de parada foi enviado

            # Verifique se há um sinal de reset do CLP
            if not command_queue.empty():
                command = command_queue.get()
                if command == 'reset':
                    print("Recebido sinal de reset do CLP. A máquina pode ser iniciada novamente.")
                    stop_signal_sent = False  # Permite que um novo sinal de parada seja enviado

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        cap.release()
        cv2.destroyAllWindows()
        
        # Esperar o processo terminar antes de encerrar o programa
        process.join()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    main()
