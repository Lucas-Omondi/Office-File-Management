<script setup lang="ts">
import { ref, defineEmits, onMounted } from "vue";
import axios from "axios";
import AddRegion from "./AddRegion.vue"; // ✅ Import AddRegion

const emit = defineEmits(["close", "countyAdded"]);

const countyForm = ref({
  name: "",
  region: ""
});

const regions = ref([]);
const loading = ref(false);
const error = ref("");
const isAddingRegion = ref(false); // ✅ Track region modal visibility

const fetchRegions = async () => {
  try {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      error.value = "Authentication required. Please log in.";
      return;
    }
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/regions/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    regions.value = response.data;
  } catch (err) {
    console.error("Error fetching regions:", err.response?.data || err.message);
  }
};

const submitCounty = async () => {
  loading.value = true;
  try {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      error.value = "Authentication required. Please log in.";
      return;
    }
    await axios.post(`${import.meta.env.VITE_API_BASE_URL}/counties/`, countyForm.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    emit("countyAdded");
    emit("close");
  } catch (err) {
    console.error("Error adding county:", err.response?.data || err.message);
    error.value = "Failed to add county. Please try again.";
  } finally {
    loading.value = false;
  }
};

// ✅ Close region modal and refresh regions
const handleRegionAdded = () => {
  isAddingRegion.value = false;
  fetchRegions();
};

onMounted(fetchRegions);
</script>

<template>
  <!-- ✅ Hide this form when AddRegion is open -->
  <div v-if="!isAddingRegion" class="p-6">
    <h2 class="text-xl font-semibold mb-4">Add New County</h2>
    <form @submit.prevent="submitCounty" class="space-y-4">
      <input v-model="countyForm.name" placeholder="County Name" class="border p-2 w-full rounded" required />

      <div>
        <label class="block text-sm font-medium">Region</label>
        <select v-model="countyForm.region" class="border p-2 w-full rounded">
          <option value="" disabled selected>Select Region</option>
          <option v-for="region in regions" :key="region.id" :value="region.id">
            {{ region.name }}
          </option>
        </select>
        <button type="button" @click="isAddingRegion = true" class="mt-2 text-green-600 hover:underline">
          ➕ Add New Region
        </button>
      </div>

      <button type="submit" :disabled="loading" class="bg-green-600 text-white px-4 py-2 rounded">
        {{ loading ? "Saving..." : "Save County" }}
      </button>
      <button type="button" @click="emit('close')" class="ml-2 text-gray-500 hover:underline">Cancel</button>
    </form>
  </div>

  <!-- ✅ AddRegion modal (full overlay to match other modals) -->
  <Teleport to="body">
    <div v-if="isAddingRegion" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <AddRegion @close="isAddingRegion = false" @regionAdded="handleRegionAdded" />
      </div>
    </div>
  </Teleport>
</template>
