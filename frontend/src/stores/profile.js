import { defineStore } from 'pinia';
import api from '../api/axios';
import { ref } from 'vue';

export const useProfileStore = defineStore('profile', () => {
    const profiles = ref([]);
    const currentProfile = ref(null);
    const loading = ref(false);

    async function fetchProfiles() {
        loading.value = true;
        try {
            const response = await api.get('/profiles/');
            profiles.value = response.data;
        } catch (error) {
            console.error('Failed to fetch profiles:', error);
        } finally {
            loading.value = false;
        }
    }

    async function createProfile(profileData) {
        try {
            const response = await api.post('/profiles/', profileData);
            profiles.value.push(response.data);
            return true;
        } catch (error) {
            console.error('Failed to create profile:', error);
            throw error;
        }
    }

    function selectProfile(profile) {
        currentProfile.value = profile;
        // You might want to persist this choice or navigate
    }

    return { profiles, currentProfile, loading, fetchProfiles, createProfile, selectProfile };
});
