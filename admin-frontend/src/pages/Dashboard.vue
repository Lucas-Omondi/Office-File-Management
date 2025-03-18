<script setup lang="ts">
import { ref, onMounted, nextTick } from "vue";
import Sidebar from "../components/Sidebar.vue";
import Navbar from "../layouts/Navbar.vue";
import api from "../utils/api.ts"; // ✅ Ensure you have API utils configured

const isSidebarCollapsed = ref(false);
const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed;
};

// Ensure layout updates correctly on first load
onMounted(() => {
  nextTick(() => {
    isSidebarCollapsed.value = true; // Set to true again after mounting
  });
});

// 🔹 Dashboard Stats
const stats = ref([
  { label: "Projects", count: 0, icon: "📁", color: "from-green-400 to-green-600", key: "projects" },
  { label: "Users", count: 0, icon: "👤", color: "from-blue-400 to-blue-600", key: "users" },
  { label: "Constituencies", count: 0, icon: "📍", color: "from-orange-400 to-orange-600", key: "constituencies" },
  { label: "Files", count: 0, icon: "📂", color: "from-purple-400 to-purple-600", key: "files" },
]);

const loading = ref(true);
const error = ref<string | null>(null);

// 🔹 Fetch Stats from Backend
const fetchStats = async () => {
  try {
    loading.value = true;
    const response = await api.get("summary/stats/");
    const data = response.data;

    // ✅ Update stats dynamically
    stats.value.forEach(stat => {
      stat.count = data[stat.key] || 0;
    });

  } catch (err) {
    console.error("❌ Error fetching stats:", err);
    error.value = "Failed to load dashboard stats.";
  } finally {
    loading.value = false;
  }
};


// 🔹 Fetch data when component is mounted
onMounted(fetchStats);
</script>

<template>
  <div class="flex h-screen bg-gray-100 dark:bg-gray-900 transition-all">
    <!-- Sidebar -->
    <Sidebar class="fixed left-0 top-0 h-full" @toggle-sidebar="handleSidebarToggle" />

    <!-- Main Content -->
    <div class="flex-1 flex flex-col transition-all duration-300"
         :class="{ 'ml-20': isSidebarCollapsed, 'ml-64': !isSidebarCollapsed }">

      <!-- Navbar -->
      <Navbar :isSidebarCollapsed="isSidebarCollapsed" />

      <!-- Page Content -->
      <main class="mt-16 p-6">
        <h2 class="text-3xl font-semibold text-gray-800 dark:text-white">🚀 Dashboard</h2>
        <p class="text-gray-600 dark:text-gray-300 mb-6">Welcome! Here’s an overview of the system.</p>

        <!-- Loading & Error Handling -->
        <div v-if="loading" class="text-gray-500 dark:text-gray-400">📡 Loading statistics...</div>
        <div v-else-if="error" class="text-red-500 dark:text-red-400">{{ error }}</div>

        <!-- Stats Cards -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          <div v-for="stat in stats" :key="stat.label"
               class="p-6 rounded-lg shadow-xl bg-gradient-to-br text-white transition-all transform hover:scale-105"
               :class="stat.color">
            <div class="flex items-center justify-between">
              <span class="text-4xl">{{ stat.icon }}</span>
              <h3 class="text-4xl font-bold">{{ stat.count }}</h3>
            </div>
            <p class="text-lg mt-2 font-medium">{{ stat.label }}</p>
          </div>
        </div>
      </main>
    </div>
  </div>
</template>
