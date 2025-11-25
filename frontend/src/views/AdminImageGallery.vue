<!-- Admin Image Gallery – Premium UI for managing images -->
<script setup>
import { ref, onMounted } from 'vue';
import { fetchImages, uploadImages, deleteImage, getImageUrl } from '../api/imageService';
import { useAuthStore } from '../stores/auth';
import { RefreshCw, Plus, Trash2 } from 'lucide-vue-next';

// Ensure only admins can see this page (guard also in router)
const authStore = useAuthStore();
if (!authStore.isAdmin) {
  // Redirect if somehow accessed
  window.location.href = '/dashboard';
}

const images = ref([]);
const loading = ref(false);
const uploading = ref(false);
const page = ref(1);
const pageSize = ref(20);
const total = ref(0);

async function loadImages() {
  loading.value = true;
  try {
    const resp = await fetchImages(page.value, pageSize.value);
    images.value = resp.data.results || resp.data; // API returns {results: []}
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

function handleFileSelect(event) {
  const files = event.target.files || event.dataTransfer.files;
  if (!files.length) return;
  uploading.value = true;
  uploadImages(files, (percent) => {
    // optional progress UI – could be added later
  })
    .then(() => {
      alert('Upload successful');
      loadImages();
    })
    .catch((e) => {
      console.error('Upload error', e);
      alert('Upload failed');
    })
    .finally(() => {
      uploading.value = false;
    });
}

function confirmDelete(imageId) {
  if (confirm('Delete this image? This action cannot be undone.')) {
    deleteImage(imageId)
      .then(() => {
        alert('Image deleted');
        loadImages();
      })
      .catch((e) => {
        console.error('Delete error', e);
        alert('Failed to delete image');
      });
  }
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
    <div class="max-w-7xl mx-auto">
      <h1 class="text-4xl font-heading text-dark mb-6">Image Library</h1>

      <!-- Upload Section -->
      <div class="mb-8 p-6 bg-white/80 rounded-xl shadow-md backdrop-filter backdrop-blur-sm">
        <div class="flex items-center gap-4">
          <Plus class="text-primary" size="24" />
          <h2 class="text-2xl font-heading text-dark">Upload Images</h2>
        </div>
        <div class="mt-4">
          <input
            type="file"
            multiple
            accept="image/*"
            @change="handleFileSelect"
            class="hidden"
            id="image-upload-input"
          />
          <label
            for="image-upload-input"
            class="inline-flex items-center px-4 py-2 bg-primary text-white rounded-lg cursor-pointer hover:bg-primary/90 transition"
          >
            Choose Files
          </label>
          <span class="ml-4 text-gray-600">or drag & drop files onto this area</span>
        </div>
        <div v-if="uploading" class="mt-2 text-sm text-primary">
          <RefreshCw class="animate-spin inline-block mr-1" size="16" /> Uploading…
        </div>
      </div>

      <!-- Gallery Grid -->
      <div v-if="loading" class="flex justify-center py-10">
        <RefreshCw class="animate-spin text-4xl text-primary" />
      </div>
      <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6">
        <div
          v-for="img in images"
          :key="img.id"
          class="relative group rounded-xl overflow-hidden shadow-lg bg-white/80 backdrop-filter backdrop-blur-sm"
        >
          <img
            :src="getImageUrl(img.id)"
            alt="Image"
            class="w-full h-48 object-cover transition-transform duration-300 group-hover:scale-105"
          />
          <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center gap-4">
            <button
              @click="confirmDelete(img.id)"
              class="p-2 bg-red-600 rounded-full text-white hover:bg-red-700 transition"
              title="Delete"
            >
              <Trash2 size="20" />
            </button>
          </div>
        </div>
      </div>

      <!-- Pagination (simple) -->
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
