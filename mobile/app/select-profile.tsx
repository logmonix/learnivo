import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, TouchableOpacity, StyleSheet, ActivityIndicator } from 'react-native';
import { useRouter } from 'expo-router';
// import { Image } from 'expo-image'; // Removed unused
import api from '../services/api';
import * as SecureStore from 'expo-secure-store';
import { Platform } from 'react-native';

export default function SelectProfileScreen() {
    const [profiles, setProfiles] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);
    const router = useRouter();

    useEffect(() => {
        fetchProfiles();
    }, []);

    const fetchProfiles = async () => {
        try {
            const response = await api.get('/profiles');
            setProfiles(response.data);
        } catch (error) {
            console.error('Failed to fetch profiles', error);
        } finally {
            setLoading(false);
        }
    };

    const handleSelectProfile = async (profile: any) => {
        try {
            if (Platform.OS === 'web') {
                localStorage.setItem('current_profile_id', profile.id.toString());
                localStorage.setItem('current_grade_level', profile.grade_level.toString());
                localStorage.setItem('current_profile_name', profile.name);
            } else {
                await SecureStore.setItemAsync('current_profile_id', profile.id.toString());
                await SecureStore.setItemAsync('current_grade_level', profile.grade_level.toString());
                await SecureStore.setItemAsync('current_profile_name', profile.name);
            }

            // Navigate to main app
            router.replace('/(tabs)');
        } catch (e) {
            console.error("Error saving profile", e);
        }
    };

    if (loading) {
        return (
            <View style={styles.container}>
                <ActivityIndicator size="large" color="#7C3AED" />
            </View>
        );
    }

    return (
        <View style={styles.container}>
            <Text style={styles.title}>Who is learning?</Text>

            <FlatList
                data={profiles}
                keyExtractor={(item) => item.id.toString()}
                numColumns={2}
                contentContainerStyle={styles.listContainer}
                renderItem={({ item }) => (
                    <TouchableOpacity
                        style={styles.profileCard}
                        onPress={() => handleSelectProfile(item)}
                    >
                        <View style={[styles.avatar, { backgroundColor: item.avatar_color || '#3B82F6' }]}>
                            <Text style={styles.avatarText}>{item.name[0]}</Text>
                        </View>
                        <Text style={styles.profileName}>{item.name}</Text>
                        <Text style={styles.gradeText}>Grade {item.grade_level}</Text>
                    </TouchableOpacity>
                )}
            />
        </View>
    );
}

const styles = StyleSheet.create({
    container: {
        flex: 1,
        padding: 20,
        paddingTop: 60,
        backgroundColor: '#F3F4F6',
        alignItems: 'center',
    },
    title: {
        fontSize: 28,
        fontWeight: 'bold',
        color: '#111827',
        marginBottom: 40,
        fontFamily: Platform.select({ ios: 'Arial Rounded MT Bold', android: 'sans-serif-medium', web: 'sans-serif' }),
    },
    listContainer: {
        alignItems: 'center',
    },
    profileCard: {
        backgroundColor: 'white',
        borderRadius: 20,
        padding: 20,
        margin: 10,
        alignItems: 'center',
        width: 150,
        shadowColor: '#000',
        shadowOffset: { width: 0, height: 2 },
        shadowOpacity: 0.1,
        shadowRadius: 4,
        elevation: 3,
    },
    avatar: {
        width: 80,
        height: 80,
        borderRadius: 40,
        justifyContent: 'center',
        alignItems: 'center',
        marginBottom: 12,
    },
    avatarText: {
        fontSize: 32,
        fontWeight: 'bold',
        color: 'white',
    },
    profileName: {
        fontSize: 18,
        fontWeight: 'bold',
        color: '#374151',
        marginBottom: 4,
    },
    gradeText: {
        fontSize: 14,
        color: '#6B7280',
    },
});
