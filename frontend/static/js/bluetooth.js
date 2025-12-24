/**
 * Bluetooth Low Energy (BLE) Device Integration Module
 * Handles connection to smartwatches and heart rate monitors
 */

class FitnessDeviceConnector {
    constructor() {
        this.device = null;
        this.server = null;
        this.characteristic = null;
        this.isConnected = false;
        this.heartRateData = [];
        this.listeners = {
            onConnect: null,
            onDisconnect: null,
            onHeartRateUpdate: null,
            onError: null
        };
    }

    /**
     * Check if browser supports Web Bluetooth API
     */
    isBluetoothSupported() {
        return navigator.bluetooth !== undefined;
    }

    /**
     * Initialize Bluetooth connection
     */
    async connect() {
        try {
            if (!this.isBluetoothSupported()) {
                throw new Error('Web Bluetooth API is not supported in this browser');
            }

            this.device = await navigator.bluetooth.requestDevice({
                filters: [
                    { services: ['heart_rate'] },
                    { namePrefix: 'Fitbit' },
                    { namePrefix: 'Apple' },
                    { namePrefix: 'Garmin' },
                    { name: 'Sw 81' }
                ],
                optionalServices: ['heart_rate']
            });

            this.device.addEventListener('gattserverdisconnected', () => this.handleDisconnect());

            this.server = await this.device.gatt.connect();
            const service = await this.server.getPrimaryService('heart_rate');
            this.characteristic = await service.getCharacteristic('heart_rate_measurement');

            // Start listening for notifications
            await this.characteristic.startNotifications();
            this.characteristic.addEventListener('characteristicvaluechanged',
                e => this.handleHeartRateUpdate(e));

            this.isConnected = true;
            if (this.listeners.onConnect) {
                this.listeners.onConnect(this.device.name);
            }

        } catch (error) {
            this.handleError(`Connection failed: ${error.message}`);
            throw error;
        }
    }

    /**
     * Disconnect from device
     */
    async disconnect() {
        try {
            if (this.characteristic) {
                await this.characteristic.stopNotifications();
            }
            if (this.server) {
                this.server.disconnect();
            }
            this.isConnected = false;
        } catch (error) {
            this.handleError(`Disconnection error: ${error.message}`);
        }
    }

    /**
     * Handle heart rate measurement
     */
    handleHeartRateUpdate(event) {
        const value = event.target.value;
        const heartRate = this.parseHeartRate(value);

        this.heartRateData.push({
            bpm: heartRate,
            timestamp: new Date()
        });

        if (this.listeners.onHeartRateUpdate) {
            this.listeners.onHeartRateUpdate(heartRate);
        }
    }

    /**
     * Parse heart rate from BLE characteristic
     */
    parseHeartRate(value) {
        const flags = value.getUint8(0);
        const rate16Bits = flags & 0x1;

        if (rate16Bits) {
            return value.getUint16(1, true);
        } else {
            return value.getUint8(1);
        }
    }

    /**
     * Get average heart rate
     */
    getAverageHeartRate() {
        if (this.heartRateData.length === 0) return 0;

        const sum = this.heartRateData.reduce((acc, data) => acc + data.bpm, 0);
        return Math.round(sum / this.heartRateData.length);
    }

    /**
     * Get maximum heart rate recorded
     */
    getMaxHeartRate() {
        if (this.heartRateData.length === 0) return 0;

        return Math.max(...this.heartRateData.map(data => data.bpm));
    }

    /**
     * Clear collected data
     */
    clearData() {
        this.heartRateData = [];
    }

    /**
     * Handle disconnect event
     */
    handleDisconnect() {
        this.isConnected = false;
        if (this.listeners.onDisconnect) {
            this.listeners.onDisconnect();
        }
    }

    /**
     * Handle error
     */
    handleError(message) {
        console.error('BLE Error:', message);
        if (this.listeners.onError) {
            this.listeners.onError(message);
        }
    }

    /**
     * Register event listeners
     */
    on(event, callback) {
        if (event in this.listeners) {
            this.listeners[event] = callback;
        }
    }

    /**
     * Get current connection status
     */
    getStatus() {
        return {
            isConnected: this.isConnected,
            deviceName: this.device ? this.device.name : null,
            heartRateData: this.heartRateData,
            averageHeartRate: this.getAverageHeartRate(),
            maxHeartRate: this.getMaxHeartRate(),
            sessionDuration: this.getSessionDuration()
        };
    }

    /**
     * Calculate session duration
     */
    getSessionDuration() {
        if (this.heartRateData.length === 0) return 0;

        const firstTime = this.heartRateData[0].timestamp;
        const lastTime = this.heartRateData[this.heartRateData.length - 1].timestamp;

        return Math.round((lastTime - firstTime) / 60000); // Convert to minutes
    }
}

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FitnessDeviceConnector;
}
