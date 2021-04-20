<template>
	<div class="circle-list">
		<circle-list-circle-view v-for="(circle, index) of $store.getters.getCircles" v-bind:circle="circle" v-bind:index="index + 1"></circle-list-circle-view>
	</div>
</template>

<script>
import CircleListCircleView from "@/components/CircleListCircleView";
export default {
	name: "CircleListView",
	components: {
		CircleListCircleView
	},
};
</script>

<style lang="scss" scoped>
</style>
