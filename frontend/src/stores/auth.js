import { defineStore } from 'pinia';
import api from '../api/axios';
import { ref } from 'vue';
import { useRouter } from 'vue-router';

export const useAuthStore = defineStore('auth', () => {
    const user = ref(null);
    const token = ref(localStorage.getItem('token') || null);
    const router = useRouter();

    async function login(email, password) {
        try {
            const response = await api.post('/auth/login', { email, password });
            token.value = response.data.access_token;
            localStorage.setItem('token', token.value);

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
        token.value = null;
        user.value = null;
        localStorage.removeItem('token');
        router.push('/login');
    }

    return { user, token, login, register, logout };
});
