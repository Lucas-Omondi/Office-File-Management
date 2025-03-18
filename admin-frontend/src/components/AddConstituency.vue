<script setup lang="ts">
import { ref, defineEmits, onMounted } from "vue";
import axios from "axios";

const emit = defineEmits(["close", "constituencyAdded", "openAddCounty"]);

const constituencyForm = ref({
  name: "",
  county: ""
});

const counties = ref([]);
const loading = ref(false);
const error = ref("");

const fetchCounties = async () => {
  try {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      error.value = "Authentication required. Please log in.";
      return;
    }
    const response = await axios.get(`${import.meta.env.VITE_API_BASE_URL}/counties/`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    counties.value = response.data;
  } catch (err) {
    console.error("Error fetching counties:", err.response?.data || err.message);
  }
};

const submitConstituency = async () => {
  loading.value = true;
  error.value = "";

  console.log("Submitting constituency:", constituencyForm.value); // Debug log

  try {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      error.value = "Authentication required. Please log in.";
      return;
    }

    const response = await axios.post(`${import.meta.env.VITE_API_BASE_URL}/constituencies/`, constituencyForm.value, {
      headers: { Authorization: `Bearer ${token}` },
    });

    console.log("Response:", response.data); // Debug log

    emit("constituencyAdded"); // Notify parent
    emit("close"); // Close modal
  } catch (err) {
    console.error("Error adding constituency:", err.response?.data || err.message);

    // Show backend error if available
    if (err.response?.data) {
      error.value = JSON.stringify(err.response.data);
    } else {
      error.value = "Failed to add constituency. Please try again.";
    }
  } finally {
    loading.value = false;
  }
};



onMounted(fetchCounties);
</script>

<template>
  <div class="p-6">
    <h2 class="text-xl font-semibold mb-4">Add New Constituency</h2>
    <form @submit.prevent="submitConstituency" class="space-y-4">
      <input v-model="constituencyForm.name" placeholder="Constituency Name" class="border p-2 w-full rounded" required />

      <div>
        <label class="block text-sm font-medium">County</label>
        <select v-model="constituencyForm.county" class="border p-2 w-full rounded">
          <option value="" disabled selected>Select County</option>
          <option v-for="county in counties" :key="county.id" :value="county.id">
            {{ county.name }}
          </option>
        </select>
        <button type="button" @click="emit('openAddCounty')" class="mt-2 text-green-600 hover:underline">
          ➕ Add New County
        </button>
      </div>

      <button type="submit" :disabled="loading" class="bg-green-600 text-white px-4 py-2 rounded">
        {{ loading ? "Saving..." : "Save Constituency" }}
      </button>
      <button type="button" @click="emit('close')" class="ml-2 text-gray-500 hover:underline">Cancel</button>
    </form>
  </div>
</template>
