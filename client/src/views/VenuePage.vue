<template>
	<div class="venue-page">
		会場
		<button v-on:click="openMaterial('https://esa-storage-tokyo.s3-ap-northeast-1.amazonaws.com/uploads/production/attachments/15779/2021/03/20/75146/b26efeb5-47f7-4510-ada5-9f334810c178.pdf')">PDF</button>
	</div>
</template>

<script>
import PdfViewer from "@/components/PdfViewer";

export default {
	name: "VenuePage",
	components: {PdfViewer},
	methods: {
		openMaterial(src) {
			this.$modal.show(
				PdfViewer,
				{src: src},
				{
					width: "95%",
					height: "95%",
					draggable: false,
				}
			)
		}
	},
};
</script>

<style scoped>

</style>
