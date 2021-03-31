<template>
	<div id="app">
		<router-view/>
	</div>
</template>

<script>
export default {
	name: "App",
	metaInfo: {
		title: "",
		titleTemplate(input) {
			return input ? `${input} - INIAD meets Web` : "INIAD meets Web"
		},
	},
};
</script>

<style lang="scss">
html {
	font-family: "Yu Gothic", "游ゴシック", YuGothic, "游ゴシック体", "ヒラギノ角ゴ Pro W3", "Hiragino Kaku Gothic Pro W3", "メイリオ", sans-serif;
	font-size: 1.5vw;
	word-spacing: 1px;
	-ms-text-size-adjust: 100%;
	-webkit-text-size-adjust: 100%;
	-moz-osx-font-smoothing: grayscale;
	-webkit-font-smoothing: antialiased;
	box-sizing: border-box;
}

*,
*::before,
*::after {
	box-sizing: border-box;
	margin: 0;
}
</style>
