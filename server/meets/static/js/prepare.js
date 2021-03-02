window.addEventListener( "scroll", function() {

	var headerElement = document.getElementsByTagName( "header" )[0];
	var rect = headerElement.getBoundingClientRect();
	var y = rect.top + window.pageYOffset;
	if (y > 0) {
		headerElement.classList.add('scrolled');
	} else {
		headerElement.classList.remove('scrolled');
	}
} ) ;