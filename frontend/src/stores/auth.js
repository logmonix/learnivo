import { defineStore } from 'pinia';
import api from '../api/axios';
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
    // Safely parse user from localStorage
    let user = ref(null);
    try {
        const storedUser = localStorage.getItem('user');
        if (storedUser && storedUser !== 'undefined' && storedUser !== 'null') {
            user = ref(JSON.parse(storedUser));
        }
    } catch (error) {
        console.warn('Failed to parse stored user data:', error);
        localStorage.removeItem('user'); // Clean up invalid data
    }

    const token = ref(localStorage.getItem('token') || '');
    const router = useRouter();

    const isAdmin = computed(() => user.value?.is_admin || false);

    async function login(email, password) {
        try {
            const response = await api.post('/auth/login', { email, password });
            token.value = response.data.access_token;
            user.value = response.data.user;
            localStorage.setItem('token', token.value);
            localStorage.setItem('user', JSON.stringify(user.value));

            // Ideally fetch user profile here
            // user.value = await fetchUserProfile();

            return true;
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }

    async function register(email, password, fullName) {
        try {
            await api.post('/auth/register', { email, password, full_name: fullName });
            return true;
        } catch (error) {
            console.error('Registration failed:', error);
            throw error;
        }
    }

    function logout() {
        token.value = '';
        user.value = null;
        localStorage.removeItem('token');
        localStorage.removeItem('user');
        router.push('/login');
    }

    return { token, user, isAdmin, login, register, logout };
});
