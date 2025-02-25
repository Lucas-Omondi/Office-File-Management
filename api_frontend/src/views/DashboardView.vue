<template>
  <div class="dashboard" :class="{ collapsed: isSidebarCollapsed }">
    <Sidebar @dataFetched="updateData" @toggleSidebar="toggleSidebar" />
    <div class="content">
      <h1>{{ title }}</h1>
      <ul v-if="dataList.length">
        <li v-for="item in dataList" :key="item.id">{{ item.name }}</li>
      </ul>
      <p v-else>No data available</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import Sidebar from "../views/Sidebar.vue";

const router = useRouter();
const authStore = useAuthStore();

const title = ref("Welcome to the Dashboard");
const dataList = ref([]);
const isSidebarCollapsed = ref(false);

// Redirect to login if not authenticated
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
  }
});

const updateData = ({ type, data }) => {
  title.value = `List of ${type.charAt(0).toUpperCase() + type.slice(1)}`;
  dataList.value = data;
};

const toggleSidebar = (collapsed) => {
  isSidebarCollapsed.value = collapsed;
};
</script>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  margin-left: 250px;
  transition: margin-left 0.3s ease;
  padding: 20px;
}

.dashboard.collapsed {
  margin-left: 60px;
}

.content {
  flex-grow: 1;
  padding: 20px;
}

ul {
  list-style: none;
  padding: 0;
}

li {
  padding: 8px;
  background: #f4f4f4;
  margin-bottom: 5px;
  border-radius: 5px;
}
</style>
