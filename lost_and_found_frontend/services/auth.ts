import api from './api';
import * as SecureStore from 'expo-secure-store';

export const login = async (username: string, password: string) => {
    const response = await api.post('/auth/login/', { username, password });
    const { access, refresh } = response.data;
    await SecureStore.setItemAsync('access_token', access);
    await SecureStore.setItemAsync('refresh_token', refresh);
    return response.data;
};

export const register = async (username: string, email: string, password: string, role: string) => {
    const response = await api.post('/auth/register/', { username, email, password, role });
    return response.data;
};

export const getMe = async () => {
    const response = await api.get('/auth/me/');
    return response.data;
};

export const logout = async () => {
    await SecureStore.deleteItemAsync('access_token');
    await SecureStore.deleteItemAsync('refresh_token');
};
