import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import VModal from 'vue-js-modal'
import { library } from '@fortawesome/fontawesome-svg-core'
import { faTwitter, faInstagram, faLine } from '@fortawesome/free-brands-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faTwitter, faInstagram, faLine)

Vue.component('font-awesome-icon', FontAwesomeIcon)

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
