import PdfViewer from "@/components/PdfViewer";

export default {
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
		},
	}
}
