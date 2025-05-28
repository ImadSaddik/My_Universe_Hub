import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import axios from "axios";
import VueLazyload from "vue3-lazyload";
import loadingGif from "@/assets/loading.gif";

axios.defaults.baseURL = "http://localhost:8000";
// axios.defaults.baseURL = 'http://192.168.1.10:8000'

const app = createApp(App);

app.use(store);
app.use(router, axios);
app.use(VueLazyload, {
  loading: loadingGif,
});

app.mount("#app");
