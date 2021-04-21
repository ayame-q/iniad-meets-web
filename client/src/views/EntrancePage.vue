<template>
	<div class="entrance-page">
		<p class="entry-wrap"><a href="/auth/google/login/" class="entry"><img src="@/assets/img/entrance_entry_text.svg" alt="入場"></a></p>
	</div>
</template>

<script>
export default {
	name: "EntrancePage",
};
</script>

<style lang="scss">
html{
	width: 100%;
	height: 100%;
	#app{
		display: flex;
		justify-content: center;
		align-items: center;
	}
}
</style>

<style lang="scss" scoped>
.entrance-page{
	font-size: min(1.8vw, calc(1.8vh / 9 * 16));
	width: min(100vw, calc(100vh / 9 * 16));
	height: min(calc(100vw / 16 * 9), 100vh);
	background-image: url("../assets/img/entrance_background.svg");
	background-position: center;
	background-size: contain;
	background-repeat: no-repeat;
	display: flex;
	justify-content: flex-start;
	align-items: center;
	p.entry-wrap{
		width: 52.5%;
		display: flex;
		align-items: center;
		justify-content: center;
		font-size: min(3vw, calc(3vh / 9 * 16));
		a.entry{
			display: block;
			text-decoration: none;
			width: fit-content;
			background-color: $theme-color;
			padding: 0.5em 1.5em;
			color: #FFFFFF;
			border-radius: 0.25em;
			border-bottom: #2D90A0 0.2em solid;
			img{
				height: 1em;
				display: block;
			}
		}
	}
}
</style>
