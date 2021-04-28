<template>
	<div class="home">
		<teaser-page v-if="!is_open"></teaser-page>
		<entrance-page v-if="is_open"></entrance-page>
	</div>
</template>

<script>
import TeaserPage from "@/views/TeaserPage";
import EntrancePage from "@/views/EntrancePage";
import axios from "axios";

export default {
	name: "Home",
	data() {
		return {
			is_open: false
		}
	},
	components: {
		TeaserPage,
		EntrancePage
	},
	created() {
		axios.get("/api/v2/is_open")
		.then((result) => {
			this.is_open = result.data.is_open
		})
	}
};
</script>
