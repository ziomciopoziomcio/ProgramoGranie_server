document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const chooseFileButton = document.getElementById('choose-file-button');
    const dragDropArea = document.getElementById('drag-drop-area');
    const fileList = document.getElementById('file-list');
    const sendFileButton = document.getElementById('send-file-button');
    const selectedFiles = new Set(); // To track unique files
    const filesToUpload = []; // To store files for upload

    // Trigger file input when "Wybierz je z dysku" button is clicked
    chooseFileButton.addEventListener('click', () => {
        fileInput.click();
    });

    // Handle file selection
    fileInput.addEventListener('change', (event) => {
        addFiles(event.target.files);
    });

    // Handle drag-and-drop functionality
    dragDropArea.addEventListener('dragover', (event) => {
        event.preventDefault();
        dragDropArea.style.borderColor = 'blue';
    });

    dragDropArea.addEventListener('dragleave', () => {
        dragDropArea.style.borderColor = '#ccc';
    });

    dragDropArea.addEventListener('drop', (event) => {
        event.preventDefault();
        dragDropArea.style.borderColor = '#ccc';
        addFiles(event.dataTransfer.files);
    });

    // Add files to the list
    function addFiles(files) {
        Array.from(files).forEach((file) => {
            if (!selectedFiles.has(file.name)) {
                selectedFiles.add(file.name);
                filesToUpload.push(file);
                const li = document.createElement('li');
                li.textContent = file.name;
                fileList.appendChild(li);
            }
        });
    }

    // Handle file upload
    sendFileButton.addEventListener('click', async () => {
        if (filesToUpload.length === 0) {
            alert('Nie wybrano żadnych plików do przesłania.');
            return;
        }

        const formData = new FormData();
        filesToUpload.forEach((file) => {
            formData.append('file', file);
        });

        try {
            const response = await fetch('/index/challenge', {
                method: 'POST',
                body: formData,
            });

            if (response.ok) {
                const uploadedFiles = await response.json();
                alert('Pliki zostały pomyślnie przesłane!');
                console.log('Uploaded files:', uploadedFiles);
            } else {
                const error = await response.json();
                alert(`Błąd przesyłania plików: ${error.error}`);
            }
        } catch (error) {
            alert('Wystąpił błąd podczas przesyłania plików.');
            console.error(error);
        }
    });
});

// play button navigates to the game page
document.addEventListener('DOMContentLoaded', () => {
    const playButton = document.getElementById('play-button');
    if (playButton) {
        playButton.addEventListener('click', () => {
            window.location.href = '/index/game';
        });
    }
});