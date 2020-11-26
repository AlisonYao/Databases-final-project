google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart2);

const time1 = time[0];
const time2 = time[1];

const monthticket1 = monthticket[0];
const monthticket2 = monthticket[1];

function drawBarChart2() {
  var data = new google.visualization.arrayToDataTable([
    ["Tickets", "#tickets"],
    [time1, monthticket1],
    [time2, monthticket2],
  ]);

  var options = {
    width: 800,
    legend: { position: "none" },
    chart: {
      title: "amounts of ticket sold",
      subtitle: "based on #tickets monthly",
    },
    axes: {
      x: {
        0: { side: "bottom", label: "#tickets monthly" },
      },
    },
    bar: { groupWidth: "50%" },
  };

  var chart = new google.charts.Bar(document.getElementById("left"));
  // Convert the Classic options to Material options.
  chart.draw(data, google.charts.Bar.convertOptions(options));
}
