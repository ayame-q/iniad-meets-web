<template>
	<div class="emergency">
		<h2>INIAD meets web 延期に関するお詫びとお知らせ</h2>
		<p>
			INIAD meets webへご来場いただきました皆さま<br>
			<br>
			誠に申し訳ありません。<br>
			システムのトラブルにより、INIAD meets webの開催を<br>
			<b>4/29(木) 18:30〜 (18:00開場), 4/30(金) 14:00〜 (13:30開場)</b>の2回開催と延期させていただきます。<br>
			再三の延期でご迷惑をおかけし大変申し訳ありません。<br>
			誠に勝手ですが、できればご都合のよろしいお時間にまたお越しいただけますと幸いです。<br>
		</p>
		<p class="close" v-on:click="$emit('close')">×</p>
	</div>
</template>

<script>
export default {
	name: "EmergencyMessage",
};
</script>

<style lang="scss" scoped>
.emergency{
	position: relative;
	color: $text-color;
	padding: 1.5em;
	h2{
		margin-bottom: 1em;
	}
	.close{
		position: absolute;
		font-size: 2em;
		top: 0;
		right: 0.3em;
		color: $theme-color;
		cursor: pointer;
	}
}
</style>
