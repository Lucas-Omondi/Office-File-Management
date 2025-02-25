<template>
  <div :class="{ sidebar: true, collapsed: isCollapsed }">
    <!-- Sidebar Toggle Button -->
    <button @click="toggleSidebar" class="toggle-btn">
      <span v-if="isCollapsed">☰</span>
      <span v-else>✖</span>
    </button>

    <!-- Sidebar Menu -->
    <ul class="menu">
      <li @click="fetchData('regions')">
        <span class="icon">🌍</span>
        <span v-if="!isCollapsed">Regions</span>
      </li>
      <li @click="fetchData('counties')">
        <span class="icon">🏛️</span>
        <span v-if="!isCollapsed">Counties</span>
      </li>
      <li @click="fetchData('constituencies')">
        <span class="icon">📍</span>
        <span v-if="!isCollapsed">Constituencies</span>
      </li>
      <li @click="fetchData('projects')">
        <span class="icon">📂</span>
        <span v-if="!isCollapsed">Projects</span>
      </li>
      <li @click="fetchData('files')">
        <span class="icon">📄</span>
        <span v-if="!isCollapsed">Files</span>
      </li>
    </ul>

    <!-- Logout Button (Aligned Properly) -->
    <button @click="logout" class="logout-btn">
      <span class="icon">🚪</span>
      <span v-if="!isCollapsed">Logout</span>
    </button>
  </div>
</template>

<script setup>
import { ref, defineEmits } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const isCollapsed = ref(false);
const emit = defineEmits(["dataFetched", "toggleSidebar"]);
const router = useRouter();
const authStore = useAuthStore();

// Toggle Sidebar and store state in localStorage
const toggleSidebar = () => {
  isCollapsed.value = !isCollapsed.value;
  localStorage.setItem("sidebar_collapsed", isCollapsed.value);
  emit("toggleSidebar", isCollapsed.value);
};

// Restore sidebar state on reload
if (localStorage.getItem("sidebar_collapsed") === "true") {
  isCollapsed.value = true;
}

// Fetch data from API
const fetchData = async (type) => {
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      console.error("No token found. User may not be logged in.");
      return;
    }

    const response = await axios.get(`http://127.0.0.1:8000/api/${type}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log(`Fetched ${type}:`, response.data);
    emit("dataFetched", { type, data: response.data });
  } catch (error) {
    console.error(`Error fetching ${type}:`, error.response?.data || error.message);
  }
};

// Logout function
const logout = () => {
  authStore.logout(); // Clears token from Pinia store
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  axios.defaults.headers.common["Authorization"] = null;
  router.push("/login"); // Redirect to login
};
</script>

<style scoped>
/* Sidebar Styles */
.sidebar {
  position: fixed;
  top: 0;
  left: 0;
  width: 250px; /* Default width */
  height: 100vh;
  background: #333;
  color: white;
  padding: 10px;
  transition: width 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
}

/* Collapsed Sidebar */
.collapsed {
  width: 60px;
}

/* Sidebar Toggle Button */
.toggle-btn {
  background: none;
  border: none;
  color: white;
  font-size: 24px;
  cursor: pointer;
  padding: 10px;
  align-self: flex-end;
}

/* Sidebar Menu */
.menu {
  list-style: none;
  padding: 0;
  margin-top: 20px;
  width: 100%;
}

li {
  display: flex;
  align-items: center;
  padding: 12px;
  cursor: pointer;
  transition: background 0.3s ease;
  width: 100%;
}

li:hover {
  background: #444;
}

.icon {
  margin-right: 10px;
}

/* If sidebar is collapsed, center the icons */
.collapsed .icon {
  margin-right: 0;
}

.collapsed li {
  justify-content: center;
}

/* Logout Button */
.logout-btn {
  background: #c0392b;
  color: white;
  border: none;
  padding: 12px;
  cursor: pointer;
  width: 100%;
  text-align: left;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-top: auto; /* Push it to the bottom */
  transition: background 0.3s ease;
}

.logout-btn:hover {
  background: #e74c3c;
  width: 60px;
}

.collapsed .logout-btn {
  justify-content: center;
}
</style>
