
var colors = ["#12ABE8"];
var dataColors = $("#basic-treemap").data("colors");
var options = {
    series: [{
        data: output_data
    }],
    colors: colors = dataColors ? dataColors.split(",") : colors,
    legend: { show: !1 },
    chart: { height: 350, type: "treemap" },
    title: { text: "삼양그룹 RPA 업무군 TREEMAP", align: "left" }
};
var chart = new ApexCharts(document.querySelector("#basic-treemap"), options);
chart.render();



colors = ["#727cf5", "#0acf97", "#fa5c7c"];
dataColors = $("#distributed-treemap").data("colors");
options = {
    series: [{
        data: output_data2
    }],
    legend: { show: !1 },
    chart: { height: 350, type: "treemap" },
    title: { text: "*Total", align: "left" },
    colors: colors = dataColors ? dataColors.split(",") : colors,
    plotOptions: {
        treemap: {
            distributed: !0,
            enableShades: !1
        }
    }
};
chart = new ApexCharts(document.querySelector("#distributed-treemap"), options);
chart.render();

// Treemap with Color scale
colors = ["#727cf5", "#0acf97", "#fa5c7c"];
dataColors = $("#color-range-treemap").data("colors");
options = {
    series: [{
        data: [
            { x: "INTC", y: 1.2 },
            { x: "GS", y: .4 },
            { x: "CVX", y: -1.4 },
            { x: "GE", y: 2.7 },
            { x: "CAT", y: -.3 },
            { x: "RTX", y: 5.1 },
            { x: "CSCO", y: -2.3 },
            { x: "JNJ", y: 2.1 },
            { x: "PG", y: .3 },
            { x: "TRV", y: .12 },
            { x: "MMM", y: -2.31 },
            { x: "NKE", y: 3.98 },
            { x: "IYT", y: 1.67 }
        ]
    }],
    legend: { show: !1 },
    chart: { height: 350, type: "treemap" },
    title: { text: "Treemap with Color scale", align: "center" },
    dataLabels: {
        enabled: !0,
        style: { fontSize: "12px" },
        formatter: function(e, a) { return [e, a.value] },
        offsetY: -4
    },
    plotOptions: {
        treemap: {
            enableShades: !0,
            shadeIntensity: .5,
            reverseNegativeShade: !0,
            colorScale: {
                ranges: [
                    { from: -6, to: 0, color: (colors = dataColors ? dataColors.split(",") : colors)[0] },
                    { from: .001, to: 6, color: colors[1] }
                ]
            }
        }
    }
};
chart = new ApexCharts(document.querySelector("#color-range-treemap"), options);
chart.render();
