<template>
	<div class="event" v-bind:class="{'blink': (event && event.type==='tutorial_info_start')}">
		<div class="next" v-if="(!event || event.type!=='final_start') && nextCircle">{{ nextCircle.name }}<img src="../assets/img/next.svg" alt="NEXT"></div>
		<event-circle-view v-bind:circle="circle" v-if="event && event.type==='circle_start'"></event-circle-view>
		<event-question-view v-bind:question="event.question" v-if="event && ( event.type === 'question_start' || event.type === 'question_result')"></event-question-view>
		<event-final-view v-if="event && event.type==='final_start'"></event-final-view>
		<event-tutorial-view v-if="event && event.type==='tutorial_info_start'"></event-tutorial-view>
		<event-pr-url-view v-bind:event="event" v-if="event && event.type==='pr_url_start'"></event-pr-url-view>
		<event-hash-tag-view v-if="event && event.type==='tutorial_hashtag_start'"></event-hash-tag-view>
		<button v-on:click="$store.dispatch('sendStart')" v-if="$store.getters.getMyUser.is_admin">スタート</button>
	</div>
</template>

<script>
import EventCircleView from "@/components/EventCircleView";
import EventQuestionView from "@/components/EventQuestionView";
import EventFinalView from "@/components/EventFinalView";
import EventTutorialView from "@/components/EventTutorialView";
import EventPrUrlView from "@/components/EventPrUrlView";
import EventHashTagView from "@/components/EventHashTagView";
export default {
	name: "EventView",
	computed: {
		event() {
			return this.$store.getters.getEvent
		},
		circle() {
			return this.$store.getters.getNowCircle
		},
		nextCircle() {
			return this.$store.getters.getNextCircle
		}
	},
	components: {
		EventCircleView,
		EventQuestionView,
		EventFinalView,
		EventTutorialView,
		EventPrUrlView,
		EventHashTagView
	}
};
</script>

<style lang="scss" scoped>
.event{
	padding: 0.2em 0.5em;
	height: 100%;
	position: relative;
	.next{
		position: absolute;
		top: 1em;
		right: 0;
		background-color: $light-button-color;
		color: #FFFFFF;
		font-size: 0.6em;
		font-weight: bold;
		display: flex;
		align-items: center;
		padding: 0.2em 0.5em;
		img{
			display: block;
			margin-left: 0.5em;
			height: 0.8em;
		}
	}
}
</style>
