// zmiana karty w formularzu rejestracji (pracownik/student)
function switchTab(formId, tabElement) {
    $('.form').removeClass('active');
    $('.tab').removeClass('active');

    $('#' + formId).addClass('active');
    $(tabElement).addClass('active');

    // Update the role value based on the selected tab
    const role = formId === 'form-pracownik' ? 'Prowadzący' : 'Student';
    $('#' + formId).find('input[name="role"]').val(role);
}
