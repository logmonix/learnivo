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
        localStorage.setItem('currentProfileId', profile.id);
    }

    function loadCurrentProfile() {
        const profileId = localStorage.getItem('currentProfileId');
        if (profileId && profiles.value.length > 0) {
            currentProfile.value = profiles.value.find(p => p.id === profileId);
        }
    }

    return { profiles, currentProfile, loading, fetchProfiles, createProfile, selectProfile, loadCurrentProfile };
});
