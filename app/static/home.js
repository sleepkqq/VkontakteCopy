document.addEventListener('DOMContentLoaded', function () {

    const logoutForm = document.querySelector('#logoutForm');

    logoutForm.addEventListener('submit', function (event) {
        event.preventDefault();

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