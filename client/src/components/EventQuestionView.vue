<template>
	<div class="event-question">
		<ul v-bind:class="{
			'two-selections': question.selections.length === 2,
			'four-selections': question.selections.length === 4
		}">
			<li v-for="selection of question.selections"><button>{{ selection.text }}</button></li>
		</ul>
	</div>
</template>

<script>
export default {
	name: "EventQuestionView",
	props: {
		question: Object
	}
};
</script>

<style lang="scss" scoped>
.event-question{
	height: 100%;
	margin: 0 -1em;
	padding-top: 2.8em;
	font-size: 0.7em;
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
