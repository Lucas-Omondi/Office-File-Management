<script setup lang="ts">
import { ref, defineEmits } from "vue";
import { useRouter, useRoute } from "vue-router";

const router = useRouter();
const route = useRoute();
const isCollapsed = ref(false);
const emit = defineEmits(["toggle-sidebar"]);

// Toggle sidebar and notify parent (App.vue)
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  emit("toggle-sidebar", isCollapsed.value);
};

const navItems = [
  { name: "Dashboard", path: "/dashboard", icon: "📊" },
  { name: "Projects", path: "/projects", icon: "📁" },
  { name: "Files", path: "/files", icon: "📂" },
  { name: "Constituencies", path: "/constituencies", icon: "🏛️" },
  { name: "Users", path: "/users", icon: "👤" },
  { name: "Counties", path: "/counties", icon: "🌍" },
  { name: "Regions", path: "/regions", icon: "🗺️" },
];

const isActive = (path: string) => route.path === path;
const navigateTo = (path: string) => {
  router.push(path);
};
</script>

<template>
  <aside
      class="h-screen bg-green-700 text-white transition-all duration-300 flex flex-col fixed top-0 left-0"
      :class="{ 'w-64': !isCollapsed, 'w-20': isCollapsed }"
  >
    <!-- Sidebar Header & Toggle Button -->
    <div class="p-4 flex justify-between items-center">
      <h1 v-if="!isCollapsed" class="text-xl font-bold">Dashboard</h1>
      <button
          @click="toggleSidebar"
          class="p-2 bg-orange-500 rounded transition-transform hover:scale-110"
      >
        {{ isCollapsed ? "➡️" : "⬅️" }}
      </button>
    </div>

    <!-- Navigation Links -->
    <nav class="flex flex-col mt-4 space-y-1">
      <button
          v-for="item in navItems"
          :key="item.path"
          @click="navigateTo(item.path)"
          class="flex items-center space-x-3 p-3 transition rounded"
          :class="{
          'bg-green-800': isActive(item.path),
          'hover:bg-green-600': !isActive(item.path),
        }"
      >
        <span>{{ item.icon }}</span>
        <span v-if="!isCollapsed" class="text-white font-medium">{{ item.name }}</span>
      </button>
    </nav>
  </aside>
</template>

<style scoped>
aside {
  height: 100vh;
  overflow: hidden;
}
button {
  transition: all 0.3s ease-in-out;
}
</style>
