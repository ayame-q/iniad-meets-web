<template>
	<form class="chat-form" @submit.prevent="submit" v-click-outside="closeOption" v-bind:class="{'as-circle': isCircleMessage, 'as-admin': isAdminMessage}">
		<div class="chat-option-wrap" v-bind:class="{'active': isChatOptionOpen}">
			<div class="close-bar" v-on:click="closeOptionForce">
				<p><img src="@/assets/img/close_chat_option.svg" alt="閉じる"></p>
			</div>
			<p v-if="parentUuid" class="parent">
				返信先
				<span class="delete" v-on:click="deleteParent">×</span>
				<chat-log-view v-bind:chat-log="parentInstance" v-bind:without-actions="true"></chat-log-view>
			</p>
			<p>
				<input type="checkbox" id="chat-form-question" v-model="isQuestion"><label for="chat-form-question">サークルへ質問</label>
				<select class="circle-list" v-bind:class="{'active': isQuestion}" v-model="receiverCircleUuid">
					<option v-for="circle of $store.getters.getCircles" v-bind:value="circle.uuid">{{ circle.name }}</option>
				</select>
			</p>
			<p v-if="isQuestion"><input type="checkbox" id="chat-form-anonymous" v-model="isAnonymous"><label for="chat-form-anonymous">匿名で送信</label></p>
			<p v-if="$store.getters.getMyStaffCircles">
				<input type="checkbox" id="chat-form-circle" v-model="isCircleMessage" v-on:input="isCircleMessageInputChanged=true"><label for="chat-form-circle">サークルとして送信</label>
				<select class="circle-list" v-bind:class="{'active': isCircleMessage}" v-model="senderCircleUuid" v-on:input="isCircleMessageInputChanged=true">
					<option v-for="circle of $store.getters.getMyStaffCircles" v-bind:value="circle.uuid">{{ circle.name }}</option>
				</select>
			</p>
			<p v-if="$store.getters.getIsAdmin"><input type="checkbox" id="chat-form-admin_message" v-model="isAdminMessage"><label for="chat-form-admin_message">運営として送信</label></p>
		</div>
		<p><textarea v-model="comment" class="input-comment" placeholder="質問・メッセージを送信" rows="1" v-on:input="input" v-on:click="openOption" v-on:keydown.ctrl.enter="submit" v-on:keydown.meta.enter="submit"></textarea></p>
		<p><button type="submit"><img src="@/assets/img/chat_submit.svg" alt="送信"></button></p>
	</form>
</template>

<script>
import ClickOutside from "vue-click-outside";
import ChatLogView from "@/components/ChatLogView";

export default {
	name: "ChatForm",
	components: {ChatLogView},
	data() {
		return {
			isChatOptionOpenInput: false,
			comment: null,
			isQuestion: false,
			isAnonymousInput: false,
			isCircleMessageInput: false,
			isCircleMessageInputChanged: false,
			senderCircleUuidInput: null,
			receiverCircleUuidInput: null,
			isAdminMessage: false,
		}
	},
	computed: {
		isChatOptionOpen: {
			set(input) {
				this.isChatOptionOpenInput = input
			},
			get() {
				if (this.parentUuid) {
					return true
				}
				return this.isChatOptionOpenInput
			}
		},
		isAnonymous: {
			get() {
				if (!this.isQuestion) {
					return false
				}
				return this.isAnonymousInput
			},
			set(input) {
				this.isAnonymousInput = input
			}
		},
		getParentReceiverCircleIncludedMyStaffCircleUuid(){
			if (this.parentUuid && this.$store.getters.getMyStaffCircles.find((item) => {return this.parentInstance.receiver_circle && item.uuid === this.parentInstance.receiver_circle.uuid })) {
				return this.parentInstance.receiver_circle.uuid
			}
			return null
		},
		isCircleMessage: {
			set(input) {
				this.isCircleMessageInput = input
			},
			get() {
				if (!this.isCircleMessageInputChanged && this.getParentReceiverCircleIncludedMyStaffCircleUuid) {
					return true
				}
				return this.isCircleMessageInput
			}
		},
		senderCircleUuid: {
			get() {
				if (!this.isCircleMessage) {
					return null
				}
				if (!this.isCircleMessageInputChanged && this.getParentReceiverCircleIncludedMyStaffCircleUuid) {
					return this.getParentReceiverCircleIncludedMyStaffCircleUuid
				}
				if (this.$store.getters.getMyStaffCircles[0] && !this.senderCircleUuidInput) {
					return this.$store.getters.getMyStaffCircles[0].uuid
				}
				return this.senderCircleUuidInput
			},
			set(input) {
				this.senderCircleUuidInput = input
			}
		},
		receiverCircleUuid: {
			get() {
				if (!this.isQuestion) {
					return null
				}
				return this.receiverCircleUuidInput
			},
			set(input) {
				this.receiverCircleUuidInput = input
			}
		},
		parentUuid: {
			set(input) {
				this.$store.commit("setChatFormParentUuid", input)
			},
			get() {
				return this.$store.getters.getChatFormParentUuid
			}
		},
		parentInstance() {
			if (!this.parentUuid) {
				return null
			}
			return this.$store.getters.getChatLogs.find((item) => {
				return item.uuid === this.parentUuid
			})
		}
	},
	methods: {
		submit() {
			if (!this.comment) {
				this.isChatOptionOpen = false
				return
			}
			this.$store.dispatch("sendChatMessage", {
				comment: this.comment,
				senderCircleUuid: this.senderCircleUuid,
				receiverCircleUuid: this.receiverCircleUuid,
				parent: this.parentUuid,
				isAnonymous: this.isAnonymous,
				isAdminMessage: this.isAdminMessage
			})
			this.isCircleMessageInputChanged = false
			this.isChatOptionOpen = false
			this.comment = null
			this.isQuestion = false
			this.parentUuid = null
		},
		input(event) {
			if (this.comment) {
				this.isChatOptionOpen = true
			}
			const target = event.target
			target.style.height = "auto"
			this.$nextTick(() => {
				target.style.height = target.scrollHeight + "px"
			})
		},
		closeOption() {
			if (!this.comment){
				this.isChatOptionOpen = false
				this.isCircleMessageInputChanged = false
			}
		},
		closeOptionForce() {
			this.isChatOptionOpen = false
		},
		openOption() {
			this.isChatOptionOpen = true
		},
		deleteParent() {
			this.parentUuid = null
			this.isCircleMessageInputChanged = false
		}
	},
	directives: {
		ClickOutside,
		ChatLogView
	}
};
</script>

<style lang="scss" scoped>
form{
	color: #FFFFFF;
	background-color: $sub-color;
	padding: 0.8em 1.5em;
	position: relative;
	&.as-circle{
		background-color: $theme-color;
	}
	&.as-admin{
		background-color: #D3AD14;
	}
	.chat-option-wrap{
		display: flex;
		flex-wrap: wrap;
		visibility: hidden;
		height: 0;
		&.active{
			margin-top: 1em;
			height: auto;
			visibility: visible;
			margin-bottom: 0.5em;
		}
		> p{
			margin-right: 1em;
			display: flex;
			align-items: center;
			input, label{
				flex-shrink: 0;
				flex-grow: 0;

			}
			.circle-list{
				display: none;
				flex-shrink: 1;
				flex-grow: 1;
				margin-left: 1em;
				margin-right: calc(-1em / 0.8);
				font-size: 0.8em;
				&.active{
					display: block;
				}
			}

			&.parent{
				display: block;
				font-size: 0.8em;
				width: 100%;
				position: relative;
				margin-right: 0;
				background-color: rgba(#FFFFFF, 0.1);
				padding: 0.5em;
				border-radius: 0.5em;
				margin-bottom: 0.5em;
				.delete{
					position: absolute;
					top: 0.2em;
					right: 0.4em;
					cursor: pointer;
					font-size: 1.4em;
				}
			}
		}
		.close-bar{
			position: absolute;
			top: 0;
			left: 0;
			width: 100%;
			text-align: center;
			background-color: $sub-color;
			padding: 0.1em;
			img{
				height: 0.8em;
			}
		}
		select{
		}
	}
	textarea{
		max-height: 25vh;
		resize: none;
	}
	button[type=submit]{
		position: absolute;
		width: 1.8em;
		height: 1.8em;
		padding: 0;
		bottom: 0.8em;
		right: 1.8em;
		background-color: rgba(#FFFFFF, 0);
	}
	.input-comment{
		padding-right: 0.8em + 1.8em;
	}
}
</style>

<style lang="scss">
form.chat-form{
	.chat-log{
		background-color: transparent;
		margin: 0;
		padding-top: 0;
		padding-bottom: 0;
		.parent-message{
			background-color: #FFFFFF;
		}
	}
}
</style>
