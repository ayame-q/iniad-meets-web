<template>
	<div class="event-circle">
		<h2>
			<span>{{ circle.name }}</span>
			<span class="pamphlet" v-on:click="openMaterial(circle.pamphlet_url)">
				<img src="../assets/img/pamphlet.svg" alt="資料を見る">
			</span>
		</h2>
		<p class="comment">
			{{ circle.comment }}
		</p>
		<div class="footer">
			<ul class="links">
				<li v-if="circle.twitter_sn"><a v-bind:href="`https://twitter.com/${circle.twitter_sn}`" target="_blank"><img src="../assets/img/twitter.svg" alt="Twitter"></a></li>
				<li v-if="circle.instagram_id"><a v-bind:href="`https://www.instagram.com/${circle.instagram_id}`" target="_blank"><img src="../assets/img/instagram.svg" alt="Instagram"></a></li>
				<li v-if="circle.website_url"><a v-bind:href="circle.website_url" target="_blank"><img src="../assets/img/website.svg" alt="公式サイト"></a></li>
			</ul>
			<entry-button v-bind:circle="circle"></entry-button>
		</div>
	</div>
</template>

<script>
import openMaterial from "@/mixins/openMaterial";
import EntryButton from "@/components/EntryButton";

export default {
	name: "EventCircleView",
	props: {
		circle: Object
	},
	components: {
		EntryButton
	},
	mixins: [openMaterial]
};
</script>

<style lang="scss" scoped>
.event-circle{
	display: flex;
	flex-direction: column;
	@media (max-aspect-ratio: 3/1.8){
		justify-content: flex-start;
	}
	@media (min-aspect-ratio: 3/1.8){
		justify-content: stretch;
	}
	height: 100%;
	h2{
		margin-top: 0.1em;
		font-size: 1.15em;
		font-weight: normal;
		display: flex;
		align-items: flex-end;
		span{
			display: block;
			img{
				display: block;
				height: 0.75em;
				margin-left: 0.3em;
				margin-bottom: 0.3em;
			}
		}
	}
	.comment{
		font-size: 0.7em;
		white-space: pre-line;
		@media (min-aspect-ratio: 9/5){
			flex-grow: 1;
			display: flex;
			align-items: center;
		}
		margin-top: 0.3em;
		margin-bottom: 0.05em;
	}
	.footer{
		display: flex;
		justify-content: space-between;
		align-items: flex-end;
		ul.links{
			display: flex;
			padding: 0;
			list-style: none;
			li{
				margin-right: 0.3em;
				img{
					height: 1.5em;
					display: block;
				}
			}
		}
		p.entry-button{
			width: fit-content;
			button{
				font-size: 0.85em;
				color: #FFFFFF;
				background-color: $sub-color;
				border-radius: 1.5em;
				padding: 0.5em 1.2em;
			}
		}
	}
}
</style>
