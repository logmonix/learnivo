import axios from 'axios';
import { Platform } from 'react-native';

const getBackendUrl = () => {
    // For Android Emulator, localhost is 10.0.2.2
    if (Platform.OS === 'android') {
        return 'http://10.0.2.2:8001/api/v1';
    }
    // For iOS Simulator and Web, localhost works (if dev machine)
    // Note: For physical devices, you'll need your machine's LAN IP
    return 'http://localhost:8001/api/v1';
};

const api = axios.create({
    baseURL: getBackendUrl(),
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add a request interceptor to inject the token
api.interceptors.request.use(
    async (config) => {
        const { getToken } = require('./storage'); // Lazy load to avoid circular deps if any, though likely fine
        const token = await getToken();
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
