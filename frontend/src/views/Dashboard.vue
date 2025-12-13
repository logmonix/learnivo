<script setup>
import { ref, onMounted } from 'vue';
import { useProfileStore } from '../stores/profile';
import { Plus, User, X } from 'lucide-vue-next';
import AdminImageGallery from '../components/AdminImageGallery.vue';

const profileStore = useProfileStore();
const showAddModal = ref(false);

// Form Data
const newProfileName = ref('');
const newProfileGrade = ref(5);

onMounted(async () => {
    await profileStore.fetchProfiles();
    profileStore.loadCurrentProfile();
});

async function handleCreateProfile() {
    try {
        await profileStore.createProfile({
            display_name: newProfileName.value,
            current_grade: newProfileGrade.value,
            avatar_url: 'default' // Placeholder
        });
        showAddModal.value = false;
        newProfileName.value = '';
    } catch (e) {
        alert('Failed to create profile');
    }
}
</script>

<template>
    <div class="p-6 md:p-10">
        <h1 class="text-4xl font-heading text-primary mb-2">Who is learning today?</h1>
        <p class="text-xl text-gray-600 mb-8">Select a profile to jump back into the adventure!</p>
        
        <div v-if="profileStore.loading" class="text-center py-10">
            <div class="animate-bounce text-4xl">🦁</div>
            <p class="text-gray-500 mt-2">Loading profiles...</p>
        </div>

        <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
            <!-- Profile Cards -->
            <div 
                v-for="profile in profileStore.profiles" 
                :key="profile.id"
                @click="() => { profileStore.selectProfile(profile); $router.push('/student'); }"
                class="card group cursor-pointer hover:scale-105 transition-transform border-2 border-transparent hover:border-primary relative overflow-hidden"
            >
                <div class="absolute top-0 right-0 bg-accent-yellow text-xs font-bold px-2 py-1 rounded-bl-xl">
                    Lvl {{ Math.floor(profile.xp / 100) + 1 }}
                </div>
                
                <div class="flex flex-col items-center py-4">
                    <div class="w-24 h-24 bg-primary/10 rounded-full mb-4 flex items-center justify-center text-primary group-hover:bg-primary group-hover:text-white transition-colors">
                        <User size="48" />
                    </div>
                    <h3 class="text-2xl font-bold text-dark">{{ profile.display_name }}</h3>
                    <p class="text-gray-500 font-bold">Grade {{ profile.current_grade }}</p>
                    <div class="mt-4 flex gap-2 text-sm font-bold text-gray-400">
                        <span>🪙 {{ profile.coins }}</span>
                        <span>⭐ {{ profile.xp }}</span>
                    </div>
                </div>
            </div>

            <!-- Add Kid Button -->
            <div 
                @click="showAddModal = true"
                class="card flex flex-col items-center justify-center cursor-pointer border-dashed border-4 border-gray-200 hover:border-primary hover:bg-primary/5 transition-all min-h-[200px]"
            >
                <div class="w-16 h-16 rounded-full bg-gray-100 flex items-center justify-center text-gray-400 mb-2 group-hover:bg-primary group-hover:text-white">
                    <Plus size="32" />
                </div>
                <h3 class="text-xl font-bold text-gray-500">Add Kid</h3>
            </div>
        </div>
    <AdminImageGallery />

        <!-- Add Profile Modal -->
        <div v-if="showAddModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div class="bg-white rounded-3xl p-8 max-w-md w-full shadow-2xl relative animate-fade-in">
                <button @click="showAddModal = false" class="absolute top-4 right-4 text-gray-400 hover:text-red-500">
                    <X />
                </button>
                
                <h2 class="text-2xl font-heading text-primary mb-6">New Adventurer</h2>
                
                <form @submit.prevent="handleCreateProfile" class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-gray-600 mb-1">Name</label>
                        <input v-model="newProfileName" type="text" class="input-field" placeholder="e.g. Leo" required />
                    </div>
                    
                    <div>
                        <label class="block text-sm font-bold text-gray-600 mb-1">Grade</label>
                        <select v-model="newProfileGrade" class="input-field bg-white">
                            <option v-for="i in 12" :key="i" :value="i">Grade {{ i }}</option>
                        </select>
                    </div>

                    <div class="pt-4">
                        <button type="submit" class="btn-primary w-full">
                            Create Profile
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<style scoped>
.animate-fade-in {
    animation: fadeIn 0.2s ease-out;
}
@keyframes fadeIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}
</style>
