import axios from 'axios';
import { Platform } from 'react-native';
import * as SecureStore from 'expo-secure-store';

// ----------------------------------------------------------------------
// ⚡ NETWORK DEBUGGING
// Your Wi-Fi IP is: 192.168.1.102
// We are hardcoding this to ensure physical devices can connect.
// ----------------------------------------------------------------------

const BASE_URL = 'http://192.168.1.102:8000';

console.log(`[API] Using Base URL: ${BASE_URL}`);

const api = axios.create({
    baseURL: BASE_URL,
    timeout: 5000,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Interceptor to add Token
api.interceptors.request.use(
    async (config) => {
        const token = await SecureStore.getItemAsync('access_token');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

export default api;
