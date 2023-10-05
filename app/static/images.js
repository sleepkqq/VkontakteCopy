document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-button');

    deleteButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            const deleteForm = event.target.closest('.delete-form');
            if (deleteForm) {
                const imageId = deleteForm.getAttribute('action').split('/').pop();
                Swal.fire({
                    title: 'Вы уверены?',
                    text: "Вы не сможете восстановить эту запись!",
                    icon: 'warning',
                    showCancelButton: true,
                    confirmButtonColor: '#3085d6',
                    cancelButtonColor: '#d33',
                    confirmButtonText: 'Удалить',
                    cancelButtonText: 'Закрыть',
                }).then((result) => {
                    if (result.isConfirmed) {
                        deleteImage(imageId);
                        Swal.fire(
                            'Удалено!',
                            'Запись успешно удалена.',
                            'success'
                        )
                    }
                })
            }
        });
    });

    function deleteImage(imageId) {
        fetch(`/image/delete/${imageId}`, {
            method: 'POST',
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    window.location.reload();
                } else {
                    errorToastify(data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
    }
});