from pylogix import PLC
import queue
import logging
import time

# Configurações do CLP
ip_address = "192.168.5.66"  # Endereço IP do CLP Rockwell

def process_commands(command_queue):
    plc = PLC()
    plc.IPAddress = ip_address

    while True:
        try:
            command = command_queue.get()
            if command == 'stop_machine':
                plc.Write('MotorStatus', 0)  # Parar o motor TAG
                plc.Write('SireneStatus', 1)  # Ativar a sirene TAG
                logging.info("Sinal de parada enviado para o CLP")

                save_report()

                while True:
                    # Lê o status atual do motor e da sirene
                    motor_status = plc.Read('MotorStatus').Value
                    sirene_status = plc.Read('SireneStatus').Value

                    # Verifica se o motor foi reiniciado e a sirene está desligada
                    if motor_status == 1 and sirene_status == 0:
                        logging.info("Motor reiniciado e sirene desligada. Enviando sinal de reset.")
                        command_queue.put('reset') 

                    time.sleep(1)  # Espera 1 segundo antes da próxima verificação

        except Exception as e:
            logging.error(f"Erro ao processar comando: {e}")

def save_report():
    """Salva o relatório com informações sobre a parada."""
    file_path = f"Relatorio/Relatorio.txt"  # Ajuste o nome do arquivo conforme necessário
    with open(file_path, "w") as report_file:
        report_file.write(f"Parada do motor: 0\n")  # 0 indica que o motor foi parado
        report_file.write(f"Status da sirene: 1\n")  # 1 indica que a sirene foi ativada
    print(f"Relatório salvo: {file_path}")

# Inicialização do logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
