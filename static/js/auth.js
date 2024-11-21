// Функція для оновлення вмісту модального вікна
function updateModalContent(title, formContent) {
    document.getElementById('authModalLabel').textContent = title;
    document.getElementById('authModalBody').innerHTML = formContent;
}

// Вміст форми входу
const loginFormContent = `
    <form action="/login" method="POST" id="loginForm">
        <div class="form-group">
            <label for="loginEmail">Email</label>
            <input type="email" class="form-control" id="loginEmail" name="email" required>
        </div>
        <div class="form-group">
            <label for="loginPassword">Пароль</label>
            <input type="password" class="form-control" id="loginPassword" name="password" required>
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary">Увійти</button>
        </div>
    </form>
    <p class="mt-3 text-center">Ще немає облікового запису? <a href="#" class="toggleForm">Зареєструйтесь</a></p>
`;

// Вміст форми реєстрації
const registerFormContent = `
    <form action="/register" method="POST" id="registerForm">
        <div class="form-group">
            <label for="registerName">Ім'я</label>
            <input type="text" class="form-control" id="registerName" name="name" required>
        </div>
        <div class="form-group">
            <label for="registerEmail">Email</label>
            <input type="email" class="form-control" id="registerEmail" name="email" required>
        </div>
        <div class="form-group">
            <label for="registerPassword">Пароль</label>
            <input type="password" class="form-control" id="registerPassword" name="password" required>
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary">Зареєструватися</button>
        </div>
    </form>
    <p class="mt-3 text-center">Вже є обліковий запис? <a href="#" class="toggleForm">Увійти</a></p>
`;

// Обробник для перемикання між формами
document.getElementById('authModalBody').addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('toggleForm')) {
        const isRegisterForm = e.target.textContent.includes('Зареєструйтесь');
        
        // Оновлюємо вміст модального вікна в залежності від вибраної форми
        if (isRegisterForm) {
            updateModalContent("Реєстрація", registerFormContent);
        } else {
            updateModalContent("Увійти", loginFormContent);
        }
    }
});

// Початковий стан модального вікна - форма входу
updateModalContent("Увійти", loginFormContent);