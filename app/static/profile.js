document.addEventListener('DOMContentLoaded', function () {
    const statusText = document.getElementById('status-text');
    const changeStatusInput = document.getElementById('changeStatusInput');
    const username = document.getElementById('usernameDiv').getAttribute('data-my-variable');

    changeStatusInput.addEventListener('click', function (e) {
        e.preventDefault();

        const inputField = document.createElement('input');
        inputField.type = 'text';
        inputField.value = statusText.textContent.trim();
        inputField.maxLength = 100;
        inputField.id = 'status-input';

        statusText.replaceWith(inputField);

        inputField.addEventListener('keyup', function (event) {
            if (event.key === 'Enter') {

                const newStatus = inputField.value;

                fetch(`/edit/status/${username}`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({newStatus}),
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            successToastify(data.message);
                            statusText.textContent = newStatus;
                            inputField.replaceWith(statusText);
                        } else {
                            errorToastify(data.message);
                        }
                    })
                    .catch(error => {
                        console.error('Error:', error);
                    });
            } else if (event.key === 'Escape') {
                inputField.replaceWith(statusText);
            }
        });

        inputField.focus();
    });
});