document.querySelectorAll('.subject-info-button').forEach(btn => {
    const container = btn.closest('.subject-container');
    const hoverInfo = container.querySelector('.subject-hover-info');
    const buttonsContainer = btn.closest('.main-menu-subject-buttons-container');
    const otherChildren = Array.from(container.children).filter(
        el => el !== hoverInfo && el !== buttonsContainer
    );

    function showInfo() {
        hoverInfo.style.display = 'block';
        otherChildren.forEach(el => {
            el.style.opacity = '0';
            el.style.pointerEvents = 'none';
        });
    }

    function hideInfo() {
        hoverInfo.style.display = 'none';
        otherChildren.forEach(el => {
            el.style.opacity = '';
            el.style.pointerEvents = '';
        });
    }

    btn.addEventListener('mouseenter', showInfo);
    btn.addEventListener('mouseleave', hideInfo);
    hoverInfo.addEventListener('mouseenter', showInfo);
    hoverInfo.addEventListener('mouseleave', hideInfo);
});

document.querySelectorAll('.event-join-button.status-open').forEach(button => {
    button.addEventListener('click', () => {
        window.location.href = '/index/challenge';
    });
});