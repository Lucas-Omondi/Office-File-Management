<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../store/auth";
import api from "../utils/api.ts";
import { Folder } from "lucide-vue-next";
import Sidebar from "../components/Sidebar.vue";
import Navbar from "../layouts/Navbar.vue";


const authStore = useAuthStore();
const isAuthenticated = computed(() => authStore.isAuthenticated);
console.log("Auth State:", authStore.isAuthenticated);
const isSidebarCollapsed = ref(true);
const projects = ref<any[]>([]);
const searchQuery = ref("");
const router = useRouter();

// Fetch projects from backend
onMounted(async () => {
  try {
    const { data } = await api.get("/projects/");
    projects.value = data;
  } catch (error) {
    console.error("Error fetching projects:", error);
  }
});

// Filtered projects based on search query
const filteredProjects = computed(() =>
    projects.value.filter((project) => {
      const rfx = String(project.rfx_number || "").toLowerCase();
      return rfx.includes(searchQuery.value.toLowerCase());
    })
);


function handleSidebarToggle  ()  {
  isSidebarCollapsed.value = !isSidebarCollapsed.value;
};
</script>

<template>
  <div class="flex h-screen overflow-hidden">
    <!-- Sidebar -->
    <Sidebar
        v-if="isAuthenticated"
        :isCollapsed="isSidebarCollapsed"
        class="fixed left-0 top-0 h-full"
        @toggle-sidebar="handleSidebarToggle"
    />

    <div
        class="flex flex-col flex-1 transition-all duration-300"
        :class="{ 'pl-20': isSidebarCollapsed, 'pl-64': !isSidebarCollapsed }"
    >
      <!-- Navbar -->
      <Navbar
          v-if="isAuthenticated"
          :isSidebarCollapsed="isSidebarCollapsed"
          class="fixed top-0 left-0 w-full z-10"
      />

      <!-- Main Content Area -->
      <main class="flex-1 p-6 transition-all duration-300 pt-20">
        <h1 class="text-2xl font-semibold text-gray-800 mb-6">Project Files</h1>

        <!-- Premium Styled Search Bar -->
        <div class="mb-6 flex justify-center">
          <input
              v-model="searchQuery"
              type="text"
              placeholder="Search projects..."
              class="w-full max-w-md px-4 py-2 bg-white/80 backdrop-blur-md border border-gray-300
               text-gray-800 rounded-lg shadow-md focus:ring-2 focus:ring-blue-500
               outline-none transition-all duration-200 placeholder-gray-500"
          />
        </div>

        <!-- Grid Layout for Folders -->
        <div class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-6">
          <v-motion
              v-for="project in filteredProjects"
              :key="project.id"
              :initial="{ opacity: 0, y: 10 }"
              :enter="{ opacity: 1, y: 0, transition: { duration: 0.3 } }"
              :hover="{ scale: 1.05 }"
              class="folder-card"
              @dblclick.stop="router.push(`/files/${project.rfx_number}`)"
          >
            <div class="folder-icon">
              <Folder class="w-14 h-14 text-orange-500" />
            </div>
            <span class="folder-name">RFX {{ project.rfx_number }}</span>
          </v-motion>
        </div>
      </main>
    </div>
  </div>
</template>

<style scoped>
.folder-card {
  @apply flex flex-col items-center justify-center bg-white/90 shadow-lg rounded-xl p-6
  backdrop-blur-md transition-all duration-200 cursor-pointer border border-gray-200;
}
.folder-card:hover {
  @apply scale-105 shadow-xl border-orange-500;
}
.folder-icon {
  @apply flex items-center justify-center w-16 h-16 bg-green-100 rounded-full;
}
.folder-name {
  @apply text-gray-900 font-medium text-sm mt-2;
}
</style>
