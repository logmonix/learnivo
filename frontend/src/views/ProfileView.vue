<script setup>
import { ref, onMounted, computed } from 'vue';
import { useProfileStore } from '../stores/profile';
import { useRouter } from 'vue-router';
import { ShoppingBag, Award, X } from 'lucide-vue-next';
import api from '../api/axios';

const profileStore = useProfileStore();
const router = useRouter();

const badges = ref([]);
const avatarItems = ref([]);
const ownedItems = ref([]);
const loading = ref(true);
const showShop = ref(false);
const purchasing = ref(false);

const profile = computed(() => profileStore.currentProfile);

const groupedItems = computed(() => {
    const groups = {};
    avatarItems.value.forEach(item => {
        if (!groups[item.category]) {
            groups[item.category] = [];
        }
        groups[item.category].push(item);
    });
    return groups;
});

onMounted(async () => {
    if (!profile.value) {
        router.push('/dashboard');
        return;
    }
    await loadProfileData();
});

async function loadProfileData() {
    loading.value = true;
    try {
        // Load real badges from API
        const badgesResponse = await api.get(`/gamification/badges/profile/${profile.value.id}`);
        badges.value = badgesResponse.data;
        
        // Load real avatar items from API
        const itemsResponse = await api.get('/gamification/shop/items');
        avatarItems.value = itemsResponse.data;
        
        // Load owned items
        const ownedResponse = await api.get(`/gamification/shop/profile/${profile.value.id}`);
        ownedItems.value = ownedResponse.data.map(item => item.item_id);
        
        // Check for newly earned badges
        await api.post(`/gamification/badges/check/${profile.value.id}`);
    } catch (error) {
        console.error('Failed to load profile data:', error);
        // Fallback to mock data on error
        badges.value = [
            { name: "First Steps", description: "Complete your first lesson", icon: "🌟", earned: true },
            { name: "Quick Learner", description: "Complete 10 lessons", icon: "⚡", earned: false },
            { name: "Math Whiz", description: "Earn 100 XP", icon: "🧮", earned: profile.value.xp >= 100 },
        ];
        
        avatarItems.value = [
            { id: 1, name: "Wizard Hat", category: "hat", icon: "🧙", cost: 50 },
            { id: 2, name: "Crown", category: "hat", icon: "👑", cost: 100 },
            { id: 3, name: "Sunglasses", category: "accessory", icon: "😎", cost: 40 },
            { id: 4, name: "Rainbow", category: "background", icon: "🌈", cost: 100 },
        ];
        
        ownedItems.value = [];
    } finally {
        loading.value = false;
    }
}

async function purchaseItem(item) {
    if (profile.value.coins < item.cost) {
        alert('Not enough coins!');
        return;
    }
    
    purchasing.value = true;
    try {
        const response = await api.post(`/gamification/shop/purchase/${profile.value.id}/${item.id}`);
        ownedItems.value.push(item.id);
        profile.value.coins = response.data.remaining_coins;
        
        // Update profile store
        await profileStore.fetchProfiles();
        profileStore.loadCurrentProfile();
        
        alert(`Purchased ${item.name}! 🎉`);
    } catch (error) {
        console.error('Purchase failed:', error);
        const errorMsg = error.response?.data?.detail || 'Purchase failed. Please try again.';
        alert(errorMsg);
    } finally {
        purchasing.value = false;
    }
}

function isOwned(itemId) {
    return ownedItems.value.includes(itemId);
}
</script>

<template>
    <div class="min-h-screen bg-gradient-to-br from-primary/5 via-secondary/5 to-accent-pink/5 p-6">
        <div class="max-w-6xl mx-auto">
            <!-- Header -->
            <div class="flex items-center justify-between mb-8">
                <div>
                    <h1 class="text-4xl font-heading text-dark mb-2">{{ profile?.display_name }}'s Profile</h1>
                    <p class="text-xl text-gray-600">Level {{ Math.floor((profile?.xp || 0) / 100) + 1 }}</p>
                </div>
                
                <div class="card px-6 py-4 flex items-center gap-4">
                    <div class="text-center">
                        <div class="text-3xl font-bold text-primary">{{ profile?.xp }}</div>
                        <div class="text-xs text-gray-500">XP</div>
                    </div>
                    <div class="text-center">
                        <div class="text-3xl font-bold text-accent-yellow">{{ profile?.coins }}</div>
                        <div class="text-xs text-gray-500">Coins</div>
                    </div>
                </div>
            </div>

            <!-- Badges Section -->
            <div class="card mb-8">
                <h2 class="text-2xl font-heading text-dark mb-4 flex items-center gap-2">
                    <Award class="text-accent-yellow" />
                    Badges & Achievements
                </h2>
                
                <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                    <div 
                        v-for="badge in badges" 
                        :key="badge.name"
                        :class="[
                            'p-4 rounded-2xl text-center transition-all',
                            badge.earned ? 'bg-gradient-to-br from-accent-yellow/20 to-accent-orange/20 border-2 border-accent-yellow' : 'bg-gray-100 opacity-50'
                        ]"
                    >
                        <div class="text-5xl mb-2">{{ badge.icon }}</div>
                        <div class="font-bold text-dark">{{ badge.name }}</div>
                        <div class="text-xs text-gray-600">{{ badge.description }}</div>
                    </div>
                </div>
            </div>

            <!-- Avatar Shop -->
            <div class="card">
                <div class="flex items-center justify-between mb-4">
                    <h2 class="text-2xl font-heading text-dark flex items-center gap-2">
                        <ShoppingBag class="text-secondary" />
                        Avatar Shop
                    </h2>
                    <div class="text-sm text-gray-600">Spend your coins to customize your avatar!</div>
                </div>

                <div v-for="(items, category) in groupedItems" :key="category" class="mb-6">
                    <h3 class="text-lg font-bold text-dark mb-3 capitalize">{{ category }}s</h3>
                    <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                        <div 
                            v-for="item in items" 
                            :key="item.id"
                            class="p-4 bg-white rounded-2xl border-2 border-gray-200 hover:border-primary transition-all text-center"
                        >
                            <div class="text-4xl mb-2">{{ item.icon }}</div>
                            <div class="font-bold text-dark mb-1">{{ item.name }}</div>
                            <div class="text-sm text-gray-600 mb-3">{{ item.cost }} 🪙</div>
                            
                            <button
                                v-if="!isOwned(item.id)"
                                @click="purchaseItem(item)"
                                :disabled="profile.coins < item.cost || purchasing"
                                :class="[
                                    'w-full px-4 py-2 rounded-xl font-bold transition-all',
                                    profile.coins >= item.cost && !purchasing
                                        ? 'bg-secondary text-white hover:bg-secondary-light'
                                        : 'bg-gray-200 text-gray-400 cursor-not-allowed'
                                ]"
                            >
                                Buy
                            </button>
                            <div v-else class="text-sm font-bold text-primary">✓ Owned</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>
