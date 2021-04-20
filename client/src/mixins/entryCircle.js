import axios from "axios";

export default {
	methods: {
		entry(circle) {
			axios.post("/api/v2/entry/",{
				circle: circle.uuid
			}, {withCredentials: true, headers: {"X-CSRFToken": this.$cookies.get("csrftoken")}})
				.then((response) => {
					this.$toast.show(`${circle.name} の入会受付が完了しました。`)
				})
				.catch((error) => {
					this.$toast.show(error.response.data[0])
				})
			this.$emit("close")
		},
	}
}
