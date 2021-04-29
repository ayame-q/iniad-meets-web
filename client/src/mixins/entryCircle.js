import axios from "axios";

export default {
	methods: {
		entry(circle) {
			this.isPending = true
			axios.post("/api/v2/entry/",{
				circle: circle.uuid
			}, {withCredentials: true, headers: {"X-CSRFToken": this.$cookies.get("csrftoken")}})
				.then((response) => {
					this.$store.commit("addEnteredCircle", {
						uuid: response.data.circle
					})
					this.$toast.show(`${circle.name} の入会受付が完了しました。サークルよりINIADメールアドレスに連絡が届きますのでお待ちください。`)
					this.isPending = false
				})
				.catch((error) => {
					this.$toast.show(error.response.data[0])
					this.isPending = false
				})
			this.$emit("close")
		},
	}
}
