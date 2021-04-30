<template>
	<div class="start">
		<div class="text">
			<p>
				申し訳ありません。サーバーから切断されました。<br>
				しばらくしてからリロードしてみてください。
			</p>
		</div>
	</div>
</template>

<script>
export default {
	name: "EventConnectionErrorView",
};
</script>

<style lang="scss" scoped>
.start{
	margin-top: 3em;
	.text p{
		font-size: 1.2em;
	}
}
</style>
