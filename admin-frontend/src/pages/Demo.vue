<script setup lang="ts">
import { ref } from "vue";
import Modal from "../components/Modal.vue";

const showModal = ref(false);
</script>

<template>
  <div>
    <button @click="showModal = true" class="bg-green-600 text-white px-4 py-2 rounded-lg">
      Open Modal
    </button>

    <Modal title="Test Modal" :show="showModal" :onClose="() => (showModal = false)">
      <p>This is a simple test modal!</p>
    </Modal>
  </div>
</template>
