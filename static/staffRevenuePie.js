google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

const mdirect0 = NSDecimalNumber(mdirect[0]);
const mindirect0 = NSDecimalNumber(mindirect[0]);

function drawChart() {

  var data = google.visualization.arrayToDataTable([
    ['Sales', 'Amount'],
    ['Direct', mdirect0],
    ['Indirect', mindirect0],

  ]);

  var options = {
    title: 'Total Revenue Last Month'
  };

  var chart = new google.visualization.PieChart(document.getElementById('revenue_chart'));

  chart.draw(data, options);
}
