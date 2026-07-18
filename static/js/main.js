// Konfirmasi sebelum menghapus data (proyek, pesan, skill, sertifikasi)
document.addEventListener('DOMContentLoaded', function () {
    const deleteForms = document.querySelectorAll('.delete-form');

    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (event) {
            const konfirmasi = confirm('Yakin ingin menghapus data ini? Tindakan ini tidak bisa dibatalkan.');
            if (!konfirmasi) {
                event.preventDefault();
            }
        });
    });
});