<script setup>
import { ref, onMounted, computed } from 'vue';
import { useProfileStore } from '../stores/profile';
import { useRouter } from 'vue-router';
import { BookOpen, Sparkles, Trophy, Zap } from 'lucide-vue-next';
import api from '../api/axios';

const profileStore = useProfileStore();
const router = useRouter();

const subjects = ref([]);
const loading = ref(false);
const generatingSubject = ref(null);

const profile = computed(() => profileStore.currentProfile);

onMounted(async () => {
    if (!profile.value) {
        router.push('/dashboard');
        return;
    }
    await loadSubjects();
});

async function loadSubjects() {
    loading.value = true;
    try {
        const response = await api.get(`/curriculum/?grade=${profile.value.current_grade}`);
        subjects.value = response.data;
    } catch (error) {
        console.error('Failed to load subjects:', error);
    } finally {
        loading.value = false;
    }
}

async function generateSubject(subjectName) {
    generatingSubject.value = subjectName;
    try {
        const response = await api.post('/curriculum/generate', {
            grade_level: profile.value.current_grade,
            subject_name: subjectName
        });
        subjects.value.push(response.data);
    } catch (error) {
        console.error('Failed to generate subject:', error);
        alert('Failed to generate curriculum. Please try again.');
    } finally {
        generatingSubject.value = null;
    }
}

function viewSubject(subject) {
    router.push(`/learn/${subject.id}`);
}

const suggestedSubjects = ['Mathematics', 'Science', 'English', 'History', 'Geography'];
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
        <!-- Header -->
        <div class="max-w-6xl mx-auto mb-8">
            <div class="flex items-center justify-between">
                <div>
                    <h1 class="text-4xl font-heading text-dark mb-2">
                        Hey {{ profile?.display_name }}! 👋
                    </h1>
                    <p class="text-xl text-gray-600">Ready to learn something awesome today?</p>
                </div>
                
                <div class="card px-6 py-4 flex items-center gap-4">
                    <div class="text-center">
                        <div class="text-2xl font-bold text-primary">{{ profile?.xp }}</div>
                        <div class="text-xs text-gray-500">XP</div>
                    </div>
                    <div class="text-center">
                        <div class="text-2xl font-bold text-accent-yellow">{{ profile?.coins }}</div>
                        <div class="text-xs text-gray-500">Coins</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Subjects Grid -->
        <div class="max-w-6xl mx-auto">
            <h2 class="text-2xl font-heading text-dark mb-4 flex items-center gap-2">
                <BookOpen class="text-primary" />
                Your Subjects
            </h2>

            <div v-if="loading" class="text-center py-20">
                <div class="animate-bounce text-6xl mb-4">📚</div>
                <p class="text-gray-500">Loading your subjects...</p>
            </div>

            <div v-else class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Existing Subjects -->
                <div 
                    v-for="subject in subjects" 
                    :key="subject.id"
                    @click="viewSubject(subject)"
                    class="card group cursor-pointer hover:scale-105 transition-all border-2 border-transparent hover:border-primary relative overflow-hidden"
                >
                    <div class="absolute top-0 right-0 w-20 h-20 bg-primary/10 rounded-full -mr-10 -mt-10"></div>
                    
                    <div class="relative">
                        <div class="text-4xl mb-3">📖</div>
                        <h3 class="text-2xl font-bold text-dark mb-2">{{ subject.name }}</h3>
                        <p class="text-gray-600 text-sm mb-4">{{ subject.chapters?.length || 0 }} chapters</p>
                        
                        <div class="flex items-center gap-2 text-sm font-bold text-primary">
                            <Zap size="16" />
                            Start Learning
                        </div>
                    </div>
                </div>

                <!-- Generate New Subject Cards -->
                <div 
                    v-for="suggestedSubject in suggestedSubjects.filter(s => !subjects.find(sub => sub.name === s))" 
                    :key="suggestedSubject"
                    @click="generateSubject(suggestedSubject)"
                    :class="{'opacity-50 pointer-events-none': generatingSubject === suggestedSubject}"
                    class="card group cursor-pointer hover:scale-105 transition-all border-2 border-dashed border-gray-300 hover:border-secondary relative overflow-hidden"
                >
                    <div v-if="generatingSubject === suggestedSubject" class="absolute inset-0 bg-white/90 flex items-center justify-center z-10">
                        <div class="text-center">
                            <Sparkles class="animate-spin text-secondary mx-auto mb-2" size="32" />
                            <p class="text-sm font-bold text-secondary">Generating...</p>
                        </div>
                    </div>
                    
                    <div class="relative opacity-60 group-hover:opacity-100 transition-opacity">
                        <div class="text-4xl mb-3">✨</div>
                        <h3 class="text-2xl font-bold text-dark mb-2">{{ suggestedSubject }}</h3>
                        <p class="text-gray-600 text-sm mb-4">Click to generate curriculum</p>
                        
                        <div class="flex items-center gap-2 text-sm font-bold text-secondary">
                            <Sparkles size="16" />
                            AI Generate
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
