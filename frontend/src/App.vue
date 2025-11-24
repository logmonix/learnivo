```vue
<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { BookOpen, Star, User, Menu } from 'lucide-vue-next'
import { useAuthStore } from './stores/auth' // Added import for auth store

const router = useRouter()
const isMenuOpen = ref(false)
const authStore = useAuthStore() // Initialize auth store
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <!-- Navbar -->
    <nav class="bg-white shadow-sm border-b-4 border-gray-100 py-4 px-6 sticky top-0 z-50">
      <div class="max-w-7xl mx-auto flex justify-between items-center">
        <div class="flex items-center gap-3 cursor-pointer" @click="router.push('/')">
          <div class="bg-primary p-2 rounded-xl text-white">
            <BookOpen size="28" stroke-width="3" />
          </div>
          <span class="text-2xl font-heading font-bold text-primary tracking-wide">Learnivo</span>
        </div>

        <!-- Desktop Menu -->
        <div class="hidden md:flex items-center gap-6">
          <button @click="router.push('/student')" class="flex items-center gap-2 font-bold text-gray-600 hover:text-primary transition-colors">
            <Star class="text-accent-yellow fill-current" />
            Daily Mix
          </button>
          <button @click="router.push('/profile')" class="flex items-center gap-2 font-bold text-gray-600 hover:text-primary transition-colors">
            <User />
            Profile
          </button>
          <button v-if="authStore.isAdmin" @click="router.push('/admin')" class="btn-primary">
            Admin
          </button>
        </div>

        <!-- Mobile Menu Button -->
        <button class="md:hidden text-gray-600" @click="isMenuOpen = !isMenuOpen">
          <Menu size="32" />
        </button>
      </div>
    </nav>

    <!-- Main Content -->
    <main class="flex-grow container mx-auto px-4 py-8">
      <router-view></router-view>
    </main>

    <!-- Footer -->
    <footer class="bg-dark text-white py-10 mt-auto">
      <div class="container mx-auto px-4 text-center">
        <p class="font-heading text-xl opacity-80">Made with ❤️ for curious minds</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
</style>
