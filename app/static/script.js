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
