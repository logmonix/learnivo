import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'
import { useAuthStore } from './stores/auth'
import Login from './views/Login.vue'
import Dashboard from './views/Dashboard.vue'
import StudentHome from './views/StudentHome.vue'
import SubjectView from './views/SubjectView.vue'
import LessonView from './views/LessonView.vue'
import AdminDashboard from './views/AdminDashboard.vue'
import ProfileView from './views/ProfileView.vue'

const routes = [
    { path: '/', redirect: '/login' },
    { path: '/login', component: Login },
    { path: '/dashboard', component: Dashboard },
    { path: '/student', component: StudentHome },
    { path: '/learn/:id', component: SubjectView },
    { path: '/lesson/:chapterId', component: LessonView },
    { path: '/admin', component: AdminDashboard },
    { path: '/profile', component: ProfileView },
]

const router = createRouter({
    history: createWebHistory(),
    routes,
});

// Route guard for admin pages
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

    if (to.path === '/admin' && !authStore.isAdmin) {
        alert('Admin access required');
        next('/dashboard');
    } else {
        next();
    }
});

const pinia = createPinia() // pinia creation remains before app creation
const app = createApp(App);

app.use(router); // Reordered to be before pinia as per snippet
app.use(pinia);
app.mount('#app');
