document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const chooseFileButton = document.getElementById('choose-file-button');
    const dragDropArea = document.getElementById('drag-drop-area');
    const fileList = document.getElementById('file-list');
    const selectedFiles = new Set(); // To track unique files

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
                const li = document.createElement('li');
                li.textContent = file.name;
                fileList.appendChild(li);
            }
        });
    }
});