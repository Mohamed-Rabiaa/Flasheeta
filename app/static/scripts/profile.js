$(document).ready(function() {
    $('.logout').on('click', function() {
	window.location.href = 'https://flasheeta.pythonanywhere.com/auth/logout';
    });
});


