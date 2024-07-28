class DeviceModel {
	constructor(deviceName, mac, callbackMethod) {
		this.deviceName = deviceName;
		this.mac = mac;
		this.deviceData = {};
		this.isOpen = false;
		this.TempBytes = [];
		this.callbackMethod = callbackMethod;
	}

	set(key, value) {
		this.deviceData[key] = value;
	}

	get(key) {
		return this.deviceData[key] || null;
	}

	remove(key) {
		delete this.deviceData[key];
	}

	async openDevice() {
		try {
			console.log("Iniciando o dispositivo...");
			const device = await navigator.bluetooth.requestDevice({
				filters: [{ services: ["0000ffe5-0000-1000-8000-00805f9a34fb"] }],
			});

			const server = await device.gatt.connect();
			this.isOpen = true;
			const service = await server.getPrimaryService(
				"0000ffe5-0000-1000-8000-00805f9a34fb"
			);
			const notifyCharacteristic = await service.getCharacteristic(
				"0000ffe4-0000-1000-8000-00805f9a34fb"
			);
			this.writerCharacteristic = await service.getCharacteristic(
				"0000ffe9-0000-1000-8000-00805f9a34fb"
			);

			notifyCharacteristic.startNotifications();
			notifyCharacteristic.addEventListener(
				"characteristicvaluechanged",
				this.onDataReceived.bind(this)
			);
		} catch (error) {
			console.error(error);
		}
	}

	closeDevice() {
		this.isOpen = false;
		console.log("O dispositivo está desligado");
	}

	onDataReceived(event) {
		let data = new Uint8Array(event.target.value.buffer);
		for (let i = 0; i < data.length; i++) {
			this.TempBytes.push(data[i]);
			if (
				this.TempBytes.length === 2 &&
				(this.TempBytes[0] !== 0x55 || this.TempBytes[1] !== 0x61)
			) {
				this.TempBytes.shift();
				continue;
			}
			if (this.TempBytes.length === 20) {
				this.processData(this.TempBytes.slice(2));
				this.TempBytes = [];
			}
		}
	}

	processData(Bytes) {
		let Ax = (this.getSignInt16((Bytes[1] << 8) | Bytes[0]) / 32768) * 16;
		let Ay = (this.getSignInt16((Bytes[3] << 8) | Bytes[2]) / 32768) * 16;
		let Az = (this.getSignInt16((Bytes[5] << 8) | Bytes[4]) / 32768) * 16;
		let Gx = (this.getSignInt16((Bytes[7] << 8) | Bytes[6]) / 32768) * 2000;
		let Gy = (this.getSignInt16((Bytes[9] << 8) | Bytes[8]) / 32768) * 2000;
		let Gz = (this.getSignInt16((Bytes[11] << 8) | Bytes[10]) / 32768) * 2000;
		let AngX = (this.getSignInt16((Bytes[13] << 8) | Bytes[12]) / 32768) * 180;
		let AngY = (this.getSignInt16((Bytes[15] << 8) | Bytes[14]) / 32768) * 180;
		let AngZ = (this.getSignInt16((Bytes[17] << 8) | Bytes[16]) / 32768) * 180;
		this.set("gFx", Ax.toFixed(3));
		this.set("gFy", Ay.toFixed(3));
		this.set("gFz", Az.toFixed(3));
		this.set("AsX", Gx.toFixed(3));
		this.set("AsY", Gy.toFixed(3));
		this.set("AsZ", Gz.toFixed(3));
		this.set("AngX", AngX.toFixed(3));
		this.set("AngY", AngY.toFixed(3));
		this.set("AngZ", AngZ.toFixed(3));
		this.callbackMethod(this);
	}

	getSignInt16(num) {
		if (num >= Math.pow(2, 15)) {
			num -= Math.pow(2, 16);
		}
		return num;
	}

	async sendData(data) {
		if (this.writerCharacteristic) {
			await this.writerCharacteristic.writeValue(new Uint8Array(data));
		}
	}

	getReadBytes(regAddr) {
		return [0xff, 0xaa, 0x27, regAddr, 0];
	}

	getWriteBytes(regAddr, rValue) {
		return [0xff, 0xaa, regAddr, rValue & 0xff, rValue >> 8];
	}

	async readReg(regAddr) {
		await this.sendData(this.getReadBytes(regAddr));
	}

	async writeReg(regAddr, sValue) {
		await this.unlock();
		await this.delay(100);
		await this.sendData(this.getWriteBytes(regAddr, sValue));
		await this.delay(100);
		await this.save();
	}

	async unlock() {
		await this.sendData(this.getWriteBytes(0x69, 0xb588));
	}

	async save() {
		await this.sendData(this.getWriteBytes(0x00, 0x0000));
	}

	delay(ms) {
		return new Promise((resolve) => setTimeout(resolve, ms));
	}
}

export default DeviceModel;
