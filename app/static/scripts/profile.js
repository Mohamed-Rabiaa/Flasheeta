const API_BASE_URL = 
    ['localhost', '127.0.0.1', '0.0.0.0'].includes(window.location.hostname)
        ? 'http://localhost:5000'
        : 'https://flasheeta.pythonanywhere.com';

$(document).ready(function() {
    $('.logout').on('click', function() {
	window.location.href = `${API_BASE_URL}/auth/logout`;
    });
});


