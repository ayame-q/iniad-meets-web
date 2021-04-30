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
			videoSrc: null,
			options: {}
		}
	},
	mounted() {
		axios.get("/api/v2/status")
		.then((result) => {
			this.videoSrc = result.data.movie_url
			this.$nextTick(() => {
				const player = videojs(this.$refs.videoPlayer, this.options, () => {
					player.on("error", (err) => {
						console.error("Movie load Error!")
					})
					player.on("play", (arg) => {
						if (this.$store.getters.getStatus.status === 2){
							this.$store.commit("clearPastEventsAndTimeout")
							const player = this.$store.getters.getPlayer
							this.$store.dispatch("updateMovieTime", player.currentTime())
						}
					})
					/*
					player.on("seeked", (arg) => {
						if (this.$store.getters.getStatus.status === 2){
							this.$store.commit("clearPastEventsAndTimeout")
							const player = this.$store.getters.getPlayer
							this.$store.dispatch("updateMovieTime", player.currentTime())
						}
					})
					*/
					player.on("pause", (arg) => {
						if (this.$store.getters.getStatus.status === 2) {
							this.$store.commit("clearTimeoutsForPastEvent")
						}
					})
				})
				this.$store.commit("setPlayer", player)
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
