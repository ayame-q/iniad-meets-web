<template>
	<div class="pdf-viewer">
		<embed v-bind:src="`${src}#toolbar=0&navpanes=0`">
		<p class="close" v-on:click="$emit('close')">閉じる</p>
	</div>
</template>

<script>
export default {
	name: "PdfViewer",
	props: {
		src: String
	},
};
</script>

<style scoped>
.pdf-viewer{
	margin: 0;
	padding: 0;
	width: 100%;
	height: 100%;
	position: relative;
}
embed{
	width: 100%;
	height: 100%;
	overflow-y: scroll;
}
.close{
	position: absolute;
	cursor: pointer;
	top: 0;
	right: 0;
	color: #730201;
	background-color: #ff675f;
	border-radius: 0.5em;
	font-size: 1.2em;
	margin: 1em;
	padding: 0.3em 0.5em;
}
</style>
