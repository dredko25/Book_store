function handleEnterKey(event, itemId) {
    if (event.key === "Enter") {
        event.preventDefault();

        const quantityInput = document.getElementById(`quantity-${itemId}`);
        const quantity = quantityInput.value;

        const formData = new FormData();
        formData.append('quantity', quantity);

        fetch(`/update_quantity/${itemId}`, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            // Перевіряємо, чи є редірект
            if (response.redirected) {
                window.location.href = response.url; // Перенаправляємо сторінку
            } else {
                console.error('Сервер не редіректнув');
                alert('Редірект не відбувся. Спробуйте ще раз.');
            }
        })
        .catch(error => {
            console.error('Помилка:', error);
            alert('Не вдалося оновити кількість товару');
        });
    }
}
