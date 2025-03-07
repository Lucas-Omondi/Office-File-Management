<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";

// Reactive state
const projects = ref([]);
const constituencies = ref<Record<number, string>>({}); // Store constituency names by ID
const loading = ref(true);
const error = ref("");
const sortKey = ref("rfx_number");
const sortOrder = ref(1);

// Search filters
const searchFilters = ref({
  rfx_number: "",
  name: "",
  contracting_company: "",
  contract_date: "",
  constituency: "",
  status: "",
});

// Fetch projects from API with token
const fetchProjects = async () => {
  try {
    const token = localStorage.getItem("accessToken");

    if (!token) {
      error.value = "Authentication required. Please log in.";
      return;
    }

    const [projectsResponse, constituenciesResponse] = await Promise.all([
      axios.get("http://127.0.0.1:8000/api/projects/", {
        headers: { Authorization: `Bearer ${token}` },
      }),
      axios.get("http://127.0.0.1:8000/api/constituencies/", {
        headers: { Authorization: `Bearer ${token}` },
      }),
    ]);

    projects.value = Array.isArray(projectsResponse.data) ? projectsResponse.data : [];
    constituencies.value = Object.fromEntries(
        constituenciesResponse.data.map((c: { id: number; name: string }) => [c.id, c.name])
    );
  } catch (err) {
    console.error("Error fetching data:", err.response?.data || err.message);
    error.value = "Failed to load projects. Please try again later.";
  } finally {
    loading.value = false;
  }
};

// Computed filtered and sorted projects
const filteredProjects = computed(() => {
  return projects.value
      .filter((project) =>
          Object.keys(searchFilters.value).every((key) => {
            if (key === "constituency") {
              const constituencyName = constituencies.value[project.constituency] || "";
              return constituencyName.toLowerCase().includes(
                  searchFilters.value.constituency.toLowerCase()
              );
            }
            return String(project[key as keyof typeof project] || "")
                .toLowerCase()
                .includes(searchFilters.value[key as keyof typeof searchFilters.value].toLowerCase());
          })
      )
      .sort((a, b) =>
          (a[sortKey.value] > b[sortKey.value] ? 1 : -1) * sortOrder.value
      );
});

// Sort function
const sortBy = (key: string) => {
  if (sortKey.value === key) {
    sortOrder.value *= -1;
  } else {
    sortKey.value = key;
    sortOrder.value = 1;
  }
};

// Fetch data on mount
onMounted(fetchProjects);
</script>

<template>
  <div class="p-6 bg-white shadow-md rounded-lg">
    <h2 class="text-xl font-semibold text-gray-800 mb-4">Projects</h2>

    <p v-if="loading" class="text-gray-500">Loading projects...</p>
    <p v-if="error" class="text-red-500">{{ error }}</p>

    <div v-if="!loading && !error" class="overflow-x-auto">
      <table class="min-w-full border border-gray-200">
        <thead>
        <tr class="bg-green-700 text-white">
          <th class="p-3 cursor-pointer" @click="sortBy('rfx_number')">RFX Number</th>
          <th class="p-3 cursor-pointer" @click="sortBy('name')">Project Name</th>
          <th class="p-3 cursor-pointer" @click="sortBy('contracting_company')">Contractor</th>
          <th class="p-3 cursor-pointer" @click="sortBy('contract_date')">Project Date</th>
          <th class="p-3 cursor-pointer" @click="sortBy('constituency')">Constituency</th>
          <th class="p-3 cursor-pointer" @click="sortBy('status')">Status</th>
        </tr>
        <tr class="bg-green-100">
          <th class="p-2">
            <input v-model="searchFilters.rfx_number" placeholder="Search..." class="input" />
          </th>
          <th class="p-2">
            <input v-model="searchFilters.name" placeholder="Search..." class="input" />
          </th>
          <th class="p-2">
            <input v-model="searchFilters.contracting_company" placeholder="Search..." class="input" />
          </th>
          <th class="p-2">
            <input v-model="searchFilters.contract_date" type="date" class="input" />
          </th>
          <th class="p-2">
            <input v-model="searchFilters.constituency" placeholder="Search..." class="input" />
          </th>
          <th class="p-2">
            <input v-model="searchFilters.status" placeholder="Search..." class="input" />
          </th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="project in filteredProjects" :key="project.rfx_number" class="hover:bg-gray-100 transition">
          <td class="p-3 border">{{ project.rfx_number }}</td>
          <td class="p-3 border">{{ project.name }}</td>
          <td class="p-3 border">{{ project.contracting_company }}</td>
          <td class="p-3 border">{{ project.contract_date }}</td>
          <td class="p-3 border">{{ constituencies[project.constituency] || 'Unknown' }}</td>
          <td class="p-3 border">
              <span :class="{
                'text-green-600 font-bold': project.status === 'Completed',
                'text-orange-500 font-bold': project.status === 'Ongoing',
                'text-red-500 font-bold': project.status === 'Pending'
              }">
                {{ project.status }}
              </span>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<style scoped>
.input {
  width: 100%;
  padding: 6px;
  border: 1px solid #ccc;
  border-radius: 4px;
  font-size: 14px;
  outline: none;
}
.input:focus {
  border-color: #4caf50;
}
th {
  cursor: pointer;
  transition: background 0.3s;
}
th:hover {
  background: rgba(255, 255, 255, 0.2);
}
</style>
