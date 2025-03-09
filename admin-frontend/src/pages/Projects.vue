<script setup lang="ts">
import { ref, computed, onMounted } from "vue";
import axios from "axios";
import Sidebar from "../components/Sidebar.vue";
import Navbar from "../layouts/Navbar.vue";
import Modal from "../components/Modal.vue";
import AddProject from "../components/AddProject.vue";
import AddCounty from "../components/AddCounty.vue";
import AddConstituency from "../components/AddConstituency.vue";
import AddRegion from "../components/AddRegion.vue";
import EditProject from "../components/EditProject.vue";
import ConfirmDelete from "../components/ConfirmDelete.vue";
import {useProjectStore} from "../store/useProjectStore.ts";

// Props
defineProps({
  sidebarExpanded: Boolean,
});

// Sidebar state
const isSidebarCollapsed = ref(false);
const handleSidebarToggle = (collapsed: boolean) => {
  isSidebarCollapsed.value = collapsed;
};

// Reactive state
const projects = ref<any[]>([]);  // Ensure it's defined as an empty array
const constituencies = ref<Record<number, string>>({});
const selectedProjects = ref<string[]>([]);
const loading = ref(true);
const error = ref("");
const sortKey = ref("rfx_number");
const sortOrder = ref(1);
const selectAllOption = ref("");
const searchQuery = ref("");

// Modal State
const activeModal = ref<"project" | "constituency" | "county" | "region" | null>(null);

// Modal Handlers
const openModal = (modal: "project" | "constituency" | "county" | "region") => {
  activeModal.value = modal;
};
const closeModal = () => {
  activeModal.value = null;
};
const handleProjectAdded = async () => {
  await fetchProjects(); // ✅ Refresh projects after adding a new one
  closeModal();
};

// Editing Projects
const activeEditProject = ref(null);
const openEditModal = (project) => {
  activeEditProject.value = {...project };
};
const closeEditModal = () => {
  activeEditProject.value = null;
};
const handleProjectUpdated = (updatedProject) => {
  const index = projects.value.findIndex((p) => p.id === updatedProject.id);
  if (index !== -1) {
    projects.value[index] = updatedProject; // ✅ Update project in place
  }
  closeEditModal();
};

// Fetch projects from API
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
      .filter((project) => {
        return Object.values(project).some((value) =>
            String(value).toLowerCase().includes(searchQuery.value.toLowerCase())
        );
      })
      .sort((a, b) => (a[sortKey.value] > b[sortKey.value] ? 1 : -1) * sortOrder.value);
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

// Select/Deselect all projects
const toggleSelectAll = (option: string) => {
  if (option === "All") {
    selectedProjects.value = projects.value.map((project) => project.id);
  } else {
    selectedProjects.value = [];
  }
};
const projectStore = useProjectStore();
const isDeleteModalOpen = ref(false);

// Compute whether to show the delete button
const isDeleteEnabled = computed(() => projectStore.selectedProjects.length > 0);

const openDeleteModal = () => {
  console.log("Delete button clicked!");
  isDeleteModalOpen.value = true;
};

const deleteProjects = async () => {
  try {
    const token = localStorage.getItem("accessToken");
    await axios.delete("http://127.0.0.1:8000/api/projects/bulk_delete/", {
      headers: { Authorization: `Bearer ${token}` },
      data: { ids: selectedProjects.value },  // 🔹 Send selected project IDs
    });

    // Remove deleted projects from local state
    projects.value = projects.value.filter((p) => !selectedProjects.value.includes(p.id));
    selectedProjects.value = [];
    isDeleteModalOpen.value = false;
  } catch (error) {
    console.error("Failed to delete projects:", error);
  }
};



// Determine if multiple selections are made
const isMultipleSelected = computed(() => selectedProjects.value.length > 1);

// Fetch data on mount
onMounted(fetchProjects);
</script>

<template>
  <div class="flex h-screen bg-gray-100">
    <Sidebar class="fixed left-0 top-0 h-full" @toggle-sidebar="handleSidebarToggle" />
    <div class="flex-1 flex flex-col transition-all duration-300" :class="{ 'ml-64': !isSidebarCollapsed, 'ml-20': isSidebarCollapsed }">
      <Navbar :isSidebarCollapsed="isSidebarCollapsed" />
      <main class="mt-16 p-6">
        <h2 class="text-xl font-semibold text-gray-800 mb-4">Projects</h2>
        <p v-if="loading" class="text-gray-500">Loading projects...</p>
        <p v-if="error" class="text-red-500">{{ error }}</p>
        <div v-if="!loading && !error" class="overflow-x-auto bg-white p-4 rounded-lg shadow-md">
          <div class="flex items-center justify-between bg-gray-100 p-2">
            <select v-model="selectAllOption" @change="toggleSelectAll(selectAllOption)" class="border p-2 rounded">
              <option value="" disabled selected>Select</option>
              <option value="All">All</option>
              <option value="None">None</option>
            </select>
            <input v-model="searchQuery" placeholder="Search..." class="border p-2 rounded w-1/3" />
            <div v-if="selectedProjects.length" class="flex gap-2">
              <button v-if="!isMultipleSelected" @click="openEditModal(filteredProjects.find(p => p.id === selectedProjects[0]))" class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded">Edit</button>
              <button v-if="isDeleteEnabled || isMultipleSelected || !isMultipleSelected" @click="openDeleteModal" class="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded">Delete</button>
            </div>
          </div>
          <table class="w-full border border-gray-200 table-fixed">
            <thead>
            <tr class="bg-green-700 text-white">
              <th class="p-3 w-16">Select</th>
              <th class="p-3 w-1/6 cursor-pointer" @click="sortBy('rfx_number')">RFX Number</th>
              <th class="p-3 w-1/6 cursor-pointer" @click="sortBy('name')">Project Name</th>
              <th class="p-3 w-1/6 cursor-pointer" @click="sortBy('contracting_company')">Contractor</th>
              <th class="p-3 w-1/6 cursor-pointer" @click="sortBy('contract_date')">Project Date</th>
              <th class="p-3 w-1/6 cursor-pointer" @click="sortBy('constituency')">Constituency</th>
              <th class="p-3 w-1/6 cursor-pointer" @click="sortBy('status')">Status</th>
            </tr>
            </thead>
            <tbody>
            <tr v-for="project in filteredProjects" :key="project.id" class="hover:bg-gray-100 transition">
              <td class="p-3 border text-center w-16">
                <input type="checkbox" :value="project.id" v-model="selectedProjects" />
              </td>
              <td v-for="field in [project.rfx_number, project.name, project.contracting_company, project.contract_date, constituencies[project.constituency] || 'Unknown', project.status]" class="p-3 border w-1/6 truncate relative" :title="field">
                <span class="block truncate" @mouseover="$event.target.title = field">{{ field }}</span>
              </td>
            </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
    <button @click="openModal('project')" class="fixed bottom-6 right-6 bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-full shadow-lg transition-all duration-300 flex items-center gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 5v14M5 12h14"/>
      </svg>
      <span class="hidden sm:inline">New Project</span>
    </button>


    <!-- Confirmation Modal -->


    <Modal :show="activeModal !== null" @close="closeModal">
      <AddProject v-if="activeModal === 'project'" @close="closeModal" @projectAdded="handleProjectAdded" />
      <AddConstituency v-if="activeModal === 'constituency'" @close="closeModal" @openAddCounty="openModal('county')" />
      <AddCounty v-if="activeModal === 'county'" @close="closeModal" @openAddRegion="openModal('region')" />
      <AddRegion v-if="activeModal === 'region'" @close="closeModal" />

    </Modal>

    <EditProject
      v-if="activeEditProject"
      :show="!!activeEditProject"
      :project= "activeEditProject"
      @close="closeEditModal"
      @projectUpdated="handleProjectUpdated"
    />
    <ConfirmDelete
        v-if="isDeleteModalOpen"
        @confirm="deleteProjects"
        @cancel="isDeleteModalOpen = false"
    />


  </div>
</template>
