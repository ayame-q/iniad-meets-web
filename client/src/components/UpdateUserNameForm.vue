<template>
	<form class="name-form" @submit.prevent="submit">
		<h3 style="display: none">サークル入会情報登録</h3>
		<p class="description">
			サークルの入会には氏名の登録が必要です。<br>
			大学事務課への提出に必要なため本名を入力してください。
		</p>
		<div class="name-wrap">
			<div class="name-line">
				<p>
					<label for="form-family-name">姓</label>
					<input type="text" id="form-family-name" v-model="family_name" placeholder="東洋" required>
				</p>
				<p>
					<label for="form-given-name">名</label>
					<input type="text" id="form-given-name" v-model="given_name" placeholder="太郎" required>
				</p>
			</div>
			<div class="name-line">
				<p>
					<label for="form-family-name-ruby">フリガナ(姓)</label>
					<input type="text" id="form-family-name-ruby" v-model="family_name_ruby" placeholder="トウヨウ" required>
				</p>
				<p>
					<label for="form-given-name-ruby">フリガナ(名)</label>
					<input type="text" id="form-given-name-ruby" v-model="given_name_ruby" placeholder="タロウ" required>
				</p>
			</div>
		</div>
		<p class="submit-button-wrap"><input type="submit" value="登録"></p>
	</form>
</template>

<script>
import axios from "axios";
import entryCircle from "@/mixins/entryCircle";
export default {
	name: "UpdateUserNameForm",
	data() {
		return {
			family_name: null,
			given_name: null,
			family_name_ruby: null,
			given_name_ruby: null
		}
	},
	props: {
		circle: {
			type: Object,
			default: null
		}
	},
	methods: {
		submit() {
			axios.patch("/api/v2/user/", {
				family_name: this.family_name,
				given_name: this.given_name,
				family_name_ruby: this.family_name_ruby,
				given_name_ruby: this.given_name_ruby
			}, {withCredentials: true, headers: {"X-CSRFToken": this.$cookies.get("csrftoken")}})
			.then((response) => {
				this.$store.commit("setMyUser", Object.assign(this.$store.getters.getMyUser, response.data))
				if (this.circle) {
					this.entry(this.circle)
				}
			})
		}
	},
	mixins: [
		entryCircle
	]
};
</script>

<style lang="scss" scoped>
.name-form{
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
