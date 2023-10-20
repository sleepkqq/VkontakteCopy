function errorToastify(message) {
    Toastify({
        text: message,
        duration: 1500,
        stopOnFocus: true,
        avatar: "https://www.freeiconspng.com/uploads/error-icon-4.png",
        style: {
            background: "#fff",
            fontFamily: "Arial, sans-serif",
            color: "#000",
            paddingLeft: "2px",
            paddingRight: "10px",
        },
    }).showToast();
}

function successToastify(message) {
    Toastify({
        text: message,
        duration: 3000,
        stopOnFocus: true,
        avatar: "https://www.freeiconspng.com/thumbs/success-icon/success-icon-10.png",
        style: {
            background: "#fff",
            fontFamily: "Arial, sans-serif",
            color: "#000",
            paddingLeft: "2px",
            paddingRight: "10px",
        },
    }).showToast();
}

document.querySelector('.user-container').addEventListener('click', function (event) {
    const dropdown = document.getElementById('dropdown');
    dropdown.style.display = (dropdown.style.display === 'block') ? 'none' : 'block';

    event.stopPropagation();
});

document.addEventListener('click', function (event) {
    const dropdown = document.getElementById('dropdown');

    if (dropdown.style.display === 'block' && !dropdown.contains(event.target)) {
        dropdown.style.display = 'none';
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const logoutForm = document.querySelector('#logoutForm');

    logoutForm.addEventListener('submit', function (event) {
        event.preventDefault();

        Swal.fire({
            title: 'Выйти из аккаунта?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonColor: '#3085d6',
            cancelButtonColor: '#d33',
            confirmButtonText: 'Подтвердить',
            cancelButtonText: 'Закрыть',
        }).then((result) => {
            if (result.isConfirmed) {
                fetch('/logout', {
                    method: 'POST',
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
            }
        })
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const uploadForm = document.querySelector('#uploadForm');

    uploadForm.addEventListener('submit', function (event) {
        event.preventDefault();

        const formData = new FormData(uploadForm);

        fetch('/image/upload', {
            method: 'POST',
            body: formData,
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector('#text').value = '';
                    document.querySelector('#photo').value = '';
                    successToastify(data.message);
                } else {
                    errorToastify(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    });
});
