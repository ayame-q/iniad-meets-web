<template>
	<div class="entry-button-wrap">
		<p class="entry-button">
			<button v-on:click="startEntry" v-bind:disabled="isPending || isEntered" v-bind:class="{'entered': isEntered, 'pending': isPending}">{{ entryButtonText }}</button>
		</p>
	</div>
</template>

<script>
import UpdateUserNameForm from "@/components/UpdateUserNameForm";
import entryCircle from "@/mixins/entryCircle";

export default {
	name: "EntryButton",
	props: {
		circle: Object,
	},
	data() {
		return {
			isPending: false
		}
	},
	computed: {
		isEntered() {
			return this.$store.getters.getMyEnteredCircles.find((item) => {
				return item.uuid === this.circle.uuid
			})
		},
		entryButtonText() {
			if (this.isEntered) {
				return "入会済"
			}
			if (this.isPending) {
				return ""
			}
			return "入会はこちら"
		},
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
				this.$modal.show('dialog', {
					title: '確認',
					text: `${this.circle.name}に入会しますか？`,
					buttons: [
						{
							title: 'キャンセル',
							handler: () => {
								this.$modal.hide('dialog')
							}
						},
						{
							title: '入会する',
							handler: () => {
								this.isPending = true
								this.entry(this.circle)
								this.$modal.hide('dialog')
							}
						}
					]
				})
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
@keyframes pending {
	0%{
		transform: rotate(0deg);
	}
	100%{
		transform: rotate(360deg);
	}
}
.entry-button{
	width: fit-content;
	button{
		font-size: 0.85em;
		color: #FFFFFF;
		background-color: $sub-color;
		border-radius: 1.5em;
		padding: 0.5em 1.2em;

		&:hover{
			text-decoration: underline;
		}

		&:disabled{
			cursor: default;
		}
		&.entered{
			background: $light-button-color;
		}
		&.pending{
			content: "";
			width: 2em;
			height: 2em;
			top: 50%;
			left: 50%;
			transform: translateY(-50%) translateX(-50%);
			margin: auto;
			padding: 0;
			background-color: #FFFFFF;
			border-color: #cbcbcb;
			border-width:3px;
			border-style: solid;
			border-radius: 100%;
			border-left-color: $sub-color;
			animation: pending 2s 0.25s linear infinite;
		}
	}
}
</style>
