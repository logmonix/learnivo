import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, FlatList, TouchableOpacity, RefreshControl, Platform } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useRouter } from 'expo-router';
import * as SecureStore from 'expo-secure-store';
import api from '@/services/api';
import { useAuth } from '@/context/AuthContext';

const getStorageItem = async (key: string) => {
  if (Platform.OS === 'web') return localStorage.getItem(key);
  return await SecureStore.getItemAsync(key);
}

export default function StudentHomeScreen() {
  const [subjects, setSubjects] = useState<any[]>([]);
  const [profileName, setProfileName] = useState('');
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const { signOut } = useAuth();
  const router = useRouter();

  const loadData = async () => {
    try {
      const name = await getStorageItem('current_profile_name');
      const grade = await getStorageItem('current_grade_level');
      setProfileName(name || 'Student');

      if (grade) {
        const response = await api.get(`/curriculum/subjects?grade_level=${grade}`);
        setSubjects(response.data);
      }
    } catch (error) {
      console.error('Failed to load data', error);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const onRefresh = () => {
    setRefreshing(true);
    loadData();
  };

  const colors = ['#FCD34D', '#F472B6', '#60A5FA', '#34D399', '#A78BFA']; // Yellow, Pink, Blue, Green, Purple

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.greeting}>Hi, {profileName}!</Text>
          <Text style={styles.subtitle}>Ready to learn?</Text>
        </View>
        <TouchableOpacity onPress={signOut} style={styles.logoutButton}>
          <Text style={styles.logoutText}>Logout</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.sectionTitle}>My Subjects</Text>

      <FlatList
        data={subjects}
        keyExtractor={(item) => item.id.toString()}
        contentContainerStyle={styles.list}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
        }
        renderItem={({ item, index }) => (
          <TouchableOpacity
            style={[styles.subjectCard, { backgroundColor: colors[index % colors.length] }]}
            onPress={() => console.log('Open Subject', item.name)} // TODO: Navigate to chapters
          >
            <Text style={styles.subjectIcon}>{item.emoji || '📚'}</Text>
            <Text style={styles.subjectName}>{item.name}</Text>
            <Text style={styles.subjectChapters}>{item.chapter_count || 0} Chapters</Text>
          </TouchableOpacity>
        )}
        ListEmptyComponent={
          !loading ? (
            <View style={styles.emptyState}>
              <Text style={styles.emptyText}>No subjects found.</Text>
            </View>
          ) : null
        }
      />
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F3F4F6',
    paddingHorizontal: 20,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 20,
  },
  greeting: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#111827',
    fontFamily: Platform.select({ ios: 'Arial Rounded MT Bold', android: 'sans-serif-medium', web: 'sans-serif' }),
  },
  subtitle: {
    fontSize: 16,
    color: '#6B7280',
  },
  logoutButton: {
    padding: 8,
  },
  logoutText: {
    color: '#EF4444',
    fontWeight: '600',
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    color: '#374151',
    marginBottom: 16,
  },
  list: {
    paddingBottom: 20,
  },
  subjectCard: {
    borderRadius: 20,
    padding: 24,
    marginBottom: 16,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
    flexDirection: 'row',
    alignItems: 'center',
  },
  subjectIcon: {
    fontSize: 40,
    marginRight: 16,
  },
  subjectName: {
    fontSize: 22,
    fontWeight: 'bold',
    color: '#FFFFFF',
    flex: 1,
    textShadowColor: 'rgba(0,0,0,0.1)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 2,
  },
  subjectChapters: {
    fontSize: 14,
    color: 'rgba(255,255,255,0.9)',
    fontWeight: '600',
  },
  emptyState: {
    alignItems: 'center',
    marginTop: 40,
  },
  emptyText: {
    color: '#9CA3AF',
    fontSize: 16,
  }
});
