<template>
	<div class="final">
		<div class="quiz-result">
			<p>クイズ {{ quizCount }}問中 <span style="font-size: 1.6em; margin-left: 0.2em">{{ correctCount }}</span> 問正解！おめでとうございます！！！</p>
			<ul class="quiz-link">
				<li><a v-bind:href="`https://twitter.com/intent/tweet?url=https://meets.iniad.net/share/${$store.getters.getMyUser.uuid}&text=INIAD meets webのクイズに 回答した${quizCount}問中${correctCount}問正解しました！%20&hashtags=INIADmeetsweb&related=iniad_webmedia&via=iniad_webmedia`" target="_blank"><img src="@/assets/img/twitter_white.svg" alt="Twitterで">結果をシェア</a></li>
				<li><a href="/img/wallpaper.png" target="_blank">景品を受け取る</a></li>
			</ul>
		</div>
		<div class="final-buttons">
			<ul>
				<li><a v-bind:href="finalQuestionnaireUrl" target="_blank">参加者アンケートに回答</a></li>
				<li>
					<a href="https://iniad-wm.com/" target="_blank" class="times-button">
						<img src="@/assets/img/times-icon-white.svg" alt="Times icon">INIAD Timesを見に行く
					</a>
				</li>
			</ul>
		</div>
	</div>
</template>

<script>
export default {
	name: "EventFinalView",
	computed: {
		quizResponses() {
			return this.$store.getters.getQuestionResponses.filter((item) => {
				return item.question_type === 1
			})
		},
		correctResponses() {
			return this.$store.getters.getQuestionResponses.filter((item) => {
				return item.question_type === 1 && item.is_correct
			})
		},
		quizCount() {
			return this.quizResponses.length
		},
		correctCount() {
			return this.correctResponses.length
		},
		finalQuestionnaireUrl() {
			return process.env.VUE_APP_FINAL_QUESTIONNAIRE_URL
		}
	}
};
</script>

<style lang="scss" scoped>
.final{
	display: flex;
	flex-direction: column;
	justify-content: stretch;
	height: 100%;
	.quiz-result{
		font-size: 1em;
		flex-grow: 0;
		ul.quiz-link{
			padding: 0;
			list-style: none;
			display: flex;
			justify-content: flex-end;
			li{
				&:not(:last-child){
					margin-right: 0.5em;
				}
				a{
					display: flex;
					align-items: center;
					background-color: $light-button-color;
					font-size: 0.65em;
					padding: 0.3em 1em;
					border-radius: 1em;
					color: #FFFFFF;
					text-decoration: none;
					font-weight: bold;
					&:hover{
						text-decoration: underline;
					}
					img{
						height: 0.8em;
						margin-right: 0.3em;
						display: block;
					}
				}
			}
		}
	}
	.final-buttons{
		flex-grow: 1;
		ul{
			height: 100%;
			list-style: none;
			padding: 0;
			padding-top: 1em;
			display: flex;
			li{
				height: 100%;
				max-height: 5em;
				width: 49%;
				&:not(:last-child){
					margin-right: 2%;
				}
				a{
					height: 100%;
					display: flex;
					justify-content: center;
					align-items: center;
					font-size: 0.78em;
					padding: 0.3em 1em;
					border-radius: 1em;
					color: #FFFFFF;
					text-decoration: none;
					background-color: $light-button-color;
					&:hover{
						text-decoration: underline;
					}
					&:not(:last-child){
						margin-right: 0.5em;
					}
					&.times-button{
						background-color: #F08840;
						img{
							height: 1em;
							margin-right: 0.3em;
							display: block;
						}
					}
				}
			}
		}
	}
}
</style>
