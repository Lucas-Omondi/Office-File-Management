<script setup lang="ts">
import { ref, defineEmits } from "vue";
import axios from "axios";

const emit = defineEmits(["close", "regionAdded"]);

const regionForm = ref({
  name: ""
});

const loading = ref(false);
const error = ref("");

const submitRegion = async () => {
  loading.value = true;
  try {
    const token = localStorage.getItem("accessToken");
    if (!token) {
      error.value = "Authentication required. Please log in.";
      return;
    }
    await axios.post("http://127.0.0.1:8000/api/regions/", regionForm.value, {
      headers: { Authorization: `Bearer ${token}` },
    });
    emit("regionAdded");
    emit("close");
  } catch (err) {
    console.error("Error adding region:", err.response?.data || err.message);
    error.value = "Failed to add region. Please try again.";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <!-- Modal Overlay -->
  <Teleport to="body">
    <div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <!-- Modal Content -->
      <div class="bg-white p-6 rounded shadow-lg w-96">
        <h2 class="text-xl font-semibold mb-4">Add New Region</h2>

        <form @submit.prevent="submitRegion" class="space-y-4">
          <input v-model="regionForm.name" placeholder="Region Name"
                 class="border p-2 w-full rounded bg-white text-black" required />

          <div class="flex justify-end space-x-2">
            <button type="button" @click="emit('close')"
                    class="px-4 py-2 bg-gray-500 text-white rounded">
              Cancel
            </button>
            <button type="submit" :disabled="loading"
                    class="px-4 py-2 bg-green-600 text-white rounded">
              {{ loading ? "Saving..." : "Save Region" }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </Teleport>
</template>
