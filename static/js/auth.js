function updateModalContent(title, formContent) {
    document.getElementById('authModalLabel').textContent = title;
    document.getElementById('authModalBody').innerHTML = formContent;
}

const loginFormContent = `
    <form action="/login" method="POST" id="loginForm">
        <div class="form-group">
            <label for="loginEmail" class="small">Email</label>
            <input type="email" class="form-control" id="loginEmail" name="email" required>
        </div>
        <div class="form-group">
            <label for="loginPassword" class="small">Пароль</label>
            <input type="password" class="form-control" id="loginPassword" name="password" required>
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary">Увійти</button>
        </div>
    </form>
    <p class="mt-3 text-center">Ще немає облікового запису? <a href="#" class="toggleForm">Зареєструйтесь</a></p>
`;

const registerFormContent = `
    <form action="/register" method="POST" id="registerForm">
        <div class="form-group">
            <label for="registerFirstName" class="small">Ім'я</label>
            <input type="text" class="form-control" id="registerFirstName" name="first_name" placeholder="Наприклад: Іван" required>
        </div>
        <div class="form-group">
            <label for="registerLastName" class="small">Прізвище</label>
            <input type="text" class="form-control" id="registerLastName" name="last_name" placeholder="Наприклад: Петренко" required>
        </div>
        <div class="form-group">
            <label for="registerPhone" class="small">Номер телефону</label>
            <input type="tel" class="form-control" id="registerPhone" name="phone" placeholder="Наприклад: +380501234567" required>
        </div>
        <div class="form-group">
            <label for="registerAddress" class="small">Адреса доставки</label>
            <input type="text" class="form-control" id="registerAddress" name="delivery_address" placeholder="Наприклад: шосе Харківське, 164, Київ, 02091" required>
        </div>
        <div class="form-group">
            <label for="registerEmail" class="small">Email</label>
            <input type="email" class="form-control" id="registerEmail" name="email" placeholder="Наприклад: example@mail.com" required>
        </div>
        <div class="form-group">
            <label for="registerPassword" class="small">Пароль</label>
            <input type="password" class="form-control" id="registerPassword" name="password" placeholder="Введіть пароль" required>
        </div>
        <div class="text-center">
            <button type="submit" class="btn btn-primary">Зареєструватися</button>
        </div>
    </form>
    <p class="mt-3 text-center">Вже є обліковий запис? <a href="#" class="toggleForm">Увійти</a></p>
`;

document.getElementById('authModalBody').addEventListener('click', function (e) {
    if (e.target && e.target.classList.contains('toggleForm')) {
        const isRegisterForm = e.target.textContent.includes('Зареєструйтесь');

        if (isRegisterForm) {
            updateModalContent("Реєстрація", registerFormContent);
        } else {
            updateModalContent("Увійти", loginFormContent);
        }
    }
});

updateModalContent("Увійти", loginFormContent);