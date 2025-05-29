// zmiana karty w formularzu rejestracji (pracownik/student)
function switchTab(formId, tabElement) {
    $('.form').removeClass('active');
    $('.tab').removeClass('active');

    $('#' + formId).addClass('active');
    $(tabElement).addClass('active');
}
