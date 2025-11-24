<script setup>
import { ref } from 'vue';
import { useAuthStore } from '../stores/auth';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const isLogin = ref(true);
const email = ref('');
const password = ref('');
const fullName = ref('');
const errorMsg = ref('');

async function handleSubmit() {
    errorMsg.value = '';
    try {
        if (isLogin.value) {
            await authStore.login(email.value, password.value);
            router.push('/dashboard');
        } else {
            await authStore.register(email.value, password.value, fullName.value);
            // Auto login after register or ask to login
            isLogin.value = true;
            alert('Registration successful! Please login.');
        }
    } catch (e) {
        errorMsg.value = e.response?.data?.detail || 'An error occurred';
    }
}
</script>

<template>
    <div class="min-h-[80vh] flex items-center justify-center">
        <div class="card max-w-md w-full">
            <h2 class="text-3xl font-heading text-center mb-6 text-primary">
                {{ isLogin ? 'Welcome Back!' : 'Join the Fun!' }}
            </h2>
            
            <form @submit.prevent="handleSubmit" class="space-y-4">
                <div v-if="!isLogin">
                    <label class="block text-sm font-bold text-gray-600 mb-1">Full Name</label>
                    <input v-model="fullName" type="text" class="input-field" placeholder="Parent's Name" required />
                </div>
                
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Email Address</label>
                    <input v-model="email" type="email" class="input-field" placeholder="hello@example.com" required />
                </div>
                
                <div>
                    <label class="block text-sm font-bold text-gray-600 mb-1">Password</label>
                    <input v-model="password" type="password" class="input-field" placeholder="••••••••" required />
                </div>

                <div v-if="errorMsg" class="text-red-500 text-sm font-bold text-center">
                    {{ errorMsg }}
                </div>

                <button type="submit" class="btn-primary w-full text-lg">
                    {{ isLogin ? 'Log In' : 'Create Account' }}
                </button>
            </form>

            <div class="mt-6 text-center">
                <p class="text-gray-600">
                    {{ isLogin ? "Don't have an account?" : "Already have an account?" }}
                    <button @click="isLogin = !isLogin" class="text-secondary font-bold hover:underline">
                        {{ isLogin ? 'Sign Up' : 'Log In' }}
                    </button>
                </p>
            </div>
        </div>
    </div>
</template>
