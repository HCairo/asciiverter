document.addEventListener('DOMContentLoaded', function() {
    const form = document.querySelector('form');
    const loadingText = document.querySelector('.loading');

    form.addEventListener('submit', function() {
        loadingText.style.display = 'block';
    });
});