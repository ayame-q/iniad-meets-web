import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VModal from 'vue-js-modal'

Vue.config.productionTip = false;

new Vue({
	router,
	store,
	render: h => h(App),
}).$mount("#app");

Vue.use(VModal, {
	dialog: true,
	dynamicDefaults: {
		height: "auto",
		adaptive: true,
		focusTrap: true,
	}
})
