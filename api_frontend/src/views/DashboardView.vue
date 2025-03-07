<template>
  <div class="dashboard" :class="{ collapsed: isSidebarCollapsed }">
    <div class="floating-card">
      <button v-for="item in menuItems" :key="item.type" @click="fetchData(item.type)">
        <span class="icon">{{ item.icon }}</span>
        <span>{{ item.label }}</span>
      </button>
      <button @click="logout" class="logout-btn">🚪 Logout</button>
    </div>

    <div class="content">
      <h1>{{ title }}</h1>

      <!-- Loading & Error Messages -->
      <p v-if="loading">Loading data...</p>
      <p v-if="error" class="error">{{ error }}</p>

      <!-- Data Table -->
      <table v-if="formattedData.length">
        <thead>
        <tr>
          <th v-for="(value, key) in formattedData[0]" :key="key">{{ key }}</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in formattedData" :key="item.id">
          <td v-for="(value, key) in item" :key="key">
            {{ typeof value === "object" && value !== null ? value.name || "N/A" : value || "N/A" }}
          </td>
        </tr>
        </tbody>
      </table>
      <p v-else-if="!loading">No data available</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "@/stores/auth";
import axios from "axios";

const router = useRouter();
const authStore = useAuthStore();
const title = ref("Welcome to the Dashboard");
const dataList = ref([]);
const isSidebarCollapsed = ref(false);
const loading = ref(false);
const error = ref(null);

const menuItems = [
  { type: "regions", label: "Regions", icon: "🌍" },
  { type: "counties", label: "Counties", icon: "🏛️" },
  { type: "constituencies", label: "Constituencies", icon: "📍" },
  { type: "projects", label: "Projects", icon: "📂" },
  { type: "files", label: "Files", icon: "📄" }
];

// Redirect if not authenticated
onMounted(() => {
  if (!authStore.isAuthenticated) {
    router.push("/login");
  }
});

const fetchData = async (type) => {
  loading.value = true;
  error.value = null;
  try {
    const token = localStorage.getItem("access_token");
    if (!token) {
      throw new Error("Authentication required. Please log in.");
    }

    const res = await axios.get(`http://127.0.0.1:8000/api/${type}/`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log(`Raw API response for ${type}:`, res.data); // ✅ Log API response
    title.value = `List of ${type.charAt(0).toUpperCase() + type.slice(1)}`;
    dataList.value = res.data || [];
  } catch (err) {
    console.error(`Error fetching ${type}:`, err);
    error.value = err.response?.data?.detail || "Failed to load data.";
  } finally {
    loading.value = false;
  }
};

const formattedData = computed(() => {
  return dataList.value.map(item => {
    let formattedItem = {
      name: item.name || "N/A",
    };

    // Add region field only if applicable
    if (item.region) {
      formattedItem.region = item.region.name || "N/A";
    }

    // Add county field only if applicable
    if (item.county) {
      formattedItem.county = item.county.name || "N/A";
    }

    // Add constituency field only if applicable
    if (item.constituency) {
      formattedItem.constituency = item.constituency.name || "N/A";
    }

    // Add project-specific fields
    if (item.rfx_number) {
      formattedItem.rfx_number = item.rfx_number || "N/A";
      formattedItem.contracting_company = item.contracting_company || "N/A";
      formattedItem.contract_date = item.contract_date || "N/A";
      formattedItem.status = item.status || "N/A";
    }

    // Add file-specific fields
    if (item.file) {
      formattedItem.file = item.file.split('/').pop() || "N/A";
      formattedItem.rfx_number = item.project?.rfx_number || "N/A"; // Get rfx_number from the related project
    }

    return formattedItem;
  });
});



const logout = () => {
  authStore.logout();
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
  router.push("/login");
};
</script>

<style scoped>
.dashboard {
  display: flex;
  height: 100vh;
  padding: 20px;
}

.floating-card {
  position: fixed;
  top: 20px;
  left: 20px;
  background: #333;
  color: white;
  padding: 15px;
  border-radius: 10px;
  box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
}

.floating-card button {
  display: flex;
  align-items: center;
  background: none;
  border: none;
  color: white;
  font-size: 16px;
  cursor: pointer;
  padding: 8px;
  margin: 5px 0;
  width: 100%;
}

.floating-card .logout-btn {
  background: #c0392b;
  width: 100%;
  text-align: left;
  border-radius: 5px;
}

.floating-card button:hover {
  background: #444;
}

.content {
  flex-grow: 1;
  margin-left: 150px;
  padding: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table, th, td {
  border: 1px solid #ddd;
}

th, td {
  padding: 8px;
  text-align: left;
}

th {
  background: #f4f4f4;
}

.error {
  color: red;
  font-weight: bold;
}
</style>
