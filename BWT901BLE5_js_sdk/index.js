import DeviceModel from "./device_model.js";

const searchButton = document.getElementById("search");
const deviceList = document.getElementById("deviceList");
const sendButton = document.getElementById("send");
const readButton = document.getElementById("read");

let devices = [];
let connectedDeviceModel = null;

async function scan() {
	console.log("Pesquisando dispositivos Bluetooth......");
	try {
		const options = {
			acceptAllDevices: true,
		};

		const device = await navigator.bluetooth.requestDevice(options);
		console.log("Pesquisa finalizada");

		if (device && device.name) {
			devices.push(device);
			const listItem = document.createElement("li");
			listItem.textContent = `Name: ${device.name}, MAC: ${device.id}`;
			listItem.addEventListener("click", () => connectDevice(device));
			deviceList.appendChild(listItem);
			console.log(device);
		}
	} catch (ex) {
		console.log("Falha ao iniciar a busca por Bluetooth");
		console.log(ex);
	}
}

searchButton.addEventListener("click", scan);

async function connectDevice(device) {
	try {
		console.log(`Conectando ao dispositivo: ${device.name}`);
		const deviceModel = new DeviceModel(device.name, device.id, saveData);
		await deviceModel.openDevice();
		connectedDeviceModel = deviceModel;
	} catch (error) {
		console.log("Erro ao conectar ao dispositivo");
		console.log(error);
	}
}

function saveData(deviceModel) {
	const fieldnames = [
		"hora",
		"AccX",
		"AccY",
		"AccZ",
		"AsX",
		"AsY",
		"AsZ",
		"AngX",
		"AngY",
		"AngZ",
	];
	const data = deviceModel.deviceData;
	data["hora"] = new Date().toISOString();

	const csvData = fieldnames.map((field) => data[field]).join(",");
	const csvHeader = fieldnames.join(",");

	let csvContent = localStorage.getItem("device_data_csv");

	if (!csvContent) {
		csvContent = `${csvHeader}\n${csvData}`;
	} else {
		csvContent += `\n${csvData}`;
	}

	localStorage.setItem("device_data_csv", csvContent);
	console.log("Data saved:", csvData);
}

sendButton.addEventListener("click", () => {
	if (connectedDeviceModel) {
		const data = prompt(
			"Digite os dados a serem enviados (ex.: 0x01,0x02,0x03):"
		)
			.split(",")
			.map(Number);
		connectedDeviceModel.sendData(data);
	} else {
		console.log("Nenhum dispositivo conectado");
	}
});

readButton.addEventListener("click", () => {
	if (connectedDeviceModel) {
		const regAddr = parseInt(
			prompt("Digite o endereço do registro para ler (ex.: 0x01):"),
			16
		);
		connectedDeviceModel.readReg(regAddr);
	} else {
		console.log("Nenhum dispositivo conectado");
	}
});
