<template>
	<div class="event-question">
		<ul v-bind:class="{
			'two-selections': question.selections.length === 2,
			'four-selections': question.selections.length === 4
		}">
			<li v-for="selection of question.selections">
				<button v-bind:class="{
					'result-questionnaire': selection.percentage,
					'selected': isSelected(selection)
				}" v-bind:disabled="selection.percentage" v-on:click="$store.dispatch('sendQuestionResponse', selection.uuid)">
					<span class="text">{{ selection.text }}</span>
					<span class="result-percentage" v-if="selection.percentage">{{ selection.percentage }}%</span>
				</button>
			</li>
		</ul>
		<p v-if="question.correct_uuid" class="result-quiz">
			<img src="../assets/img/correct.svg" v-if="isQuizCorrect()">
			<img src="../assets/img/wrong.svg" v-else>
		</p>
	</div>
</template>

<script>
export default {
	name: "EventQuestionView",
	props: {
		question: Object
	},
	methods: {
		isSelected(selection) {
			const responses = this.$store.getters.getQuestionResponses
			const result = responses.find((item) => {
				return item.selection_uuid === selection.uuid
			})
			return result
		},
		isQuizCorrect() {
			const responses = this.$store.getters.getQuestionResponses
			const original = responses.find((item) => {
				return item.question_uuid === this.question.uuid
			})
			if (original.is_correct) {
				return original.is_correct
			}
			const result = (original.selection_uuid === this.question.correct_uuid)
			original["is_correct"] = result
			this.$store.commit("addQuestionResponse", original)
			return result
		}
	}
};
</script>

<style lang="scss" scoped>
.event-question{
	height: 100%;
	margin: 0 -1em;
	padding-top: 2.8em;
	font-size: 0.7em;
	position: relative;
	.result-quiz{
		position: absolute;
		width: 100%;
		height: 100%;
		display: flex;
		justify-content: center;
		top: 0;
		left: 0;
		z-index: 5;
		img{
			height: 98%;
		}
	}
	ul{
		padding: 0;
		list-style: none;
		display: flex;
		height: 100%;
		button{
			border: $light-button-color solid 3px;
			border-radius: 1em;
			color: $text-color;
			width: 100%;
			height: 100%;
			font-weight: bold;
			&:hover{
				text-decoration: underline;
			}
			&:disabled{
				background-color: transparent;
				&:hover{
					text-decoration: none;
				}
			}
			&.selected{
				background-color: $theme-color;
				border-color: $theme-color;
				color: #FFFFFF;
			}
			&.result-questionnaire{
				display: flex;
				justify-content: center;
				position: relative;
				.text{
					font-size: 0.8em;
					position: absolute;
					top: 0;
					left: 0.5em;
				}
				.result-percentage{
					justify-self: center;
					align-self: center;
				}
			}
		}

		&.two-selections{
			flex-direction: column;
			justify-content: stretch;
			li{
				padding: 0.5em;
				flex-shrink: 1;
				flex-grow: 1;
			}
		}
		&.four-selections{
			flex-wrap: wrap;
			li{
				width: 50%;
				height: 50%;
				padding: 0.2em 0.5em;
			}
		}
	}
}
</style>
