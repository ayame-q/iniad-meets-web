<template>
	<div>
		<p>
			<a v-bind:href="event.pr_url" target="_blank" class="pr-button">
				{{ event.pr_text }}
			</a>
		</p>
	</div>
</template>

<script>
export default {
	name: "EventPrUrlView",
	props: {
		event: Object
	}
}
</script>

<style lang="scss" scoped>
div{
	display: flex;
	height: 100%;
	padding-top: 2em;
	justify-content: center;
	align-items: center;
	.pr-button{
		display: flex;
		align-items: center;
		border: $light-button-color solid 3px;
		width: fit-content;
		font-size: 1.2em;
		padding: 0.8em 1.5em;
		border-radius: 1em;
		color: $text-color;
		text-decoration: none;
		font-weight: bold;
		&:hover{
			text-decoration: underline;
		}
	}
}
</style>
