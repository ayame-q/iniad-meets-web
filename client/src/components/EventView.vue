<template>
	<div class="event">
		<div class="next">Webメディア研究会<img src="../assets/img/next.svg" alt="NEXT"></div>
		<event-circle-view v-bind:circle="$store.getters.getCircles[0]"></event-circle-view>
		<!--<event-question-view v-bind:question="questionSample"></event-question-view>-->
		<!--<event-final-view></event-final-view>-->
	</div>
</template>

<script>
import EventCircleView from "@/components/EventCircleView";
import EventQuestionView from "@/components/EventQuestionView";
import EventFinalView from "@/components/EventFinalView";
export default {
	name: "EventView",
	data() {
		return {
			questionSample: {
				"type": 1,
				"text": "問題",
				"selections": [
					{
						"question_uuid": "uuid1",
						"text": "選択肢1"
					},
					{
						"question_uuid": "uuid2",
						"text": "選択肢2"
					},
					{
						"question_uuid": "uuid3",
						"text": "選択肢3"
					},
					{
						"question_uuid": "uuid4",
						"text": "選択肢4"
					}
				]
			}
		}
	},
	components: {
		EventCircleView,
		EventQuestionView,
		EventFinalView
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
