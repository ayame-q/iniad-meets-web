import Vue from "vue";
import VueRouter from "vue-router";
import VueMeta from "vue-meta";
import VueGtag from "vue-gtag";

Vue.use(VueRouter);
Vue.use(VueMeta);

const routes = [
	{
		path: "/",
		name: "Index",
		component() {
			if (process.env.VUE_APP_TEASER) {
				return import("@/views/TeaserPage")
			}
			return import("@/views/VenuePage")
		},
	},
];

const router = new VueRouter({
	mode: "history",
	base: process.env.BASE_URL,
	routes,
});

if (process.env.VUE_APP_GOOGLE_ANALYTICS_ID){
	Vue.use(VueGtag, {
		config: { id: process.env.VUE_APP_GOOGLE_ANALYTICS_ID }
	}, router);
}

export default router;
