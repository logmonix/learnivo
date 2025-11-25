<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { getChapterImages, addImageToChapter, removeImageFromChapter, updateImageOrder } from '../api/chapterImageService';
import { fetchImages, getImageUrl } from '../api/imageService';
import { RefreshCw, Plus, Trash2, ArrowUp, ArrowDown } from 'lucide-vue-next';

const router = useRouter();
const route = useRoute();
const chapterId = Number(route.params.chapterId);

const chapterImages = ref([]);
const loading = ref(false);

// For adding existing image
const allImages = ref([]);
const showAddModal = ref(false);
const selectedImageId = ref(null);

async function loadChapterImages() {
  loading.value = true;
  try {
    const resp = await getChapterImages(chapterId);
    chapterImages.value = resp.data; // assume array of {id, order_index, caption, image: {id, filename}}
  } catch (e) {
    console.error('Failed to load chapter images', e);
    alert('Could not load images');
  } finally {
    loading.value = false;
  }
}

async function loadAllImages() {
  try {
    const resp = await fetchImages(1, 1000);
    allImages.value = resp.data.results || resp.data;
  } catch (e) {
    console.error('Failed to fetch all images', e);
  }
}

onMounted(() => {
  loadChapterImages();
});

function openAddModal() {
  loadAllImages();
  showAddModal.value = true;
}

async function confirmAdd() {
  if (!selectedImageId.value) return;
  try {
    await addImageToChapter(chapterId, selectedImageId.value);
    alert('Image added');
    await loadChapterImages();
    showAddModal.value = false;
    selectedImageId.value = null;
  } catch (e) {
    console.error('Add image error', e);
    alert('Failed to add image');
  }
}

async function deleteImg(imgId) {
  if (!confirm('Delete this image from chapter?')) return;
  try {
    await removeImageFromChapter(chapterId, imgId);
    alert('Deleted');
    await loadChapterImages();
  } catch (e) {
    console.error('Delete error', e);
    alert('Failed to delete');
  }
}

async function moveUp(idx) {
  if (idx === 0) return;
  const img = chapterImages.value[idx];
  const newOrder = chapterImages.value[idx - 1].order_index;
  await updateImageOrder(chapterId, img.id, newOrder);
  await loadChapterImages();
}

async function moveDown(idx) {
  if (idx === chapterImages.value.length - 1) return;
  const img = chapterImages.value[idx];
  const newOrder = chapterImages.value[idx + 1].order_index;
  await updateImageOrder(chapterId, img.id, newOrder);
  await loadChapterImages();
}
</script>

<template>
  <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
    <div class="max-w-4xl mx-auto">
      <h1 class="text-3xl font-heading text-dark mb-4">Chapter Images</h1>
      <button @click="router.push('/admin/content')" class="btn-secondary mb-4">← Back to Content Browser</button>

      <div class="flex items-center gap-4 mb-4">
        <button @click="openAddModal" class="btn-primary flex items-center gap-2">
          <Plus size="20" /> Add Existing Image
        </button>
        <RefreshCw v-if="loading" class="animate-spin text-primary" />
      </div>

      <div v-if="chapterImages.length === 0 && !loading" class="text-center py-10 text-gray-600">
        No images linked to this chapter.
      </div>

      <ul v-else class="space-y-3">
        <li v-for="(ci, idx) in chapterImages" :key="ci.id" class="flex items-center bg-white/80 rounded-xl p-3 shadow-sm">
          <img :src="getImageUrl(ci.image.id)" alt="" class="w-16 h-16 object-cover rounded mr-4" />
          <div class="flex-1">
            <div class="font-medium">{{ ci.caption || 'No caption' }}</div>
            <div class="text-sm text-gray-500">Order: {{ ci.order_index }}</div>
          </div>
          <div class="flex gap-2 items-center">
            <button @click="moveUp(idx)" :disabled="idx===0" class="p-1 rounded hover:bg-gray-200">
              <ArrowUp size="18" />
            </button>
            <button @click="moveDown(idx)" :disabled="idx===chapterImages.length-1" class="p-1 rounded hover:bg-gray-200">
              <ArrowDown size="18" />
            </button>
            <button @click="deleteImg(ci.id)" class="p-1 rounded bg-red-600 text-white hover:bg-red-700">
              <Trash2 size="18" />
            </button>
          </div>
        </li>
      </ul>

      <!-- Add Image Modal -->
      <div v-if="showAddModal" class="fixed inset-0 bg-black/40 flex items-center justify-center z-50">
        <div class="bg-white p-6 rounded-xl w-full max-w-lg">
          <h2 class="text-xl font-heading mb-4 flex items-center gap-2">
            <Plus class="text-primary" size="20" /> Select Image to Add
          </h2>
          <select v-model="selectedImageId" class="input-field w-full mb-4">
            <option disabled value="">-- Choose an image --</option>
            <option v-for="img in allImages" :key="img.id" :value="img.id">
              {{ img.filename || img.id }}
            </option>
          </select>
          <div class="flex justify-end gap-2">
            <button @click="showAddModal = false" class="btn-secondary">Cancel</button>
            <button @click="confirmAdd" :disabled="!selectedImageId" class="btn-primary">Add</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.input-field {
  border: 1px solid #ddd;
  padding: 0.5rem;
  border-radius: 0.5rem;
}
.btn-primary { @apply bg-primary text-white py-2 px-4 rounded hover:bg-primary/90; }
.btn-secondary { @apply bg-gray-200 text-gray-800 py-2 px-4 rounded hover:bg-gray-300; }
</style>
