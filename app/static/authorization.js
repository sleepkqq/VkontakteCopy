document.addEventListener('DOMContentLoaded', function () {

    const registerForm = document.querySelector('#registerForm');
    const phoneNumberInput = document.querySelector('#phoneNumberRegister')
    const firstNameInput = document.querySelector('#firstNameRegister');
    const secondNameInput = document.querySelector('#secondNameRegister');
    const passwordInput = document.querySelector('#passwordRegister');

    document.querySelector('#toast-container');
    registerForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the default form submission

        const phoneNumber = phoneNumberInput.value;
        const firstName = firstNameInput.value;
        const secondName = secondNameInput.value;
        const password = passwordInput.value;

        fetch('/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({phoneNumber, firstName, secondName, password}),
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
    const phoneNumberInput = document.querySelector('#phoneNumberLogin')
    const passwordInput = document.querySelector('#passwordLogin');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const phoneNumber = phoneNumberInput.value;
        const password = passwordInput.value;

        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({phoneNumber, password}),
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
