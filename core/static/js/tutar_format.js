alert("TUTAR FORMAT YUKLENDI");
document.addEventListener("DOMContentLoaded", function() {

    const input = document.querySelector("#id_tutar");

    if (!input) return;

    function formatNumber(value) {
        value = value.replace(/\D/g, "");
        return value.replace(/\B(?=(\d{3})+(?!\d))/g, ".");
    }

    input.addEventListener("input", function() {
        const raw = this.value.replace(/\./g, "");
        this.value = formatNumber(raw);
    });

    document.querySelector("form").addEventListener("submit", function() {
        input.value = input.value.replace(/\./g, "");
    });

});