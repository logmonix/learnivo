<!-- Public Image Gallery – Premium UI for students to browse images -->
<script setup>
import { ref, onMounted } from 'vue';
import { fetchImages, getImageUrl } from '../api/imageService';

const images = ref([]);
const loading = ref(false);
const page = ref(1);
const pageSize = ref(20);
const total = ref(0);

async function loadImages() {
  loading.value = true;
  try {
    const resp = await fetchImages(page.value, pageSize.value);
    images.value = resp.data.results || resp.data;
    total.value = resp.data.total || resp.data.length;
  } catch (e) {
    console.error('Failed to load images', e);
    alert('Could not load images');
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadImages();
});
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-heading text-dark mb-6">Image Gallery</h1>

      <div v-if="loading" class="flex justify-center py-10">
        <RefreshCw class="animate-spin text-4xl text-primary" />
      </div>

      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div
          v-for="img in images"
          :key="img.id"
          class="rounded-xl overflow-hidden shadow-lg bg-white/80 backdrop-filter backdrop-blur-sm"
        >
          <img
            :src="getImageUrl(img.id)"
            alt="Image"
            class="w-full h-48 object-cover"
          />
        </div>
      </div>

      <!-- Simple pagination -->
      <div class="mt-8 flex justify-center items-center gap-4">
        <button
          @click="if (page > 1) { page--; loadImages(); }"
          :disabled="page === 1"
          class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >Prev</button>
        <span>Page {{ page }}</span>
        <button
          @click="if (images.length === pageSize) { page++; loadImages(); }"
          :disabled="images.length < pageSize"
          class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50"
        >Next</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Optional subtle glass‑morphism for cards */
.card {
  background: rgba(255, 255, 255, 0.12);
  backdrop-filter: blur(12px);
  border: 1px solid rgba(255, 255, 255, 0.18);
}
</style>
