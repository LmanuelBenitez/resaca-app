import axios from 'axios';
import { Platform } from 'react-native';

const getApiUrl = () => {
    if (__DEV__) {
        // Emulador Android
        if (Platform.OS === 'android') {
        return 'http://10.0.2.2:8000';
        }
        // iOS / Web
        return 'http://localhost:8000';
    }
};

export const apiClient = axios.create({
    baseURL: getApiUrl(),
    headers: {
        'Content-Type': 'application/json',
    },
    timeout: 10000,
});