// google.charts.load("current", { packages: ["bar"] });
// google.charts.setOnLoadCallback(drawBarChart2);

// const time = time[0];

// const monthticket = monthticket[0];

google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

const mdirect = mdirect;

const mindirect = mindirect;

const ydirect = ydirect;

const yindirect = yindirect;

function drawChart() {

  var data = google.visualization.arrayToDataTable([
    ['Sales', 'Amount'],
    ['Direct',     mdirect],
    ['Indirect',      mindirect],

  ]);

  var options = {
    title: 'Total Revenue Last Month'
  };

  var chart = new google.visualization.PieChart(document.getElementById('piechart'));

  chart.draw(data, options);
}
