<template>
	<article class="teaser">
		<div class="info">
			<p>INIADのサークル情報満載！<br>リアルタイムなWeb新歓イベント</p>
			<h1><img src="@/assets/img/logo.svg" alt="INIAD meets web"></h1>
			<p class="datetime"><time>
				<span class="date" v-if="dayjs() < dayjs('2021/4/29 19:00:00')">2021.4.29 Thur.</span>
				<span class="time" v-if="dayjs() < dayjs('2021/4/29 19:00:00')">18:00 Open, 18:30 Start</span>
				<span class="date" v-if="dayjs() >= dayjs('2021/4/29 19:00:00')">2021.4.30 Fri.</span>
				<span class="time" v-if="dayjs() >= dayjs('2021/4/29 19:00:00')">13:30 Open, 14:00 Start</span>
			</time></p>
			<ul class="sns-share">
				<li>
					<a href="https://twitter.com/intent/tweet?url=https://meets.iniad.net&text=INIADのサークル情報満載！「INIAD meets web」2021.4.29 18:00開場 &hashtags=INIADmeetsweb&related=iniad_webmedia&via=iniad_webmedia">
						<font-awesome-icon v-bind:icon="['fab', 'twitter']"></font-awesome-icon>
						ツイート
					</a>
				</li>
				<li class="sns-share-line">
					<a href="https://line.me/R/msg/text/?INIADのサークル情報満載！「INIAD meets web」2021.4.29 18:00開場 https://meets.iniad.net" class="sns-share-line">
						<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 87.38 83.26"><path class="cls-1" d="M87.38,35.46C87.38,15.91,67.78,0,43.69,0S0,15.91,0,35.46c0,17.52,15.54,32.2,36.54,35,1.42.3,3.36.93,3.85,2.15a8.94,8.94,0,0,1,.14,4l-.62,3.74c-.19,1.11-.88,4.32,3.78,2.36S68.85,67.82,78,57.27h0C84.35,50.33,87.38,43.28,87.38,35.46ZM28.28,45.89a.85.85,0,0,1-.85.85H15.18a.89.89,0,0,1-.59-.23h0v0a.83.83,0,0,1-.24-.59h0v-19a.85.85,0,0,1,.85-.85h3.07a.85.85,0,0,1,.85.85V42h8.33a.85.85,0,0,1,.85.85Zm7.38,0a.85.85,0,0,1-.85.84H31.75a.85.85,0,0,1-.85-.84v-19a.85.85,0,0,1,.85-.85h3.06a.85.85,0,0,1,.85.85Zm21.1,0a.85.85,0,0,1-.85.84H52.84l-.21,0h0l-.06,0h-.06l0,0,0,0-.05,0h0a1,1,0,0,1-.21-.21l-8.74-11.8V45.9a.85.85,0,0,1-.85.84H39.5a.86.86,0,0,1-.86-.84v-19A.86.86,0,0,1,39.5,26h3.29l.05,0h0l.05,0h0l0,0h0l0,0,0,0,.05,0h0l.06.05h0l.07.09L52,38.17V26.86a.85.85,0,0,1,.85-.85h3.07a.85.85,0,0,1,.85.85Zm16.92-16a.86.86,0,0,1-.85.86H64.5V34h8.33a.85.85,0,0,1,.85.85v3.07a.85.85,0,0,1-.85.85H64.5V42h8.33a.85.85,0,0,1,.85.85v3.06a.85.85,0,0,1-.85.85H60.59a.87.87,0,0,1-.59-.23h0v0a.83.83,0,0,1-.24-.58h0v-19h0a.87.87,0,0,1,.23-.59h0a.83.83,0,0,1,.59-.24H72.83a.85.85,0,0,1,.85.85Z"/></svg>
						LINEで送る
					</a>
				</li>
			</ul>
		</div>
		<p class="times-pr"><a href="https://iniad-wm.com/" target="_blank">INIAD情報満載のオンライン情報誌<br>「INIAD Times」もぜひご覧ください！</a></p>
	</article>
</template>

<script>
import EmergencyMessage from "@/components/EmergencyMessage";
import dayjs from "dayjs";

export default {
	name: "TeaserPage",
	mounted() {
		if (dayjs() < dayjs("2021/4/29 18:00:00")) {
			this.$modal.show(
				EmergencyMessage,
				{},
				{
					width: "70%",
					height: "70%",
					draggable: true,
				}
			)
		}
	}
};
</script>

<style lang="scss">
html{
	width: 100%;
	height: 100%;
}
#app{
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
		ul.sns-share{
			list-style: none;
			padding: 0;
			display: flex;
			justify-content: flex-end;
			padding-right: 1%;
			li{
				&.sns-share-line{
					svg{
						display: inline;
						width: 1em;
						height: 1em;
						margin-bottom: -0.1em;
					}
				}
				margin: 0 0.2em;
				a{
					color: #36B0CC;
					text-decoration: none;
					border: #FFFFFF solid 1px;
					background-color: #FFFFFF;
					font-size: 0.6em;
					padding: 5px;
					border-radius: 5px;
					.cls-1{
						fill:#36B0CC;
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
			&:hover{
				text-decoration: underline;
			}
		}
	}
}
.datetime{
	color: #FFFFFF;
}
</style>
