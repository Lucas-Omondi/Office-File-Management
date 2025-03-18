import { createRouter, createWebHistory } from 'vue-router';
import LoginPage from '../pages/Login.vue';
import DashboardPage from '../pages/Dashboard.vue';
import ProjectsPage from '../pages/Projects.vue'; // Import Projects Page
import { useAuthStore } from '../store/auth';
import Demo from "../pages/Demo.vue";
import UsersPage from '../pages/usersView.vue';

const routes = [
    {
        path: "/files/:rfx_number",
        name: "ProjectFiles",
        component: () => import("../components/files/FilesPage.vue"),
    },
    { path: '/', component: LoginPage },
    {path: '/demo', component: Demo },
    { path: '/dashboard', component: DashboardPage, meta: { requiresAuth: true } },
    { path: '/projects', component: ProjectsPage, meta: { requiresAuth: true } }, // Add projects route
    {path: '/users', component: UsersPage, meta: { requiresAuth: true } },
    { path: '/files', component: () => import('../pages/FilesView.vue'), meta: { requiresAuth: true } },
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
