<script setup>
import { ref } from 'vue';
import Modal from '../components/Modal.vue';

const isOpen = ref(false);
</script>

<template>
  <div>
    <!-- Floating Compose Button -->
    <button
        @click="isOpen = true"
        class="fixed bottom-6 right-6 bg-green-600 hover:bg-green-700 text-white font-medium py-3 px-6 rounded-full shadow-lg transition-all duration-300 flex items-center gap-2">
      <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M12 5v14M5 12h14"/>
      </svg>
      <span class="hidden sm:inline">Compose</span>
    </button>

    <!-- Modal -->
    <Modal v-if="isOpen" @close="isOpen = false" />
  </div>
</template>
