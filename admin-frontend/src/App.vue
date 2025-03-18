<script setup lang="ts">
import { ref, computed } from "vue";
import { useAuthStore } from "./store/auth.ts";
import { useRoute, RouterView } from "vue-router";
import Sidebar from "./components/Sidebar.vue";
import Navbar from "./layouts/Navbar.vue";

const authStore = useAuthStore();
const route = useRoute();

const isSidebarCollapsed = ref(false);

// Compute authentication status
const isAuthenticated = computed(() => !!authStore.token);

// Compute if the current page is login
const isLoginPage = computed(() => route.path === "/");

// Sidebar toggle event handler
const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed;
};
</script>

<template>
  <!-- If on login page, render only RouterView without layout -->
  <RouterView v-if="isLoginPage" />

  <!-- Otherwise, render the full layout with Sidebar and Navbar -->
  <div v-else class="flex">
    <!-- Sidebar (Only when authenticated) -->
    <Sidebar v-if="isAuthenticated" @toggle-sidebar="handleSidebarToggle" />

    <!-- Main Content -->
    <div
        class="transition-all duration-300 min-h-screen"
        :class="{
        'ml-64 w-[calc(100%-16rem)]': isAuthenticated && !isSidebarCollapsed,
        'ml-20 w-[calc(100%-5rem)]': isAuthenticated && isSidebarCollapsed,
        'w-full': !isAuthenticated, // Full width if not authenticated
      }"
    >
      <!-- Navbar (Only when authenticated) -->
      <Navbar v-if="isAuthenticated" />


      <main class="p-4">
        <RouterView :sidebarExpanded="!isSidebarCollapsed" />
      </main>
    </div>
  </div>
</template>

<style scoped>
/* Smooth transition for main content */
main {
  transition: margin-left 0.3s ease-in-out, width 0.3s ease-in-out;
}
</style>
