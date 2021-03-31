<template>
	<article class="teaser">
		<div class="info">
			<p>INIADのサークル情報満載！<br>リアルタイムなWeb新歓イベント</p>
			<h1><img src="@/assets/img/logo.svg" alt="INIAD meets web"></h1>
			<p class="datetime"><time>
				<span class="date">2021.4.21 Wed.</span>
				<span class="time">18:00 Open, 18:30 Start</span>
			</time></p>
		</div>
		<p class="times-pr"><a href="https://iniad-wm.com/" target="_blank">INIAD情報満載のオンライン情報誌<br>「INIAD Times」もぜひご覧ください！</a></p>
	</article>
</template>

<script>
export default {
	name: "TeaserPage",
};
</script>

<style lang="scss">
html{
	width: 100%;
	height: 100%;
	display: flex;
	justify-content: center;
	align-items: center;
}
.teaser{
	text-align: right;
	font-size: min(1.8vw, calc(1.8vh / 9 * 16));
	width: min(100vw, calc(100vh / 9 * 16));
	height: min(calc(100vw / 16 * 9), 100vh);
	background-image: url("../assets/img/teaser-background.png");
	background-size: contain;
	display: flex;
	flex-direction: column;
	justify-content: stretch;
	.info{
		flex-shrink: 1;
		flex-grow: 1;
		display: flex;
		flex-direction: column;
		justify-content: center;
		padding: 2%;
		h1{
			img{
				width: 50%;
			}
		}
		p{
			padding: 0 1.8%;
			&.datetime{
				padding: 0.5% 1.8%;
				span{
					display: block;
					&.date{
						font-size: 2.45em;
					}
					&.time{
						font-size: 1.2em;
						margin-top: -0.5em;
					}
				}
			}
		}
	}
	.times-pr{
		height: fit-content;
		flex-shrink: 0;
		flex-grow: 0;
		padding: 2% 4%;
		font-size: 0.8em;
		a{
			color: #222222;
			text-decoration: none;
		}
	}
}
.datetime{
	color: #FFFFFF;
}
</style>
