<template>
	<div class="entry-button-wrap">
		<p class="entry-button"><button v-on:click="startEntry">入会はこちら</button></p>
	</div>
</template>

<script>
import UpdateUserNameForm from "@/components/UpdateUserNameForm";
import entryCircle from "@/mixins/entryCircle";

export default {
	name: "EntryButton",
	props: {
		circle: Object
	},
	methods: {
		openUpdateUserNameForm() {
			this.$modal.show(
				UpdateUserNameForm,
				{
					circle: this.circle
				},
				{
					width: "40%",
					draggable: true,
				}
			)
		},
		startEntry() {
			const myUser = this.$store.getters.getMyUser
			if(myUser.family_name && myUser.given_name) {
				this.entry(this.circle)
			} else {
				this.openUpdateUserNameForm()
			}
		}
	},
	mixins: [
		entryCircle
	]
};
</script>

<style lang="scss" scoped>
.entry-button{
	width: fit-content;
	button{
		font-size: 0.85em;
		color: #FFFFFF;
		background-color: $sub-color;
		border-radius: 1.5em;
		padding: 0.5em 1.2em;
	}
}
</style>
