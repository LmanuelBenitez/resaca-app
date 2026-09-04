import axios from 'axios';
import { Platform } from 'react-native';
import Constants from 'expo-constants';

const PC_IP = '192.168.1.76';

const getApiUrl = () => {
    if (__DEV__) {
        // Emulador Android
        if (Platform.OS === 'web') {
            return 'http://localhost:8000';
        }
        
        // Emulador Android
        if (Platform.OS === 'android' && Constants.isDevice === false) {
            return 'http://10.0.2.2:8000';
        }
        
        // Emulador iOS
        if (Platform.OS === 'ios' && Constants.isDevice === false) {
            return 'http://localhost:8000';
        }
        
        // Dispositivo físico (Android o iOS)
        return `http://${PC_IP}:8000`;
    }
    return 'https://tu-api.com';
};

export const apiClient = axios.create({
    baseURL: getApiUrl(),
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
});