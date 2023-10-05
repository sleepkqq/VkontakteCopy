document.addEventListener('DOMContentLoaded', function () {

    const registerForm = document.querySelector('#registerForm');
    const usernameInput = document.querySelector('#usernameRegister');
    const emailInput = document.querySelector('#emailRegister');
    const passwordInput = document.querySelector('#passwordRegister');

    document.querySelector('#toast-container');
    registerForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const username = usernameInput.value;
        const email = emailInput.value;
        const password = passwordInput.value;

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, email, password}),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/';
                } else {
                    errorToastify(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});

document.addEventListener('DOMContentLoaded', function () {

    const loginForm = document.querySelector('#loginForm');
    const usernameInput = document.querySelector('#usernameLogin');
    const passwordInput = document.querySelector('#passwordLogin');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const username = usernameInput.value;
        const password = passwordInput.value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({username, password}),
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.href = '/';
                } else {
                    errorToastify(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
