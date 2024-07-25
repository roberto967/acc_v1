import asyncio
import csv
from datetime import datetime
import bleak
import time
import numpy as np

from device_model import DeviceModel

devices = []
acc_data = []


async def scan():
    global devices
    print("Pesquisando dispositivos Bluetooth......")
    try:
        devices = await bleak.BleakScanner.discover()
        print("Pesquisa finalizada")
        for d in devices:
            if d.name is not None and "WT" in d.name:  # O nome do dispositivo contém "WT"
                print(d)
    except Exception as ex:
        print("Falha ao iniciar a busca por Bluetooth")
        print(ex)
        exit()


def print_collecteData(DeviceModel):
    print(DeviceModel.deviceData)


def saveData(DeviceModel):
    # Salvar dados no formato CSV
    # Timestaps tem que ser feitos de forma diferente para ir para o tratamento dos dados, no caso fica o ms
    fieldnames = ['hora', 'gFx', 'gFy', 'gFz',
                  'AsX', 'AsY', 'AsZ', 'AngX', 'AngY', 'AngZ']
    with open("device_data.csv", "a", newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:  # Escrever cabeçalho apenas se o arquivo estiver vazio
            writer.writeheader()
        data = DeviceModel.deviceData
        data['hora'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        writer.writerow(data)


def main():
    asyncio.run(scan())

    device_mac = None
    user_input = input(
        "Por favor, digite o endereço Mac do dispositivo ao qual deseja se conectar (ex. DF:E9:1F:2C:BD:59)：")
    for device in devices:
        if device.address == user_input:
            device_mac = device.address
            break

    # Se o dispositivo for encontrado, conecte-se a ele
    # Aqui tem que ver a questão do salvamento dos dados pois a função não reescreve o aquivo quando o programa reinicia
    if device_mac is not None:
        print("Conectando ao dispositivo......")
        device = DeviceModel(
            "MyBle5.0", device_mac, saveData)

        asyncio.run(device.openDevice())

        print(acc_data)
    else:
        print("Nenhum dispositivo Bluetooth correspondente ao endereço Mac encontrado!!")


if __name__ == '__main__':
    main()
