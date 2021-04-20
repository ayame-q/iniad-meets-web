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

html, body, #app{
	width: 100%;
	height: 100%;
}

*,
*::before,
*::after {
	box-sizing: border-box;
	margin: 0;
}

input, select, textarea, button{
	display: block;
	font-family: inherit;
	font-size: 1.1em;
	padding: 0.4em 0.8em;
	box-sizing: border-box;
	-webkit-appearance: none;
	-moz-appearance: none;
	appearance: none;
	border: none;
	width: calc(100%);
	background-color: white;
	color: $text-color;
	&::placeholder{
		color: $placeholder-color;
	}

	&:focus{
		outline: none;
	}
	&[type=submit]{
		cursor: pointer;
	}
	&:disabled{
		background-color: lightgray;
	}
	&[type=checkbox]{
		cursor: pointer;
		display: inline-block;
		position: relative;
		width: 0.6em;
		height: 0.6em;
		margin-right: 0.5em;
		padding: 0;
		&:checked{
			&::before{
				content: "";
				position: absolute;
				bottom: 0.25em;
				left: 0;
				height: 0.5em;
				width: 0.8em;
				border-left: $light-button-color 3px solid;
				border-bottom: $light-button-color 3px solid;
				transform: rotate(-45deg);
			}
		}
	}
}
button{
	cursor: pointer;
}

</style>
