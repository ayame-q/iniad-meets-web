<template>
	<div>
		<p>
			<a href="https://twitter.com/intent/tweet?hashtags=INIADmeetsweb" target="_blank" class="hasttag">
				#INIADmeetsweb
			</a>
		</p>
	</div>
</template>

<script>
export default {
	name: "EventHashTagView",
};
</script>

<style lang="scss" scoped>
div{
	display: flex;
	height: 100%;
	padding-top: 2em;
	justify-content: center;
	align-items: center;
	.hasttag{
		display: flex;
		align-items: center;
		width: fit-content;
		font-size: 1.5em;
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
