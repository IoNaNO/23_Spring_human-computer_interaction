import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import axios from "axios";
// import "~/styles/element/index.scss";

import ElementPlus from "element-plus";
// import all element css, uncommented next line

// or use cdn, uncomment cdn link in `index.html`

import "~/styles/index.scss";
import "uno.css";

// If you want to use ElMessage, import it.
import "element-plus/theme-chalk/src/message.scss";
import "element-plus/theme-chalk/src/button.scss";


import "element-plus/dist/index.css";
axios.defaults.baseURL='http://localhost:5000';
axios.defaults.timeout=10000;
const app = createApp(App);
app.use(router);
app.config.globalProperties.$axios = axios;
app.use(ElementPlus);
app.mount("#app");
