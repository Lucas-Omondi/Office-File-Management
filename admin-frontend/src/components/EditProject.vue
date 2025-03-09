<script setup lang="ts">
import { ref, defineProps, defineEmits, watchEffect, toRaw } from "vue";
import axios from "axios";

const props = defineProps(["show", "project"]);
const emit = defineEmits(["close", "projectUpdated"]);

const editedProject = ref({});

watchEffect(() => {
  if (props.project) {
    editedProject.value = { ...props.project };  // ✅ Update immediately when project changes
  }
});

const saveChanges = async () => {
  try {
    if (!editedProject.value) return;

    const token = localStorage.getItem("accessToken");
    if (!token) {
      console.error("No access token found. Please log in.");
      return;
    }

    const projectData = toRaw(editedProject.value); // ✅ Ensure raw object is sent

    console.log("Updating project with data:", JSON.stringify(projectData, null, 2));

    await axios.put(`http://127.0.0.1:8000/api/projects/${projectData.id}/`, projectData, {
      headers: { Authorization: `Bearer ${token}`, "Content-Type": "application/json" },
    });

    console.log("✅ Project updated successfully");
    emit("projectUpdated", projectData);
    emit("close");
  } catch (error) {
    console.error("❌ Error updating project:", error.response?.data || error.message);
  }
};
</script>

<template>
  <div v-if="show" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center">
    <div class="bg-white p-6 rounded shadow-lg w-1/3">
      <h2 class="text-xl font-semibold mb-4">Edit Project</h2>

      <label class="block mb-2">RFX Number</label>
      <input v-model="editedProject.rfx_number" class="border p-2 w-full rounded mb-4" />

      <label class="block mb-2">Project Name</label>
      <input v-model="editedProject.name" class="border p-2 w-full rounded mb-4" />

      <label class="block mb-2">Contractor</label>
      <input v-model="editedProject.contracting_company" class="border p-2 w-full rounded mb-4" />

      <label class="block mb-2">Contract Date</label>
      <input type="date" v-model="editedProject.contract_date" class="border p-2 w-full rounded mb-4" />

      <label class="block mb-2">Status</label>
      <select v-model="editedProject.status" class="border p-2 w-full rounded mb-4">
        <option value="Not Started">Not Started</option>
        <option value="Ongoing">In Progress</option>
        <option value="Completed">Completed</option>
      </select>

      <div class="flex justify-end gap-2">
        <button @click="$emit('close')" class="bg-gray-400 text-white px-4 py-2 rounded">Cancel</button>
        <button @click="saveChanges" class="bg-green-600 text-white px-4 py-2 rounded">Save</button>
      </div>
    </div>
  </div>
</template>
