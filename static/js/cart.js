// function handleEnterKey(event, itemId) {
//     if (event.key === "Enter") {
//         event.preventDefault();

//         const quantityInput = document.getElementById(`quantity-${itemId}`);
//         const quantity = quantityInput.value;

//         const formData = new FormData();
//         formData.append('quantity', quantity);

//         fetch(`/update_quantity/${itemId}`, {
//             method: 'POST',
//             body: formData
//         })
//         .then(response => {
//             return response.json();
//         })
//         .then(data => {
//             if (data.success) {
//                 document.getElementById('total-sum').innerText = `${data.total} грн`;
//             } else {
//                 alert(data.message || 'Не вдалося оновити товар. Спробуйте ще раз.');
//             }
//         })
//         .catch(error => {
//             console.error('Помилка:', error);
//             alert('Не вдалося оновити кількість товару');
//         });
//     }
// }
function handleEnterKey(event, itemId) {
    if (event.key === "Enter") {
        event.preventDefault();

        const quantityInput = document.getElementById(`quantity-${itemId}`);
        const quantity = quantityInput.value;

        console.log("Item ID:", itemId);
        console.log("Entered Quantity:", quantity);

        const formData = new FormData();
        formData.append('quantity', quantity);

        fetch(`/update_quantity/${itemId}`, {
            method: 'POST',
            body: formData
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            console.log("Response from server:", data);
            if (data.success) {
                document.getElementById('total-sum').innerText = `${data.total} грн`;
            } else {
                alert(data.message || 'Не вдалося оновити товар. Спробуйте ще раз.');
            }
        })
        .catch(error => {
            console.error('Error occurred in handleEnterKey:', error);
            alert('Не вдалося оновити кількість товару');
        });
    }
}
