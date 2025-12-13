<template>
  <div class="min-h-screen bg-slate-900 text-white p-6">
    <div class="max-w-6xl mx-auto">
      <header class="flex items-center justify-between mb-8">
        <div>
          <h1 class="text-3xl font-bold font-display text-transparent bg-clip-text bg-gradient-to-r from-teal-400 to-blue-500">
            Lesson Editor
          </h1>
          <p class="text-slate-400 mt-1">Edit content for Grade 4 Curriculum</p>
        </div>
        <button @click="$router.push('/admin/dashboard')" class="text-slate-400 hover:text-white transition">
          Back to Dashboard
        </button>
      </header>

      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin text-4xl mb-4">🌀</div>
        <p class="text-slate-400">Loading content...</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-8">
        <!-- Lesson Editor -->
        <div class="glass-panel p-6 rounded-2xl relative overflow-hidden">
          <div class="absolute inset-0 bg-blue-500/10 pointer-events-none"></div>
          <div class="relative z-10">
            <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
              <span class="text-2xl">📖</span> Lesson Content (Markdown)
            </h2>
            <textarea
              v-if="lessonBlock"
              v-model="lessonContent.markdown"
              class="w-full h-[600px] bg-slate-950/50 border border-slate-700 rounded-lg p-4 font-mono text-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition outline-none resize-none"
            ></textarea>
            <div v-else class="text-slate-500 italic p-4 text-center border border-dashed border-slate-700 rounded-lg">
              No lesson content found for this chapter.
            </div>
            
            <div class="mt-4 flex justify-end">
              <button 
                @click="saveLesson" 
                :disabled="savingLesson || !lessonBlock"
                class="px-6 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-full font-bold shadow-lg shadow-blue-900/20 transition flex items-center gap-2"
              >
                <span v-if="savingLesson" class="animate-spin">⌛</span>
                {{ savingLesson ? 'Saving...' : 'Save Lesson' }}
              </button>
            </div>
          </div>
        </div>

        <!-- Quiz Editor -->
        <div class="glass-panel p-6 rounded-2xl relative overflow-hidden">
          <div class="absolute inset-0 bg-purple-500/10 pointer-events-none"></div>
          <div class="relative z-10">
             <h2 class="text-xl font-bold mb-4 flex items-center gap-2">
              <span class="text-2xl">🧩</span> Quiz Questions (JSON)
            </h2>
             <textarea
              v-if="quizBlock"
              v-model="quizContentString"
              class="w-full h-[600px] bg-slate-950/50 border border-slate-700 rounded-lg p-4 font-mono text-sm focus:border-purple-500 focus:ring-1 focus:ring-purple-500 transition outline-none resize-none"
            ></textarea>
             <div v-else class="text-slate-500 italic p-4 text-center border border-dashed border-slate-700 rounded-lg">
              No quiz content found.
            </div>

            <div class="mt-4 flex justify-end">
              <button 
                @click="saveQuiz" 
                :disabled="savingQuiz || !quizBlock"
                class="px-6 py-2 bg-purple-600 hover:bg-purple-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-full font-bold shadow-lg shadow-purple-900/20 transition flex items-center gap-2"
              >
                <span v-if="savingQuiz" class="animate-spin">⌛</span>
                {{ savingQuiz ? 'Saving...' : 'Save Quiz' }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'

import api from '../api/axios'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const authStore = useAuthStore()
const chapterId = route.params.chapterId

const loading = ref(true)
const blocks = ref([])

// Computed Helper to access specific blocks
const lessonBlock = computed(() => blocks.value.find(b => b.block_type === 'lesson'))
const quizBlock = computed(() => blocks.value.find(b => b.block_type === 'quiz'))

// Local state for editing
const lessonContent = ref({ markdown: '' })
const quizContentString = ref('')

const savingLesson = ref(false)
const savingQuiz = ref(false)

// Init
onMounted(async () => {
    await fetchContent()
})

const fetchContent = async () => {
    try {
        loading.value = true
        const response = await api.get(`/admin/chapters/${chapterId}/content`)
        blocks.value = response.data
        
        if (lessonBlock.value) {
            lessonContent.value = { ...lessonBlock.value.content_data }
        }
        
        if (quizBlock.value) {
            // Pretty print JSON
            quizContentString.value = JSON.stringify(quizBlock.value.content_data, null, 2)
        }

    } catch (e) {
        console.error("Failed to load content", e)
        alert("Failed to load content. Check console.")
    } finally {
        loading.value = false
    }
}

const saveLesson = async () => {
    if (!lessonBlock.value) return
    try {
        savingLesson.value = true
        await api.put(`/admin/content-blocks/${lessonBlock.value.id}`, {
            content_data: lessonContent.value
        })
        alert("Lesson saved successfully! ✅")
    } catch (e) {
        console.error(e)
        alert("Failed to save lesson.")
    } finally {
        savingLesson.value = false
    }
}

const saveQuiz = async () => {
    if (!quizBlock.value) return
    try {
        // Validate JSON
        const json = JSON.parse(quizContentString.value)
        savingQuiz.value = true
        
        await api.put(`/admin/content-blocks/${quizBlock.value.id}`, {
            content_data: json
        })
        alert("Quiz saved successfully! ✅")
    } catch (e) {
        console.error(e)
        if (e instanceof SyntaxError) {
            alert("Invalid JSON format! Please check your syntax.")
        } else {
            alert("Failed to save quiz.")
        }
    } finally {
        savingQuiz.value = false
    }
}
</script>

<style scoped>
.glass-panel {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.1);
}
.font-display {
  font-family: 'Fredoka One', cursive;
}
</style>
