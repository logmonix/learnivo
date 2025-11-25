<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { ArrowLeft, MapPin, Lock, CheckCircle } from 'lucide-vue-next';
import api from '../api/axios';

const route = useRoute();
const router = useRouter();

const subject = ref(null);
const loading = ref(true);

onMounted(async () => {
    await loadSubject();
});

async function loadSubject() {
    try {
        const response = await api.get(`/curriculum/?grade=5`);
        const subjects = response.data;
        subject.value = subjects.find(s => s.id === route.params.id);
        
        if (!subject.value) {
            router.push('/student');
        }
    } catch (error) {
        console.error('Failed to load subject:', error);
    } finally {
        loading.value = false;
    }
}

function startChapter(chapter) {
    // Always use the chapter UUID, not order_index
    router.push(`/lesson/${chapter.id}`);
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
        <div class="max-w-4xl mx-auto">
            <!-- Back Button -->
            <button @click="router.push('/student')" class="flex items-center gap-2 text-gray-600 hover:text-primary mb-6 font-bold">
                <ArrowLeft size="20" />
                Back to Subjects
            </button>

            <div v-if="loading" class="text-center py-20">
                <div class="animate-bounce text-6xl mb-4">📚</div>
                <p class="text-gray-500">Loading chapters...</p>
            </div>

            <div v-else-if="subject">
                <!-- Subject Header -->
                <div class="card mb-8">
                    <div class="flex items-start gap-4">
                        <div class="text-6xl">📖</div>
                        <div class="flex-1">
                            <h1 class="text-4xl font-heading text-dark mb-2">{{ subject.name }}</h1>
                            <p class="text-gray-600">{{ subject.chapters?.length || 0 }} exciting chapters to explore!</p>
                        </div>
                    </div>
                </div>

                <!-- Chapter Map -->
                <div class="space-y-4">
                    <h2 class="text-2xl font-heading text-dark flex items-center gap-2">
                        <MapPin class="text-secondary" />
                        Your Learning Journey
                    </h2>

                    <div class="relative">
                        <!-- Path Line -->
                        <div class="absolute left-8 top-0 bottom-0 w-1 bg-gradient-to-b from-primary via-secondary to-accent-pink opacity-20"></div>

                        <!-- Chapters -->
                        <div class="space-y-6">
                            <div 
                                v-for="(chapter, index) in subject.chapters" 
                                :key="chapter.id || index"
                                class="relative"
                            >
                                <div class="flex items-start gap-4">
                                    <!-- Chapter Number Badge -->
                                    <div class="relative z-10 w-16 h-16 rounded-full bg-white border-4 border-primary flex items-center justify-center font-heading text-2xl text-primary shadow-lg">
                                        {{ chapter.order_index || index + 1 }}
                                    </div>

                                    <!-- Chapter Card -->
                                    <div 
                                        @click="startChapter(chapter)"
                                        class="flex-1 card cursor-pointer hover:scale-102 transition-all border-2 border-transparent hover:border-primary group"
                                    >
                                        <div class="flex items-start justify-between">
                                            <div class="flex-1">
                                                <h3 class="text-xl font-bold text-dark mb-2 group-hover:text-primary transition-colors">
                                                    {{ chapter.title }}
                                                </h3>
                                                <p class="text-gray-600 text-sm">{{ chapter.description }}</p>
                                            </div>
                                            
                                            <!-- Status Icon -->
                                            <div class="ml-4">
                                                <div class="w-10 h-10 rounded-full bg-gray-100 flex items-center justify-center">
                                                    <Lock size="20" class="text-gray-400" />
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
.hover\:scale-102:hover {
    transform: scale(1.02);
}
</style>
