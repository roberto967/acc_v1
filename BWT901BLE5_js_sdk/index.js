import DeviceModel from "./device_model.js";
import {add, sub, mul, div} from "./operations.js";

const searchButton = document.getElementById("search");
const deviceList = document.getElementById("deviceList");
const recordBtn = document.getElementById("recordBtn");
const viewDataBtn = document.getElementById("viewDataBtn");
const clearDataBtn = document.getElementById("clsDataBtn");

let devices = [];
let connectedDeviceModel = null;
let recording = false;
let recordedData = [];
let startTime = 0;

async function scan() {
	console.log("Pesquisando dispositivos Bluetooth...");
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
		console.log(`Conectado ao dispositivo: ${device.name}`);
	} catch (error) {
		console.log("Erro ao conectar ao dispositivo");
		console.log(error);
	}
}

function saveData(deviceModel) {
	if (recording) {
		const currentTime = div(sub(performance.now(), startTime), 1000);
		const data = {
			timestamp: currentTime,
			data: structuredClone(deviceModel.deviceData),
		};
		recordedData.push(data);
		console.log("Dados gravados: ", data);
	} else {
		console.log("Dados recebidos (não gravados): ", deviceModel.deviceData);
	}
}

recordBtn.addEventListener("click", () => {
	recording = !recording;
	if (recording) {
		recordBtn.textContent = "Stop Recording";
		recordedData = []; // Reseta o array para gravar novos dados
		startTime = performance.now();
		console.log("Iniciando gravação...");
	} else {
		recordBtn.textContent = "Record Data";
		console.log("Parando gravação...");
	}
});

viewDataBtn.addEventListener("click", () => {
	if (recording) {
		recording = false;
		recordBtn.textContent = "Record Data";
		console.log("Parando gravação...");
	}

	console.log("Visualizando dados gravados: ", recordedData);
	const dataBlob = new Blob([JSON.stringify(recordedData, null, 2)], {
		type: "application/json",
	});
	const url = URL.createObjectURL(dataBlob);
	window.open(url);
});

clearDataBtn.addEventListener("click", () => {
	recordedData = [];
	alert("Dados apagados");
	console.log("Dados apagados");
});
