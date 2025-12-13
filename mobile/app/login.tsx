import React, { useState } from 'react';
import { View, Text, TextInput, TouchableOpacity, StyleSheet, ActivityIndicator, Alert, KeyboardAvoidingView, Platform } from 'react-native';
import { Stack } from 'expo-router';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';
import { Image } from 'expo-image';

export default function LoginScreen() {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [loading, setLoading] = useState(false);
    const { signIn } = useAuth();

    const handleLogin = async () => {
        if (!username || !password) {
            Alert.alert('Error', 'Please enter both username/email and password');
            return;
        }

        setLoading(true);
        try {
            // The backend expects x-www-form-urlencoded for OAuth2
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await api.post('/auth/token', formData, {
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
            });

            const { access_token } = response.data;
            await signIn(access_token);
        } catch (error: any) {
            console.error(error);
            const msg = error.response?.data?.detail || 'Login failed. Please check your credentials.';
            Alert.alert('Login Failed', msg);
        } finally {
            setLoading(false);
        }
    };

    return (
        <KeyboardAvoidingView
            behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
            style={styles.container}
        >
            <Stack.Screen options={{ headerShown: false }} />

            <View style={styles.content}>
                <View style={styles.header}>
                    {/* Placeholder for logo - using text for now */}
                    <Text style={styles.title}>Learnivo</Text>
                    <Text style={styles.subtitle}>Fun learning for everyone!</Text>
                </View>

                <View style={styles.form}>
                    <View style={styles.inputContainer}>
                        <Text style={styles.label}>Email</Text>
                        <TextInput
                            style={styles.input}
                            placeholder="parent@example.com"
                            value={username}
                            onChangeText={setUsername}
                            autoCapitalize="none"
                            keyboardType="email-address"
                            placeholderTextColor="#9CA3AF"
                        />
                    </View>

                    <View style={styles.inputContainer}>
                        <Text style={styles.label}>Password</Text>
                        <TextInput
                            style={styles.input}
                            placeholder="••••••••"
                            value={password}
                            onChangeText={setPassword}
                            secureTextEntry
                            placeholderTextColor="#9CA3AF"
                        />
                    </View>

                    <TouchableOpacity
                        style={styles.button}
                        onPress={handleLogin}
                        disabled={loading}
                    >
                        {loading ? (
                            <ActivityIndicator color="#FFFFFF" />
                        ) : (
                            <Text style={styles.buttonText}>Sign In</Text>
                        )}
                    </TouchableOpacity>
                </View>
            </View>
        </KeyboardAvoidingView>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F3F4F6', // Gray-100
    },
    content: {
        flex: 1,
        padding: 24,
        justifyContent: 'center',
    },
    header: {
        alignItems: 'center',
        marginBottom: 40,
    },
    title: {
        fontSize: 40,
        fontWeight: 'bold',
        color: '#7C3AED', // Violet-600
        marginBottom: 8,
        fontFamily: Platform.select({ ios: 'Arial Rounded MT Bold', android: 'sans-serif-medium', web: 'sans-serif' }),
    },
    subtitle: {
        fontSize: 18,
        color: '#4B5563', // Gray-600
    },
    form: {
        backgroundColor: '#FFFFFF',
        padding: 24,
        borderRadius: 20,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.1,
        shadowRadius: 10,
        elevation: 5,
    },
    inputContainer: {
        marginBottom: 20,
    },
    label: {
        fontSize: 14,
        fontWeight: '600',
        color: '#374151', // Gray-700
        marginBottom: 8,
    },
    input: {
        backgroundColor: '#F9FAFB', // Gray-50
        borderWidth: 1,
        borderColor: '#E5E7EB', // Gray-200
        borderRadius: 12,
        padding: 16,
        fontSize: 16,
        color: '#111827',
    },
    button: {
        backgroundColor: '#7C3AED', // Violet-600
        padding: 16,
        borderRadius: 12,
        alignItems: 'center',
        marginTop: 8,
        shadowColor: '#7C3AED',
        shadowOffset: { width: 0, height: 4 },
        shadowOpacity: 0.3,
        shadowRadius: 8,
        elevation: 4,
    },
    buttonText: {
        color: '#FFFFFF',
        fontSize: 18,
        fontWeight: 'bold',
    },
});
