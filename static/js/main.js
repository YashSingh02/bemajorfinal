document.getElementById('fileInput').addEventListener('change', function() {
    readURL(this);
});

document.getElementById('predictBtn').addEventListener('click', function() {
    uploadFile();
});

function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            document.getElementById('imagePreview').style.backgroundImage = 'url(' + e.target.result + ')';
            document.getElementById('imagePreview').style.display = 'none';
            document.getElementById('imagePreview').style.display = 'block';
        }
        reader.readAsDataURL(input.files[0]);
    }
}

function uploadFile() {
    var formData = new FormData(document.getElementById('uploadForm'));
    fetch('/predict', {
        method: 'POST',
        body: formData
    })
    .then(response => response.text())
    .then(data => {
        document.getElementById('result').innerText = data;
    })
    .catch(error => {
        console.error('Error:', error);
    });
}