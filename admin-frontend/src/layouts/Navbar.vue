<script setup lang="ts">
import { ref, defineProps, computed, onMounted, reactive} from "vue";
import { useAuthStore } from "../store/auth.ts";
import { useRouter } from "vue-router";
import { onClickOutside } from "@vueuse/core";


const authStore = useAuthStore();
const router = useRouter();
const dropdownOpen = ref(false);
const userData = reactive<Record<string, any>>({});

// Props
defineProps<{ isSidebarCollapsed: boolean }>();

// Get user data from localStorage
function getUserDataFromLocalStorage(): Record<string, any> {
  const user = localStorage.getItem("user");
  return JSON.parse(user || "{}");
}

// Assign user data when component is mounted
onMounted(() => {
  Object.assign(userData, getUserDataFromLocalStorage());
});

// Logout function
const logout = () => {
  authStore.logout();
  router.push("/");
};

// Compute user initials for avatar
const userInitials = computed(() => {
  return userData.username
      ? userData.username
          .split(" ")
          .map((n: string) => n[0])
          .join("")
          .toUpperCase()
      : "U";
});

// Close dropdown when clicking outside
const dropdownRef = ref(null);
onClickOutside(dropdownRef, () => {
  dropdownOpen.value = false;
});
</script>

<template>
  <nav
      class="fixed top-0 left-0 right-0 h-16 bg-white/30 border-b border-white/20 backdrop-blur-md shadow-lg z-50 flex items-center px-6"
  >
    <h1 class="text-xl font-bold text-gray-900">Dashboard</h1>

    <div class="ml-auto relative" ref="dropdownRef">
      <button
          @click="dropdownOpen = !dropdownOpen"
          class="flex items-center space-x-3 bg-white/40 px-4 py-2 rounded-lg hover:bg-white/50 transition shadow-sm"
      >
        <span class="hidden sm:inline text-gray-900 font-medium">{{ userData.username }}</span>
        <div
            class="w-9 h-9 rounded-full flex items-center justify-center text-lg font-semibold text-white bg-gradient-to-r from-green-600 to-green-800 shadow-md"
        >
          {{ userInitials }}
        </div>
      </button>

      <transition name="fade">
        <div
            v-if="dropdownOpen"
            class="absolute right-0 mt-2 w-52 bg-white text-gray-900 rounded-lg shadow-lg border border-gray-200"
        >
          <button
              @click="logout"
              class="block w-full text-left px-4 py-3 text-red-600 font-medium hover:bg-gray-100 transition"
          >
            Logout
          </button>
        </div>
      </transition>
    </div>
  </nav>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}
</style>
