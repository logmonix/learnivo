<!-- src/components/AdminImageGallery.vue -->
<template>
  <section class="admin-image-gallery">
    <header class="flex items-center justify-between mb-6">
      <h2 class="text-2xl font-bold text-primary">Image Gallery</h2>
      <label class="cursor-pointer inline-flex items-center gap-2 bg-primary/10 hover:bg-primary/20 text-primary rounded-md px-4 py-2 transition-colors">
        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1M12 12v9m0 0l-3-3m3 3l3-3M12 3v9" />
        </svg>
        Upload Images
        <input type="file" multiple @change="handleFileSelect" class="hidden" />
      </label>
    </header>

    <div v-if="loading" class="flex justify-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
    </div>

    <div v-else-if="images.length === 0" class="text-center text-gray-500 py-12">
      No images found. Upload some to get started!
    </div>

    <div v-else class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      <article v-for="img in images" :key="img.id" class="relative group rounded-lg overflow-hidden shadow-lg hover:shadow-xl transition-shadow">
        <img :src="getFileUrl(img.id)" :alt="img.filename" class="w-full h-48 object-cover group-hover:scale-105 transition-transform" />
        <div class="absolute inset-0 bg-black/30 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
          <button @click="deleteImg(img.id)" class="bg-red-600 hover:bg-red-700 text-white rounded-full p-2">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <footer class="p-2 bg-white/80 backdrop-blur-sm text-sm truncate">
          {{ img.filename }}
        </footer>
      </article>
    </div>

    <!-- Pagination Controls -->
    <nav v-if="totalPages > 1" class="flex justify-center mt-6 space-x-2">
      <button @click="changePage(page - 1)" :disabled="page === 1" class="px-3 py-1 rounded bg-primary/10 hover:bg-primary/20 disabled:opacity-50">
        Prev
      </button>
      <span class="px-3 py-1">Page {{ page }} of {{ totalPages }}</span>
      <button @click="changePage(page + 1)" :disabled="page === totalPages" class="px-3 py-1 rounded bg-primary/10 hover:bg-primary/20 disabled:opacity-50">
        Next
      </button>
    </nav>
  </section>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue';
import { listImages, uploadImages, deleteImage, getImageFileUrl } from '../services/imageService';

const images = ref([]);
const loading = ref(false);
const page = ref(1);
const pageSize = 20;
const totalPages = ref(1);
const searchTerm = ref('');

async function fetchImages() {
  loading.value = true;
  try {
    const resp = await listImages({ page: page.value, pageSize, search: searchTerm.value });
    images.value = resp.data.items || [];
    totalPages.value = Math.ceil((resp.data.total || 0) / pageSize);
  } catch (e) {
    console.error('Failed to load images', e);
  } finally {
    loading.value = false;
  }
}

function getFileUrl(id) {
  return getImageFileUrl(id);
}

function changePage(newPage) {
  if (newPage < 1 || newPage > totalPages.value) return;
  page.value = newPage;
}

watch([page, searchTerm], fetchImages);

onMounted(fetchImages);

async function handleFileSelect(event) {
  const files = event.target.files;
  if (!files?.length) return;
  try {
    await uploadImages(files, (progressEvent) => {
      // Optional: you could hook this into a progress bar UI.
    });
    // Refresh list after successful upload.
    await fetchImages();
  } catch (e) {
    console.error('Upload failed', e);
  }
}

async function deleteImg(id) {
  if (!confirm('Delete this image? This action cannot be undone.')) return;
  try {
    await deleteImage(id);
    await fetchImages();
  } catch (e) {
    console.error('Delete failed', e);
  }
}
</script>

<style scoped>
.admin-image-gallery {
  max-width: 1200px;
  margin: 0 auto;
  padding: 1rem;
}

/* Glassmorphism card effect for the footer */
footer {
  background: rgba(255, 255, 255, 0.4);
  backdrop-filter: blur(8px);
}
</style>
