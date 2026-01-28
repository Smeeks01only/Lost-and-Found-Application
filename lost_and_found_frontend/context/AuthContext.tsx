import React, { createContext, useState, useContext, useEffect } from 'react';
import { getMe, logout as authLogout } from '../services/auth';
import * as SecureStore from 'expo-secure-store';
import { useRouter, useSegments } from 'expo-router';
import { User } from '../types';

interface AuthContextData {
    user: User | null;
    isLoading: boolean;
    signIn: (userData: User) => void;
    signOut: () => void;
}

const AuthContext = createContext<AuthContextData>({
    user: null,
    isLoading: true,
    signIn: () => { },
    signOut: () => { },
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [user, setUser] = useState<User | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();
    const segments = useSegments();

    useEffect(() => {
        const checkUser = async () => {
            try {
                // If we have a token, try to fetch user
                const token = await SecureStore.getItemAsync('access_token');
                if (token) {
                    const userData = await getMe();
                    setUser(userData);
                }
            } catch (e) {
                console.log("Not logged in or token expired");
            } finally {
                setIsLoading(false);
            }
        };
        checkUser();
    }, []);

    useEffect(() => {
        if (isLoading) return;

        const inAuthGroup = segments[0] === '(auth)';

        if (!user && !inAuthGroup) {
            // Redirect to login if not authenticated
            router.replace('/(auth)/login');
        } else if (user && inAuthGroup) {
            // Redirect to home if authenticated
            router.replace('/(tabs)');
        }
    }, [user, segments, isLoading]);

    const signIn = (userData: User) => {
        setUser(userData);
    };

    const signOut = async () => {
        await authLogout();
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, isLoading, signIn, signOut }}>
            {children}
        </AuthContext.Provider>
    );
};
