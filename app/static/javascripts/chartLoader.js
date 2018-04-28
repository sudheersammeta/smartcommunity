// Load google charts
google.charts.load('current', {'packages':['corechart']});
google.charts.setOnLoadCallback(drawChart);

// Draw the chart and set the chart values
function drawChart() {
  var data = google.visualization.arrayToDataTable([
  ['Role', 'Number of People'],
  ['Teachers', school_details.teacher_count ],
  ['Staff', school_details.staff_count],
  ['Students', school_details.student_count],
  ['Parents', school_details.parent_count]
]);

  // Optional; add a title and set the width and height of the chart
  var options = {'title':'My School Community', 'width':600, 'height':500};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechart1'));
  chart.draw(data, options);


  //var data = new google.visualization.DataTable();
  //data.addColumn('string','Grade');
  //data.addColumn('number','Strength');

  //class_details.unshift(['Grade', 'Strength']);
  //alert(class_details);

  var twoDArray = [['Grade', 'Strength']];
  for(i=0;i<class_details.length;i++){
    var obj=class_details[i];
    twoDArray.push(['Grade ' + obj[0], obj[1]]);
  }

  alert(twoDArray);


  var data = new google.visualization.arrayToDataTable(twoDArray,false);

    // Optional; add a title and set the width and height of the chart
  var options = {'title':'My School Classes', 'width':600, 'height':500};

  // Display the chart inside the <div> element with id="piechart"
  var chart = new google.visualization.PieChart(document.getElementById('piechart2'));
  chart.draw(data, options);


}
