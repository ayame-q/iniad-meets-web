<template>
	<div class="entrance-page">
		<p class="entry-wrap"><a v-on:click="enter" class="entry"><img src="@/assets/img/entrance_entry_text.svg" alt="入場"></a></p>
		<div class="smp-notify">
			<p>
				<b>スマートフォンでの参加は非推奨です。</b><br>
				パソコンまたはタブレットでの参加をオススメします。
				<small style="display: block">(スマートフォンで参加する場合、横画面でご覧いただくと多少マシに表示されるかと思います。)</small>
			</p>
		</div>
	</div>
</template>

<script>
import dayjs from "dayjs";

export default {
	name: "EntrancePage",
	methods: {
		enter() {
			if (this.$route.query.circle) {
				this.$cookies.set("start-circle", this.$route.query.circle, 30)
			}
			window.location.href = "/auth/google/login/"
		}
	}
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
			cursor: pointer;
			&:active{
				margin-top: calc(0.2em - 3px);
				border-bottom-width: 3px;
			}
			img{
				height: 1em;
				display: block;
			}
		}
	}
	.smp-notify{
		display: none;
		@include media(small){
			font-size: 18px;
			display: block;
			position: fixed;
			left: 0;
			bottom: 0;
			width: 100%;
		}
	}
}
</style>
