<template>
	<form class="display-name-form" @submit.prevent="submit">
		<h3 style="display: none">公開名登録</h3>
		<p class="description">
			チャットで利用する公開名を登録してください。
		</p>
		<div class="name-wrap">
			<div class="name-line">
				<p>
					<label for="display-name">公開名</label>
					<input type="text" id="display-name" v-model="display_name" placeholder="みーちゅ" required>
				</p>
			</div>
		</div>
		<p class="submit-button-wrap"><input type="submit" value="登録"></p>
	</form>
</template>

<script>
import axios from "axios";

export default {
	name: "UpdateUserDisplayNameForm",
	data() {
		return {
			display_name: null,
		}
	},
	methods: {
		submit() {
			axios.patch("/api/v2/user/", {
				display_name: this.display_name,
			}, {withCredentials: true, headers: {"X-CSRFToken": this.$cookies.get("csrftoken")}})
				.then((response) => {
					this.$store.commit("setMyUser", Object.assign(this.$store.getters.getMyUser, response.data))
					this.$emit("close")
				})
		}
	},
};
</script>

<style lang="scss" scoped>

.display-name-form{
	padding: 20px;
	font-size: 1em;
	box-shadow: 5px 5px 5px $shadow-color;
	color: $text-color;
	.description{
		font-size: 0.7em;
	}
	.name-wrap{
		background-color: $theme-color;
		padding: 1.5em 2.5em;
		margin-top: 1em;
		font-size: 0.8em;
		color: #FFFFFF;
		.name-line{
			width: 100%;
			display: flex;
			&:not(:first-child){
				margin-top: 1em;
			}
			p{
				width: 49%;
				&:not(:last-child){
					margin-right: 2%;
				}
			}

		}
	}
	.submit-button-wrap{
		margin-top: 1em;
		display: flex;
		justify-content: flex-end;
		input[type=submit]{
			font-size: 0.85em;
			color: #FFFFFF;
			background-color: $sub-color;
			border-radius: 1.5em;
			padding: 0.5em 3em;
			width: fit-content;
		}
	}
}
</style>
