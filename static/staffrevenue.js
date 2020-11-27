google.charts.load("current", { packages: ["bar"] });
google.charts.setOnLoadCallback(drawBarChart2);

const time = time[0];

const monthticket = monthticket[0];

function drawBarChart2() {
  var data = new google.visualization.arrayToDataTable([
    ["#tickets","Month"],
    [monthticket,time]
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
