import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../pages/Login.vue';
import DashboardPage from '../pages/Dashboard.vue';
import ProjectsPage from '../pages/Projects.vue'; // Import Projects Page
import { useAuthStore } from '../store/auth';

const routes = [
    { path: '/', component: LoginPage },
    { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true } },
    { path: '/projects', component: ProjectsPage, meta: { requiresAuth: true } }, // Add projects route
];

const router = createRouter({
    history: createWebHistory(),
    routes,
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    if (to.meta.requiresAuth && !authStore.accessToken) {
        next('/');
    } else {
        next();
    }
});

export default router;
