<template>
	<article class="chat-log" v-bind:class="{
		'question': chatLog.is_question,
		'circle-message': chatLog.sender_circle,
		'admin-message': chatLog.is_admin_message,
		'parent-message': isParent
	}" v-bind:id="'chat-log-' + chatLog.uuid">
		<header>
			<h3><span v-if="chatLog.sender_circle">{{ chatLog.sender_circle.name }}</span><span v-bind:class="{'name-with-circle': chatLog.sender_circle}">{{ chatLog.send_user_name }}</span></h3>
			<p class="time"><time>{{ chatLog.created_at.format("MM/DD HH:mm") }}</time></p>
		</header>
		<div class="comment">
			<div class="mention" v-bind:class="{'pointer': chatLog.parent}" v-if="chatLog.receiver_user || chatLog.receiver_circle" v-on:click.self="openParentBox" v-click-outside="closeParentBox">
				@{{ getReceiverName }}

				<div class="parent-box" v-if="chatLog.parent && isParentBoxActive" v-bind:style="parentBoxPosition">
					<chat-log-view v-bind:chat-log="chatLog.parent" v-bind:is-parent="true" v-bind:without-actions="withoutActions"></chat-log-view>
				</div>
			</div>
			{{ chatLog.comment }}
		</div>
		<footer v-if="!withoutActions">
			<ul class="reactions">
				<li
					v-for="(object, reaction) of getReactionList"
					v-bind:class="{'active': object.hasMine}"
					v-on:click="toggleChatReaction(reaction, object)"
				>
					{{ reaction }} {{ object.count }}
				</li>
			</ul>
			<ul class="action-button">
				<li v-on:click="toggleReactionAddBoxActive" v-click-outside="closeReactionAddBox">
					<img src="@/assets/img/add_reaction.svg" alt="リアクション">
					<ul class="reaction-add-box" v-if="isReactionAddBoxActive" v-bind:style="reactionAddBoxPosition">
						<li v-for="emoji of $store.getters.getReactionEmojis" v-on:click="addChatReaction(emoji)">{{ emoji }}</li>
					</ul>
				</li>
				<li v-on:click="addParent"><img src="@/assets/img/reply.svg" alt="返信"></li>
			</ul>
		</footer>
	</article>
</template>

<script>
import dayjs from "dayjs";
import ClickOutside from 'vue-click-outside'

export default {
	name: "ChatLogView",
	props: {
		chatLog: Object,
		withoutActions: {
			type: Boolean,
			default: false,
		},
		isParent: {
			type: Boolean,
			default: false
		}
	},
	data() {
		return {
			isReactionAddBoxActive: false,
			reactionAddBoxPosition: {
				top: null,
				right: null,
			},
			isParentBoxActive: false,
			parentBoxPosition: {
				top: null,
				right: null,
			}
		}
	},
	computed: {
		getReceiverName() {
			if (this.chatLog.receiver_circle) {
				return this.chatLog.receiver_circle.name
			}
			if (this.chatLog.receiver_user) {
				return this.chatLog.receiver_user.name
			}
		},
		getReactionList() {
			const reactions = {}
			for (const reaction of this.chatLog.reactions) {
				if (!reactions[reaction.reaction]) {
					reactions[reaction.reaction] = {
						count: 1,
						hasMine: false
					}
				} else {
					reactions[reaction.reaction].count++
				}
				if (reaction.user.uuid === this.$store.getters.getMyUuid) {
					reactions[reaction.reaction].hasMine = true
				}
			}
			return reactions
		}
	},
	methods: {
		addParent() {
			this.$store.commit("setChatFormParentUuid", this.chatLog.uuid)
		},
		addChatReaction(reaction) {
			this.$store.dispatch("addChatReaction", {messageUuid: this.chatLog.uuid, reaction: reaction})
		},
		toggleChatReaction(reaction, object) {
			if (!object.hasMine) {
				this.$store.dispatch("addChatReaction", {messageUuid: this.chatLog.uuid, reaction: reaction})
			} else {
				this.$store.dispatch("removeChatReaction", {messageUuid: this.chatLog.uuid, reaction: reaction})
			}
		},
		toggleReactionAddBoxActive(event) {
			this.isReactionAddBoxActive = !this.isReactionAddBoxActive
			this.reactionAddBoxPosition = {
				top: event.clientY + "px",
				right: document.getElementsByTagName("body")[0].clientWidth - event.clientX + "px",
			}
		},
		closeReactionAddBox() {
			this.isReactionAddBoxActive = false
		},
		openParentBox(event) {
			this.isParentBoxActive = true
			this.parentBoxPosition = {
				top: event.clientY + "px",
				left: event.clientX + "px",
			}
		},
		closeParentBox() {
			this.isParentBoxActive = false
		},
	},
	mounted() {
		if (!this.$store.getters.getChatLogWrapScrolledAt || dayjs().diff(this.$store.getters.getChatLogWrapScrolledAt) > 10 * 60 * 1000){ // 10分
			this.$store.commit("startChatLogWrapScrollAuto")
			this.$nextTick(() => {
				const chatLogWrapElement = document.getElementById("chat-log-wrap")
				chatLogWrapElement.scrollTop = chatLogWrapElement.scrollHeight
				this.$nextTick(() => {
					setTimeout(() => {
						this.$store.commit("endChatLogWrapScrollAuto")
					})
				})
			})
		}
	},
	directives: {
		ClickOutside
	}
};
</script>

<style lang="scss" scoped>
.chat-log{
	font-size: 0.75em;
	margin: 1em;
	padding: 0 1em;
	padding-left: 3em;
	border-radius: 1.2em;
	background-color: #FFFFFF;
	&:first-child{
		margin-top: 0;
	}
	&.question, &.circle-message, &.admin-message, &.parent-message{
		padding: 1em;
		padding-left: 3em;
	}
	&.parent-message{
		box-shadow: 3px 3px 5px $shadow-color;
	}
	&.question{
		background-color: #F9D2D2;

		footer ul.reactions li.active{
			background-color: rgba(#FFFFFF, 0.6);
			border: $sub-color solid 2px;
		}
	}
	&.circle-message{
		background-color: #ACDDE5;

		footer ul.reactions li.active{
			background-color: rgba(#FFFFFF, 0.6);
			border: $theme-color solid 2px;
		}
	}
	&.admin-message{
		background-color: #F5EBC3;

		footer ul.reactions li.active{
			background-color: rgba(#FFFFFF, 0.6);
			border: #EBC321 solid 2px;
		}
	}
	header{
		display: flex;
		align-items: baseline;
		margin-left: -2em;
		h3{
			font-weight: normal;
			font-size: 1.1em;
			span.name-with-circle{
				font-size: 0.6em;
				&::before{
					content: "(";
				}
				&::after{
					content: ")";
				}
			}
		}
		p.time{
			font-size: 0.8em;
			margin-left: 1em;
		}
	}
	line-height: 1.8;
	.mention{
		display: inline;
		color: $mention-color;
		background-color: rgba(#FFFFFF, 0.6);
		padding: 0.1em 0.2em;
		margin-right: 0.2em;

		.parent-box{
			font-size: calc(1em / 0.75);
			position: fixed;
			z-index: 98;
			padding: 0.3em;
			color: $text-color;
			width: 28vw;
		}
	}
	footer{
		display: flex;
		align-items: center;
		justify-content: stretch;
		width: 100%;
		margin-top: 0.5em;
		img{
			height: 0.8em;
		}
		ul.reactions{
			flex-shrink: 1;
			flex-grow: 1;
			display: flex;
			flex-wrap: wrap;
			padding: 0;
			list-style: none;
			li{
				color: $sub-color;
				cursor: pointer;
				background-color: rgba(#FFFFFF, 0.6);
				border-radius: 1em;
				font-size: 0.78em;
				padding: 0.1em 0.5em;
				margin-top: 0.2em;
				margin-right: 0.5em;
				border: rgba(#FFFFFF, 0) solid 2px;
				&.active{
					background-color: #eeeeee;
					border: #4D4D4D solid 2px;
				}
			}
		}
		ul.action-button{
			display: flex;
			padding: 0;
			list-style: none;
			li{
				margin: 0 0.2em;
				position: relative;
				cursor: pointer;
				ul.reaction-add-box{
					display: flex;
					position: fixed;
					z-index: 98;
					padding: 0.3em;
					flex-wrap: wrap;
					width: 12.2em;
					list-style: none;
					background-color: #FFFFFF;
					border-radius: 0.6em;
					box-shadow: 3px 3px 5px $shadow-color;
				}
			}
		}
	}
	
	.pointer{
		cursor: pointer;
	}
}
</style>
