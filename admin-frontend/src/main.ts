import { createApp } from 'vue';
import { createPinia } from "pinia";

import router from './router';
import './style.css';
import App from "./App.vue";
import PrimeVue from "primevue/config";
import { MotionPlugin } from "@vueuse/motion";



const app = createApp(App);
const pinia = createPinia();

app.use(MotionPlugin);
app.use(pinia);
app.use(PrimeVue)
app.use(router);
app.mount('#app');