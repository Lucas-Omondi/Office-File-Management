<script setup lang="ts">
import { ref, defineEmits, onMounted } from "vue";
import axios from "axios";
import AddConstituency from "../AddConstituency.vue";
import AddCounty from "../AddCounty.vue";
import AddRegion from "../AddRegion.vue";


const emit = defineEmits(["close", "projectAdded", "openAddConstituency"]);
const isAddingConstituency = ref(false);
const isAddingCounty = ref(false);
const isAddingRegion = ref(false);

const rfxNumber = ref("");
const name = ref("");
const constituency = ref("");
const status = ref("Not Started");
const contractingCompany = ref("");
const contractDate = ref("");
const constituencies = ref<{ id: number; name: string }[]>([]);
const isSubmitting = ref(false);
const errorMessage = ref("");


const fetchConstituencies = async () => {
  try {
    const token = localStorage.getItem("accessToken");
    if (!token) throw new Error("Authentication required.");
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/constituencies/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    constituencies.value = response.data;
  } catch (err) {
    errorMessage.value = "Failed to load constituencies.";
  }
};

const submitProject = async () => {
  isSubmitting.value = true;
  errorMessage.value = "";

  try {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      console.error("No access token found.");
      errorMessage.value = "Authentication required.";
      return;
    }

    const projectData = {
      rfx_number: rfxNumber.value,
      name: name.value,
      constituency: constituency.value,
      status: status.value,
      contracting_company: contractingCompany.value,
      contract_date: contractDate.value,
    };

    console.log("Sending project data:", projectData);

    const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/projects/`, projectData, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log("Project added successfully:", response.data);

    emit("projectAdded", response.data); // Send the new project to parent (Projects.vue)
    emit("close"); // Close modal after success

  } catch (err) {
    console.error("Error adding project:", err.response?.data || err.message);
    errorMessage.value = err.response?.data?.message || "Failed to add project.";
  } finally {
    isSubmitting.value = false;
  }
};

onMounted(fetchConstituencies);
</script>

<template>
  <!-- Project Form -->
  <div v-if="!isAddingConstituency && !isAddingCounty">
    <form @submit.prevent="submitProject" class="space-y-4">
      <p v-if="errorMessage" class="text-red-500">{{ errorMessage }}</p>

      <label class="block">
        <span class="text-gray-700">RFX Number</span>
        <input v-model="rfxNumber" type="number" required class="w-full p-2 border rounded" />
      </label>

      <label class="block">
        <span class="text-gray-700">Project Name</span>
        <input v-model="name" type="text" required class="w-full p-2 border rounded" />
      </label>

      <!-- Constituency Dropdown -->
      <label class="block">
        <span class="text-gray-700">Constituency</span>
        <select v-model="constituency" required class="w-full p-2 border rounded">
          <option value="" disabled>Select Constituency</option>
          <option v-for="c in constituencies" :key="c.id" :value="c.id">{{ c.name }}</option>
        </select>
      </label>

      <!-- Add New Constituency Button -->
      <button type="button" @click="isAddingConstituency = true" class="text-green-600 hover:underline">
        ➕ Add New Constituency
      </button>

      <label class="block">
        <span class="text-gray-700">Status</span>
        <select v-model="status" required class="w-full p-2 border rounded">
          <option value="Not Started">Not Started</option>
          <option value="Ongoing">Ongoing</option>
          <option value="Completed">Completed</option>
        </select>
      </label>

      <label class="block">
        <span class="text-gray-700">Contracting Company</span>
        <input v-model="contractingCompany" type="text" required class="w-full p-2 border rounded" />
      </label>

      <label class="block">
        <span class="text-gray-700">Contract Date</span>
        <input v-model="contractDate" type="date" required class="w-full p-2 border rounded" />
      </label>

      <div class="flex justify-end space-x-2">
        <button type="button" @click="$emit('close')" class="px-4 py-2 bg-gray-500 text-white rounded">
          Cancel
        </button>
        <button type="submit" :disabled="isSubmitting" class="px-4 py-2 bg-green-600 text-white rounded">
          {{ isSubmitting ? "Saving..." : "Add Project" }}
        </button>
      </div>
    </form>
  </div>

  <!-- Add Constituency Form -->
  <AddConstituency
      v-if="isAddingConstituency"
      @close="isAddingConstituency = false"
      @constituencyAdded="isAddingConstituency = false; fetchConstituencies()"
      @openAddCounty="isAddingConstituency = false; isAddingCounty = true"
  />

  <!-- Add County Form -->
  <AddCounty
      v-if="isAddingCounty"
      @close="isAddingCounty = false; isAddingConstituency = true"
  />
  <AddRegion
      v-if="isAddingRegion"
      @close="isAddingRegion = false"
      @regionAdded="isAddingRegion = false; fetchRegions()"
  />
</template>
