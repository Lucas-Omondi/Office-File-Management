import { createApp } from 'vue';
import App from './App.vue';
import { createPinia } from "pinia";
import { Motion } from "@motionone/vue";
import router from './router';
import './style.css';

const app = createApp(App);
const pinia = createPinia();

app.use(pinia);
app.directive("motion", Motion);
app.use(router);
app.mount('#app');