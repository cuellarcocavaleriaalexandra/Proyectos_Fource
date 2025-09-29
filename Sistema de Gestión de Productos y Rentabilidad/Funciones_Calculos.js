document.getElementById('pareto').addEventListener('click', function() {
    var companyId = this.getAttribute('data-id');
    window.location.href = 'Calculo_Pareto.php?id=' + companyId;
});

document.getElementById('profitability').addEventListener('click', function() {
    var companyId = this.getAttribute('data-id');
    window.location.href = 'Calculo_Rentabilidad.php?id=' + companyId;
});
