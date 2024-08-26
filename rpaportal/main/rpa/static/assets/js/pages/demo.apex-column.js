var distributedColumnData = {
    chart: { height: 380, type: "bar", toolbar: { show: !1 }, events: { click: function(t, o, a) { console.log(t, o, a) } } },
    colors: colors = dataColors ? dataColors.split(",") : colors,
    plotOptions: { bar: { columnWidth: "45%", distributed: !0 } },
    dataLabels: { enabled: !1 },
    series: [{ data: [21, 22, 10, 28, 16] }],
    xaxis: {
        categories: ["식품", "화학", "바이오", "패키징", "Staff"],
        labels: { style: { colors: colors, fontSize: "14px" } }
    },
    legend: { offsetY: 4 },
    grid: { row: { colors: ["transparent", "transparent"], opacity: .2 }, borderColor: "#f1f3fa" }
};

var distributedColumnChart = new ApexCharts(document.querySelector("#distributed-column"), distributedColumnData);
distributedColumnChart.render();
