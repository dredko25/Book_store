document.getElementById('publisher').addEventListener('change', function () {
    const customField = document.getElementById('custom-publisher');
    if (this.value === 'custom') {
        customField.classList.remove('d-none');
        customField.required = true;
    } else {
        customField.classList.add('d-none');
        customField.required = false;
    }
});

document.getElementById('genre').addEventListener('change', function () {
    const customField = document.getElementById('custom-genre');
    if (this.value === 'custom') {
        customField.classList.remove('d-none');
        customField.required = true;
    } else {
        customField.classList.add('d-none');
        customField.required = false;
    }
});