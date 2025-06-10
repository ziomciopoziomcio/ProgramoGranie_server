document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('file-input');
    const chooseFileButton = document.getElementById('choose-file-button');
    const dragDropArea = document.getElementById('drag-drop-area');
    const fileList = document.getElementById('file-list');
    const playButton = document.getElementById('play-button');
    let selectedFile = null; // To track the single selected file

    // Trigger file input when "Wybierz je z dysku" button is clicked
    chooseFileButton?.addEventListener('click', (event) => {
        event.preventDefault(); // Prevent default behavior
        fileInput.click();
    });

    // Handle file selection
    fileInput?.addEventListener('change', (event) => {
        addFile(event.target.files[0]);
        fileInput.value = ''; // Clear input to allow re-selection of the same file
    });

    // Handle drag-and-drop functionality
    dragDropArea?.addEventListener('dragover', (event) => {
        event.preventDefault();
        dragDropArea.style.borderColor = 'blue';
    });

    dragDropArea?.addEventListener('dragleave', () => {
        dragDropArea.style.borderColor = '#ccc';
    });

    dragDropArea?.addEventListener('drop', (event) => {
        event.preventDefault();
        dragDropArea.style.borderColor = '#ccc';
        addFile(event.dataTransfer.files[0]);
    });

    // Add a single file to the list
    function addFile(file) {
        if (!file) return;

        // Clear previous file
        selectedFile = file;
        fileList.innerHTML = '';

        // Add the new file to the list
        const li = document.createElement('li');
        li.textContent = file.name;
        fileList.appendChild(li);
    }

    // Play button navigates to the game page
    playButton?.addEventListener('click', () => {
        window.location.href = '/index/game';
    });
});