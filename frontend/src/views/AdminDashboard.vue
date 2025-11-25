<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { BarChart3, BookOpen, Users, Award, Plus, RefreshCw } from 'lucide-vue-next';
import api from '../api/axios';

const router = useRouter();

const stats = ref({
    total_subjects: 0,
    total_chapters: 0,
    total_students: 0,
    total_lessons_completed: 0
});

const loading = ref(false);
const bulkGenerating = ref(false);
const selectedGrade = ref(5);
const selectedSubjects = ref([]);

const availableSubjects = ['Mathematics', 'Science', 'English', 'History', 'Geography', 'Art', 'Music', 'Physical Education'];

onMounted(async () => {
    await loadStats();
});

async function loadStats() {
    loading.value = true;
    try {
        const response = await api.get('/admin/stats');
        stats.value = response.data;
    } catch (error) {
        console.error('Failed to load stats:', error);
    } finally {
        loading.value = false;
    }
}

async function bulkGenerate() {
    if (selectedSubjects.value.length === 0) {
        alert('Please select at least one subject');
        return;
    }
    
    bulkGenerating.value = true;
    try {
        await api.post('/admin/bulk-generate', {
            grade_level: selectedGrade.value,
            subject_names: selectedSubjects.value
        });
        alert(`Successfully generated ${selectedSubjects.value.length} subjects!`);
        selectedSubjects.value = [];
        await loadStats();
    } catch (error) {
        console.error('Failed to bulk generate:', error);
        alert('Failed to generate subjects. Please try again.');
    } finally {
        bulkGenerating.value = false;
    }
}

function toggleSubject(subject) {
    const index = selectedSubjects.value.indexOf(subject);
    if (index > -1) {
        selectedSubjects.value.splice(index, 1);
    } else {
        selectedSubjects.value.push(subject);
    }
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="mb-8">
                <h1 class="text-4xl font-heading text-dark mb-2">Admin Dashboard</h1>
                <p class="text-xl text-gray-600">Manage content and monitor platform activity</p>
            </div>

            <!-- Stats Grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
                <div class="card">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-primary/10 rounded-xl flex items-center justify-center">
                            <BookOpen class="text-primary" size="24" />
                        </div>
                        <div>
                            <div class="text-3xl font-bold text-dark">{{ stats.total_subjects }}</div>
                            <div class="text-sm text-gray-600">Subjects</div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-secondary/10 rounded-xl flex items-center justify-center">
                            <BarChart3 class="text-secondary" size="24" />
                        </div>
                        <div>
                            <div class="text-3xl font-bold text-dark">{{ stats.total_chapters }}</div>
                            <div class="text-sm text-gray-600">Chapters</div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-accent-yellow/10 rounded-xl flex items-center justify-center">
                            <Users class="text-accent-orange" size="24" />
                        </div>
                        <div>
                            <div class="text-3xl font-bold text-dark">{{ stats.total_students }}</div>
                            <div class="text-sm text-gray-600">Students</div>
                        </div>
                    </div>
                </div>

                <div class="card">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-accent-pink/10 rounded-xl flex items-center justify-center">
                            <Award class="text-accent-pink" size="24" />
                        </div>
                        <div>
                            <div class="text-3xl font-bold text-dark">{{ stats.total_lessons_completed }}</div>
                            <div class="text-sm text-gray-600">Lessons Completed</div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Bulk Generation Tool -->
            <div class="card mb-8">
                <h2 class="text-2xl font-heading text-dark mb-4 flex items-center gap-2">
                    <Plus class="text-primary" />
                    Bulk Content Generation
                </h2>

                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-gray-600 mb-2">Grade Level</label>
                        <select v-model="selectedGrade" class="input-field bg-white max-w-xs">
                            <option v-for="i in 12" :key="i" :value="i">Grade {{ i }}</option>
                        </select>
                    </div>

                    <div>
                        <label class="block text-sm font-bold text-gray-600 mb-2">Select Subjects to Generate</label>
                        <div class="grid grid-cols-2 md:grid-cols-4 gap-3">
                            <button
                                v-for="subject in availableSubjects"
                                :key="subject"
                                @click="toggleSubject(subject)"
                                :class="[
                                    'px-4 py-3 rounded-xl font-semibold transition-all',
                                    selectedSubjects.includes(subject)
                                        ? 'bg-primary text-white shadow-lg'
                                        : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
                                ]"
                            >
                                {{ subject }}
                            </button>
                        </div>
                    </div>

                    <div class="pt-4">
                        <button
                            @click="bulkGenerate"
                            :disabled="bulkGenerating || selectedSubjects.length === 0"
                            :class="[
                                'btn-primary flex items-center gap-2',
                                (bulkGenerating || selectedSubjects.length === 0) && 'opacity-50 cursor-not-allowed'
                            ]"
                        >
                            <RefreshCw :class="{ 'animate-spin': bulkGenerating }" size="20" />
                            {{ bulkGenerating ? 'Generating...' : `Generate ${selectedSubjects.length} Subject${selectedSubjects.length !== 1 ? 's' : ''}` }}
                        </button>
                    </div>
                </div>
            </div>

            <!-- Quick Actions -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                <div class="card cursor-pointer hover:scale-105 transition-transform" @click="router.push('/student')">
                    <h3 class="text-xl font-bold text-dark mb-2">Preview Student View</h3>
                    <p class="text-gray-600">See the platform as a student</p>
                </div>

                <div class="card cursor-pointer hover:scale-105 transition-transform" @click="router.push('/admin/content')">
                    <h3 class="text-xl font-bold text-dark mb-2">Content Library</h3>
                    <p class="text-gray-600">View and edit all content</p>
                </div>

                <div class="card cursor-pointer hover:scale-105 transition-transform opacity-50">
                    <h3 class="text-xl font-bold text-dark mb-2">Analytics</h3>
                    <p class="text-gray-600">Detailed engagement reports (Coming Soon)</p>
                </div>
            </div>
        </div>
    </div>
</template>
