<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useProfileStore } from '../stores/profile';
import { ArrowLeft, BookOpen, Award, Sparkles } from 'lucide-vue-next';
import api from '../api/axios';

const route = useRoute();
const router = useRouter();
const profileStore = useProfileStore();

const lesson = ref(null);
const loading = ref(true);
const showQuiz = ref(false);
const quizAnswers = ref({});
const quizResult = ref(null);
const submitting = ref(false);

const profile = computed(() => profileStore.currentProfile);

onMounted(async () => {
    if (!profile.value) {
        router.push('/dashboard');
        return;
    }
    await loadLesson();
});

async function loadLesson() {
    try {
        const response = await api.get(`/learning/${route.params.chapterId}/lesson`, {
            params: { profile_id: profile.value.id }
        });
        lesson.value = response.data;
    } catch (error) {
        console.error('Failed to load lesson:', error);
        alert('Failed to load lesson. Please try again.');
    } finally {
        loading.value = false;
    }
}

function startQuiz() {
    showQuiz.value = true;
    quizAnswers.value = {};
    quizResult.value = null;
}

function selectAnswer(questionIndex, answer) {
    quizAnswers.value[questionIndex] = answer;
}

async function submitQuiz() {
    submitting.value = true;
    try {
        const response = await api.post(`/learning/${route.params.chapterId}/submit-quiz`, quizAnswers.value, {
            params: { profile_id: profile.value.id }
        });
        quizResult.value = response.data;
        
        // Refresh profile to show updated XP/coins
        await profileStore.fetchProfiles();
        profileStore.loadCurrentProfile();
        
        // Check for newly earned badges
        try {
            const badgeResponse = await api.post(`/gamification/badges/check/${profile.value.id}`);
            if (badgeResponse.data.count > 0) {
                const badgeNames = badgeResponse.data.newly_earned.map(b => b.name).join(', ');
                setTimeout(() => {
                    alert(`🎉 New Badge${badgeResponse.data.count > 1 ? 's' : ''} Earned: ${badgeNames}!`);
                }, 1000);
            }
        } catch (badgeError) {
            console.error('Badge check failed:', badgeError);
        }
    } catch (error) {
        console.error('Failed to submit quiz:', error);
        alert('Failed to submit quiz. Please try again.');
    } finally {
        submitting.value = false;
    }
}

function goBack() {
    router.push(`/learn/${lesson.value.chapter.subject_id || route.params.id}`);
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
        <div class="max-w-4xl mx-auto">
            <!-- Header -->
            <div class="flex items-center justify-between mb-6">
                <button @click="goBack" class="flex items-center gap-2 text-gray-600 hover:text-primary font-bold">
                    <ArrowLeft size="20" />
                    Back
                </button>
                
                <div v-if="profile" class="card px-4 py-2 flex items-center gap-3">
                    <div class="text-center">
                        <div class="text-lg font-bold text-primary">{{ profile.xp }}</div>
                        <div class="text-xs text-gray-500">XP</div>
                    </div>
                    <div class="text-center">
                        <div class="text-lg font-bold text-accent-yellow">{{ profile.coins }}</div>
                        <div class="text-xs text-gray-500">Coins</div>
                    </div>
                </div>
            </div>

            <!-- Loading State -->
            <div v-if="loading" class="text-center py-20">
                <div class="animate-bounce text-6xl mb-4">📚</div>
                <p class="text-gray-500">Generating your lesson...</p>
            </div>

            <!-- Lesson Content -->
            <div v-else-if="lesson && !showQuiz && !quizResult">
                <div class="card mb-6">
                    <div class="flex items-start gap-4 mb-6">
                        <div class="text-5xl">📖</div>
                        <div>
                            <h1 class="text-3xl font-heading text-dark mb-2">{{ lesson.chapter.title }}</h1>
                            <p class="text-gray-600">{{ lesson.chapter.description }}</p>
                        </div>
                    </div>

                    <!-- Lesson Text (Markdown-style) -->
                    <div class="prose prose-lg max-w-none">
                        <div v-html="lesson.lesson.lesson_text.replace(/\n/g, '<br>')" class="text-gray-700 leading-relaxed whitespace-pre-wrap"></div>
                    </div>

                    <div class="mt-8 pt-6 border-t-2 border-gray-100">
                        <button @click="startQuiz" class="btn-primary text-lg flex items-center gap-2 mx-auto">
                            <Sparkles size="20" />
                            Take the Quiz!
                        </button>
                    </div>
                </div>
            </div>

            <!-- Quiz -->
            <div v-else-if="showQuiz && !quizResult">
                <div class="card">
                    <h2 class="text-2xl font-heading text-dark mb-6 flex items-center gap-2">
                        <BookOpen class="text-secondary" />
                        Quiz Time! 🎯
                    </h2>

                    <div class="space-y-6">
                        <div 
                            v-for="(question, index) in lesson.lesson.quiz.questions" 
                            :key="index"
                            class="p-4 bg-gray-50 rounded-2xl"
                        >
                            <p class="font-bold text-dark mb-3">{{ index + 1 }}. {{ question.question }}</p>
                            
                            <div class="space-y-2">
                                <button
                                    v-for="(text, letter) in question.options"
                                    :key="letter"
                                    @click="selectAnswer(index, letter)"
                                    :class="[
                                        'w-full text-left px-4 py-3 rounded-xl font-semibold transition-all',
                                        quizAnswers[index] === letter 
                                            ? 'bg-primary text-white shadow-lg scale-105' 
                                            : 'bg-white text-gray-700 hover:bg-gray-100'
                                    ]"
                                >
                                    {{ letter }}. {{ text }}
                                </button>
                            </div>
                        </div>
                    </div>

                    <div class="mt-8 pt-6 border-t-2 border-gray-100">
                        <button 
                            @click="submitQuiz" 
                            :disabled="Object.keys(quizAnswers).length < lesson.lesson.quiz.questions.length || submitting"
                            :class="[
                                'btn-primary text-lg flex items-center gap-2 mx-auto',
                                (Object.keys(quizAnswers).length < lesson.lesson.quiz.questions.length || submitting) && 'opacity-50 cursor-not-allowed'
                            ]"
                        >
                            <Award size="20" />
                            {{ submitting ? 'Submitting...' : 'Submit Answers' }}
                        </button>
                    </div>
                </div>
            </div>

            <!-- Quiz Result -->
            <div v-else-if="quizResult" class="card text-center">
                <div class="text-6xl mb-4">
                    {{ quizResult.percentage >= 80 ? '🎉' : quizResult.percentage >= 60 ? '👍' : '💪' }}
                </div>
                
                <h2 class="text-3xl font-heading text-dark mb-2">
                    {{ quizResult.percentage >= 80 ? 'Amazing!' : quizResult.percentage >= 60 ? 'Good Job!' : 'Keep Practicing!' }}
                </h2>
                
                <p class="text-xl text-gray-600 mb-6">
                    You scored {{ quizResult.score }} out of {{ quizResult.total }}
                </p>

                <div class="flex justify-center gap-6 mb-8">
                    <div class="card bg-primary/10 px-6 py-4">
                        <div class="text-3xl font-bold text-primary">+{{ quizResult.xp_earned }}</div>
                        <div class="text-sm text-gray-600">XP Earned</div>
                    </div>
                    <div class="card bg-accent-yellow/10 px-6 py-4">
                        <div class="text-3xl font-bold text-accent-orange">+{{ quizResult.coins_earned }}</div>
                        <div class="text-sm text-gray-600">Coins Earned</div>
                    </div>
                </div>

                <button @click="goBack" class="btn-secondary text-lg">
                    Continue Learning
                </button>
            </div>
        </div>
    </div>
</template>
