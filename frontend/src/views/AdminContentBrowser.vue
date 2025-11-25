<script setup>
import { ref, onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { BookOpen, Plus, Edit, Eye, Trash2, Sparkles } from 'lucide-vue-next';
import api from '../api/axios';

const router = useRouter();

const subjects = ref([]);
const selectedSubject = ref(null);
const chapters = ref([]);
const loading = ref(false);
const showCreateModal = ref(false);
const newChapterTitle = ref('');
const newChapterDescription = ref('');

onMounted(async () => {
    await loadSubjects();
});

async function loadSubjects() {
    loading.value = true;
    try {
        const response = await api.get('/curriculum/');
        subjects.value = response.data;
    } catch (error) {
        console.error('Failed to load subjects:', error);
    } finally {
        loading.value = false;
    }
}

async function selectSubject(subject) {
    selectedSubject.value = subject;
    loading.value = true;
    try {
        const response = await api.get(`/admin/subjects/${subject.id}/chapters`);
        chapters.value = response.data;
    } catch (error) {
        console.error('Failed to load chapters:', error);
        // Fallback to subject's chapters
        chapters.value = subject.chapters || [];
    } finally {
        loading.value = false;
    }
}

function editChapter(chapter) {
    router.push(`/admin/content-editor/${chapter.id}`);
}

function viewContent(chapter) {
    router.push(`/lesson/${chapter.id}`);
}

async function createChapter() {
    if (!newChapterTitle.value || !selectedSubject.value) {
        alert('Please enter a chapter title');
        return;
    }
    
    try {
        const response = await api.post(`/admin/subjects/${selectedSubject.value.id}/chapters`, {
            title: newChapterTitle.value,
            description: newChapterDescription.value,
            order_index: chapters.value.length + 1
        });
        
        chapters.value.push(response.data);
        newChapterTitle.value = '';
        newChapterDescription.value = '';
        showCreateModal.value = false;
        alert('Chapter created successfully!');
    } catch (error) {
        console.error('Failed to create chapter:', error);
        alert('Failed to create chapter. Please try again.');
    }
}

async function deleteChapter(chapter) {
    if (!confirm(`Delete "${chapter.title}"?`)) return;
    
    try {
        await api.delete(`/admin/chapters/${chapter.id}`);
        chapters.value = chapters.value.filter(c => c.id !== chapter.id);
        alert('Chapter deleted successfully!');
    } catch (error) {
        console.error('Failed to delete chapter:', error);
        alert('Failed to delete chapter. Please try again.');
    }
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
        <div class="max-w-7xl mx-auto">
            <!-- Header -->
            <div class="mb-8">
                <h1 class="text-4xl font-heading text-dark mb-2">Content Browser</h1>
                <p class="text-xl text-gray-600">Navigate and manage educational content</p>
            </div>

            <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <!-- Subjects List -->
                <div class="card">
                    <h2 class="text-2xl font-heading text-dark mb-4 flex items-center gap-2">
                        <BookOpen class="text-primary" />
                        Subjects
                    </h2>

                    <div v-if="loading && !selectedSubject" class="text-center py-10">
                        <div class="animate-spin text-4xl mb-2">⏳</div>
                        <p class="text-gray-500">Loading...</p>
                    </div>

                    <div v-else class="space-y-2">
                        <div
                            v-for="subject in subjects"
                            :key="subject.id"
                            @click="selectSubject(subject)"
                            :class="[
                                'p-4 rounded-xl cursor-pointer transition-all',
                                selectedSubject?.id === subject.id
                                    ? 'bg-primary text-white shadow-lg'
                                    : 'bg-gray-50 hover:bg-gray-100'
                            ]"
                        >
                            <div class="font-bold">{{ subject.name }}</div>
                            <div :class="selectedSubject?.id === subject.id ? 'text-white/80' : 'text-gray-500'" class="text-sm">
                                Grade {{ subject.grade_level }} • {{ subject.chapters?.length || 0 }} chapters
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Chapters List -->
                <div class="lg:col-span-2 card">
                    <div class="flex items-center justify-between mb-4">
                        <h2 class="text-2xl font-heading text-dark flex items-center gap-2">
                            <Edit class="text-secondary" />
                            {{ selectedSubject ? selectedSubject.name : 'Select a Subject' }}
                        </h2>
                        <button
                            v-if="selectedSubject"
                            @click="showCreateModal = true"
                            class="btn-secondary flex items-center gap-2"
                        >
                            <Plus size="20" />
                            New Chapter
                        </button>
                    </div>

                    <div v-if="!selectedSubject" class="text-center py-20">
                        <div class="text-6xl mb-4">📚</div>
                        <p class="text-gray-500">Select a subject to view chapters</p>
                    </div>

                    <div v-else-if="loading" class="text-center py-20">
                        <div class="animate-spin text-4xl mb-2">⏳</div>
                        <p class="text-gray-500">Loading chapters...</p>
                    </div>

                    <div v-else-if="chapters.length === 0" class="text-center py-20">
                        <div class="text-6xl mb-4">📝</div>
                        <p class="text-gray-500 mb-4">No chapters yet</p>
                        <button @click="showCreateModal = true" class="btn-primary">
                            Create First Chapter
                        </button>
                    </div>

                    <div v-else class="space-y-3">
                        <div
                            v-for="(chapter, index) in chapters"
                            :key="chapter.id"
                            class="p-4 bg-gray-50 rounded-xl hover:bg-gray-100 transition-all"
                        >
                            <div class="flex items-start justify-between">
                                <div class="flex-1">
                                    <div class="flex items-center gap-3 mb-2">
                                        <div class="w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-bold text-sm">
                                            {{ chapter.order_index || index + 1 }}
                                        </div>
                                        <h3 class="text-lg font-bold text-dark">{{ chapter.title }}</h3>
                                    </div>
                                    <p class="text-gray-600 text-sm ml-11">{{ chapter.description || 'No description' }}</p>
                                </div>

                                <div class="flex items-center gap-2 ml-4">
                                    <button
                                        @click="editChapter(chapter)"
                                        class="p-2 rounded-lg bg-white hover:bg-primary hover:text-white transition-colors"
                                        title="Edit Content"
                                    >
                                        <Edit size="18" />
                                    </button>
                                    <button
                                        @click="viewContent(chapter)"
                                        class="p-2 rounded-lg bg-white hover:bg-secondary hover:text-white transition-colors"
                                        title="Preview"
                                    >
                                        <Eye size="18" />
                                    </button>
                                    <button
                                        @click="deleteChapter(chapter)"
                                        class="p-2 rounded-lg bg-white hover:bg-red-500 hover:text-white transition-colors"
                                        title="Delete"
                                    >
                                        <Trash2 size="18" />
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Create Chapter Modal -->
        <div v-if="showCreateModal" class="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div class="card max-w-2xl w-full">
                <h2 class="text-2xl font-heading text-dark mb-4 flex items-center gap-2">
                    <Plus class="text-primary" />
                    Create New Chapter
                </h2>

                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-bold text-gray-600 mb-2">Chapter Title</label>
                        <input
                            v-model="newChapterTitle"
                            type="text"
                            placeholder="e.g., Introduction to Algebra"
                            class="input-field bg-white"
                        />
                    </div>

                    <div>
                        <label class="block text-sm font-bold text-gray-600 mb-2">Description</label>
                        <textarea
                            v-model="newChapterDescription"
                            rows="3"
                            placeholder="Brief description of what students will learn..."
                            class="input-field bg-white resize-none"
                        ></textarea>
                    </div>

                    <div class="flex gap-3 pt-4">
                        <button @click="createChapter" class="btn-primary flex-1">
                            Create Chapter
                        </button>
                        <button @click="showCreateModal = false" class="btn-secondary flex-1">
                            Cancel
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
