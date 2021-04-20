<template>
	<div class="venue-page">
		<header>
			<h1><img src="@/assets/img/logo.svg" alt="INIAD meets web"></h1>
			<div id="hamburger" v-bind:class="{ 'drawer-opened': isDrawerOpened }" v-on:click="isDrawerOpened = !isDrawerOpened">
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
				<span class="icon-bar"></span>
			</div>
		</header>
		<main>
			<div class="main-wrap">
				<section class="video-wrap">
					<video-view></video-view>
				</section>
				<section class="event-wrap">
					<event-view></event-view>
				</section>
			</div>
			<div class="side-wrap">
				<div class="chat-tab-wrap">
					<ul>
						<li class="chat-tab" v-for="(chatType, index) of chatTypes" v-bind:class="{ 'active': activeChatType === index }" v-on:click="setActiveChatType(index)">{{ chatType }}</li>
					</ul>
				</div>
				<div class="chat-wrap">
					<div id="chat-log-wrap" class="chat-log-wrap">
						<chat-log-view v-for="chatLog of getActiveChatLog" v-bind:chat-log="chatLog"></chat-log-view>
					</div>
					<chat-form></chat-form>
				</div>
			</div>
		</main>
		<section class="circle-list-wrap" v-bind:class="{ 'drawer-opened': isDrawerOpened }">
			<circle-list-view></circle-list-view>
		</section>
	</div>
</template>

<script>
import ChatLogView from "@/components/ChatLogView";
import ChatForm from "@/components/ChatForm";
import CircleListView from "@/components/CircleListView";
import VideoView from "@/components/VideoView";
import EventView from "@/components/EventView";

export default {
	name: "VenuePage",
	components: {
		ChatForm,
		ChatLogView,
		CircleListView,
		VideoView,
		EventView
	},
	data() {
		return {
			isDrawerOpened: false,
			activeChatType: 0,
			chatTypes: ["総合", "Q&A", "連絡", "自分宛"]
		}
	},
	computed: {
		getActiveChatLog() {
			switch (this.activeChatType) {
				case 0:
					return this.$store.getters.getChatLogs
				case 1:
					return this.$store.getters.getChatLogsQuestionsAndAnswers
				case 2:
					return this.$store.getters.getChatLogsAdminMessages
				case 3:
					return this.$store.getters.getChatLogsForYou
			}
		}
	},
	methods: {
		setActiveChatType(index) {
			this.activeChatType = index
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
	mounted() {
		const chatLogWrapElement = document.getElementById("chat-log-wrap")
		chatLogWrapElement.addEventListener("scroll", () => {
			if (chatLogWrapElement.scrollTop >= chatLogWrapElement.scrollHeight - chatLogWrapElement.clientHeight) {
				this.$store.commit("clearChatLogWrapScrolledAt")
			} else {
				this.$store.commit("setChatLogWrapScrolledAt")
			}
			if (chatLogWrapElement.scrollTop === 0) {
				this.$store.dispatch("getOldMessages")
			}
		})
		this.$store.dispatch("connectWebSocket")
	}
};
</script>

<style lang="scss" scoped>
.venue-page{
	display: flex;
	flex-direction: column;
	justify-content: stretch;
	color: $text-color;
	background-color: $background-color;
	height: 100%;
	header{
		background-color: $theme-color;
		height: $header-height;
		display: flex;
		align-items: center;
		justify-content: center;
		h1{
			width: fit-content;
			height: 100%;
			padding-bottom: 0.5%;
			flex-grow: 0;
			flex-shrink: 0;
			img{
				height: 100%;
			}
		}
		#hamburger{
			display: block;
			position: fixed;
			top: 0;
			right: 0;
			z-index: 100;
			width: $header-height;
			padding: calc(#{$header-height} / 3) calc(#{$header-height} / 3.5) calc(#{$header-height} / 3.5);
			cursor: pointer;
			box-sizing: border-box;
			span{
				height: 2px;
				background: #FFFFFF;
				display: block;
				margin-bottom: calc(#{$header-height} / 8);
				@include drawerAnimation;
			}
			&.drawer-opened{
				span{
					&:nth-child(1){
						transform: translate(0, calc(#{$header-height} / 7)) rotate(45deg);
					}
					&:nth-child(2){
						transform:translate(calc(-#{$header-height} / 7) ,0);
						opacity:0;
					}
					&:nth-child(3){
						transform: translate(0, calc(-#{$header-height} / 7)) rotate(-45deg);
					}
				}
			}
		}
	}

	.circle-list-wrap{
		position: fixed;
		z-index: 99;
		right: calc(-#{$subcolumn-width} + #{$column-margin-width} - 20px - 30px);
		width: calc(#{$subcolumn-width} - #{$column-margin-width} / 2);
		height: 100%;
		overflow-y: scroll;
		padding-top: $header-height;
		background-color: $theme-color;
		box-shadow: -10px 0 15px 10px rgba(#4D4D4D, 0.7);
		@include drawerAnimation;
		&.drawer-opened{
			right: 0;
		}
	}

	main{
		display: flex;
		height: calc(100% - #{$header-height});
		flex-shrink: 1;
		flex-grow: 1;
		.main-wrap, .side-wrap{
			margin: 2vw $column-margin-width;
		}
		.main-wrap, .side-wrap .chat-wrap{
			background-color: #FFFFFF;
			box-shadow: 5px 5px 5px $shadow-color;
		}

		.main-wrap{
			width: calc(100% - #{$subcolumn-width} - #{$column-tab-width});
			margin-left: $column-tab-width;
			padding: 1em;
			display: flex;
			flex-direction: column;
			justify-content: stretch;
			.video-wrap{
				flex-shrink: 0;
				flex-grow: 0;
			}
			.event-wrap{
				flex-shrink: 1;
				flex-grow: 1;
				overflow-y: scroll;
			}
		}
		.side-wrap{
			width: calc(#{$subcolumn-width} - #{$column-tab-width});
			margin-right: $column-tab-width;
			position: relative;

			.chat-wrap{
				width: 100%;
				height: 100%;
				position: relative;
				z-index: 2;
				display: flex;
				flex-direction: column;
				justify-content: stretch;
				padding-top: 1em;
				.chat-log-wrap{
					height: auto;
					flex-shrink: 1;
					flex-grow: 1;
					overflow-y: scroll;
				}
			}

			.chat-tab-wrap{
				width: calc(#{$column-tab-width});
				position: absolute;
				left: 100%;
				ul{
					padding: 0;
					list-style: none;
					margin-right: 2vw;
					li.chat-tab{
						font-size: 0.9em;
						position: relative;
						z-index: 1;
						cursor: pointer;
						color: $light-button-color;
						background-color: #FFFFFF;
						padding: 0.3em 0.6em;
						margin: 0.6em 0;
						box-shadow: 5px 5px 5px $shadow-color;
						&:first-child{
							margin-top: 0;
						}
						&.active{
							background-color: $theme-color;
							color: #FFFFFF;
							left: -0.5em;
							z-index: 3;
						}
					}
				}
			}

		}
	}
}
</style>
