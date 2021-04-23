<template>
	<section class="circle-list-circle" v-bind:class="{'detail-open': isDetailOpen}">
		<div class="about-box" v-on:click="isDetailOpen=!isDetailOpen">
			<div class="number">
				<p>{{ index }}</p>
			</div>
			<div class="thumbnail">
				<img v-bind:src="circle.thumbnail_url" v-bind:alt="circle.name">
			</div>
			<div class="info">
				{{ circle.name }}
			</div>
		</div>
		<div class="detail-box" v-bind:class="{'detail-open': isDetailOpen}">
			<div>
				<p class="pamphlet" v-on:click="openMaterial(circle.pamphlet_url)"><img src="../assets/img/pamphlet.svg" alt="資料">資料を見る</p>
				<p class="comment">
					{{ circle.comment }}
				</p>
				<div class="action-box">
					<ul>
						<li v-if="circle.twitter_sn"><a v-bind:href="`https://twitter.com/${circle.twitter_sn}`" target="_blank"><img src="../assets/img/twitter.svg" alt="Twitter"></a></li>
						<li v-if="circle.instagram_id"><a v-bind:href="`https://www.instagram.com/${circle.instagram_id}`" target="_blank"><img src="../assets/img/instagram.svg" alt="Instagram"></a></li>
						<li v-if="circle.website_url"><a v-bind:href="circle.website_url" target="_blank"><img src="../assets/img/website.svg" alt="公式サイト"></a></li>
					</ul>
					<entry-button class="entry-button" v-bind:circle="this.circle"></entry-button>
				</div>
			</div>
		</div>
	</section>
</template>

<script>
import openMaterial from "@/mixins/openMaterial";
import EntryButton from "@/components/EntryButton";

export default {
	name: "CircleListCircleView",
	props: {
		circle: Object,
		index: Number,
	},
	data() {
		return {
			isDetailOpen: false,
		}
	},
	components: {
		EntryButton
	},
	mixins: [openMaterial]
};
</script>

<style lang="scss" scoped>
$number-width: 3vw;
$thumbnail-width: 30%;
$arrow-width: 1vw;
.circle-list-circle{
	color: #FFFFFF;
	padding-left: 2em;
	padding-right: 2em;
	width: 100%;

	&.detail-open{
		background-color: rgba(#FFFFFF, 0.28);
		padding-bottom: 1.2em;
	}

	.about-box{
		display: flex;
		align-items: center;
		padding: 1em 0;
		padding-left: 0.1vw;
		cursor: pointer;

		.number{
			text-align: right;
			padding-right: 1vw;
			width: $number-width;
			font-size: 1.3em;
			flex-shrink: 0;
			flex-grow: 0;
		}
		.thumbnail{
			width: $thumbnail-width;
			flex-shrink: 0;
			flex-grow: 0;
			img{
				width: 100%;
			}
		}
		.info{
			margin: 0 1em;
			flex-shrink: 1;
			flex-grow: 1;
		}
	}
	.detail-box{
		background-color: #FFFFFF;
		color: $text-color;
		max-height: 0;
		overflow: hidden;
		opacity: 0;
		transition: max-height 0.5s, opacity 0.8s, background-color 0.8s;
		margin-left: calc(0.5vw + #{$number-width});
		margin-right: $arrow-width;

		&.detail-open{
			max-height: 100vh;
			opacity: 1;
		}
		> div{
			padding: 1em 2em;
		}

		.pamphlet{
			color: $sub-color;
			cursor: pointer;
			display: flex;
			align-items: flex-end;
			img{
				height: 2.5em;
				margin-right: 0.5em;
				display: block;
			}
		}
		.comment{
			white-space: pre-line;
			padding: 1.8em 0.3em;
			font-size: 0.95em;
		}
		.action-box{
			display: flex;
			justify-content: space-between;
			align-items: flex-end;
			ul{
				align-items: center;
				list-style: none;
				padding: 0;
				display: flex;
				li{
					margin-right: 0.4em;
					img{
						display: block;
						height: 1.8em;
					}
				}
			}
			.entry-button::v-deep button{
				font-size: 0.9em;
				border-radius: 1em;
			}
		}
	}
}
</style>
