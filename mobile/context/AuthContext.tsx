import React, { createContext, useContext, useState, useEffect } from 'react';
import { useRouter, useSegments } from 'expo-router';
import { getToken, saveToken, removeToken } from '../services/storage';

type AuthContextType = {
    signIn: (token: string) => void;
    signOut: () => void;
    isAuthenticated: boolean;
    isLoading: boolean;
};

const AuthContext = createContext<AuthContextType>({
    signIn: () => { },
    signOut: () => { },
    isAuthenticated: false,
    isLoading: true,
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider = ({ children }: { children: React.ReactNode }) => {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();
    const segments = useSegments();

    useEffect(() => {
        const checkAuth = async () => {
            try {
                const token = await getToken();
                setIsAuthenticated(!!token);
            } catch (e) {
                setIsAuthenticated(false);
            } finally {
                setIsLoading(false);
            }
        };
        checkAuth();
    }, []);

    useEffect(() => {
        if (isLoading) return;

        const inAuthGroup = segments[0] === '(tabs)';

        if (!isAuthenticated && inAuthGroup) {
            // Redirect to the login page if not authenticated
            router.replace('/login');
        } else if (isAuthenticated && segments[0] === 'login') {
            // Redirect to the home page if authenticated
            router.replace('/(tabs)');
        }
    }, [isAuthenticated, segments, isLoading]);

    const signIn = async (token: string) => {
        await saveToken(token);
        setIsAuthenticated(true);
        router.replace('/select-profile');
    };

    const signOut = async () => {
        await removeToken();
        setIsAuthenticated(false);
        router.replace('/login');
    };

    return (
        <AuthContext.Provider
            value={{
                signIn,
                signOut,
                isAuthenticated,
                isLoading,
            }}
        >
            {children}
        </AuthContext.Provider>
    );
};
