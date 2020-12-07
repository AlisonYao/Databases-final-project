google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

const ydirect0 = ydirect[0];

const yindirect0 = yindirect[0];

function drawChart() {

  var data = google.visualization.arrayToDataTable([
    ['Sales', 'Amount'],
    ['Direct', ydirect0],
    ['Indirect', yindirect0],

  ]);

  var options = {
    title: 'Total Revenue Last Year'
  };

  var chart = new google.visualization.PieChart(document.getElementById('revenue_chart2'));

  chart.draw(data, options);
}
