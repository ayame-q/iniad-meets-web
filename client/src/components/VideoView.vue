<template>
	<div class="video">
		<video class="video-js vjs-theme-forest vjs-16-9" id="video" controls playsinline ref="videoPlayer">
			<source v-bind:src="videoSrc" type="application/x-mpegURL">
		</video>
	</div>
</template>

<script>
import videojs from 'video.js'
import 'video.js/dist/video-js.css'
import axios from "axios";

export default {
	name: "VideoView",
	data() {
		return {
			player: null,
			videoSrc: null,
			options: {}
		}
	},
	mounted() {
		axios.get("/api/v2/status")
		.then((result) => {
			this.videoSrc = result.data.movie_url
			this.$nextTick(() => {
				this.player = videojs(this.$refs.videoPlayer, this.options, () => {
					console.log('onPlayerReady', this);
				})
			})
		})
	},
};
</script>

<style lang="scss">
.vjs-big-play-button {
	background-color: transparent !important;
	background-image: url('../assets/img/play.svg') !important;
	background-size: 25% !important;
	background-repeat: no-repeat !important;
	background-position: center !important;
	top: 50% !important;
	left: 50% !important;
	width: 100% !important;
	height: 100% !important;
	transform: translate(-50%, -50%);
	border: none !important;
	&:hover{
		opacity: 0.8;
	}
	.vjs-icon-placeholder {
		display: none !important;
	}
}
.vjs-control-bar{
	background-color: rgba($theme-color, 0.7) !important;
}
</style>
