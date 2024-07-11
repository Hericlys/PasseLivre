document.addEventListener('DOMContentLoaded', function() {
    const input = document.querySelector('input[name="3x4"]');
    const modal = document.getElementById('cropperModal');
    const image = document.getElementById('image');
    const cropButton = document.getElementById('cropButton');
    let cropper;

    input.addEventListener('change', function(event) {
        const files = event.target.files;
        const done = function(url) {
            image.src = url;
            modal.style.display = 'flex';
            if (cropper) {
                cropper.destroy();
            }
            cropper = new Cropper(image, {
                aspectRatio: 3 / 4,
                viewMode: 1,
            });
        };
        let reader;
        let file;
        if (files && files.length > 0) {
            file = files[0];
            if (URL) {
                done(URL.createObjectURL(file));
            } else if (FileReader) {
                reader = new FileReader();
                reader.onload = function(e) {
                    done(reader.result);
                };
                reader.readAsDataURL(file);
            }
        }
    });

    cropButton.addEventListener('click', function() {
        const canvas = cropper.getCroppedCanvas({
            width: 300,
            height: 400,
        });
        canvas.toBlob(function(blob) {
            const file = new File([blob], "cropped_image.jpg", { type: "image/jpeg" });
            const dataTransfer = new DataTransfer();
            dataTransfer.items.add(file);
            input.files = dataTransfer.files;
            // Fechar o modal
            modal.style.display = 'none';
        });
    });

    document.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
            if (cropper) {
                cropper.destroy();
            }
        }
    });
});
