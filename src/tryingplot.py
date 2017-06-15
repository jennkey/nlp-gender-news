import plotly

var names = ['A', 'B', 'C']
var trace1 = {
  	x: [4, 5, 6],
 	y: [1, 2, 3],
  	text: names,
  	hoverinfo: 'x+y+text',
  	xaxis: 'x',
  	yaxis: 'y',
  	mode: 'markers',
  	type: 'scatter'
};

var trace2 = {
  	x: [50, 60, 70],
  	y: [1, 2, 3],
  	text: names,
  	hoverinfo: 'x+y+text',
  	xaxis: 'x2',
  	yaxis: 'y2',
  	mode: 'markers',
  	type: 'scatter'
};

var data = [trace1, trace2];

var layout = {
	hovermode:'compare',
	yaxis: {anchor: 'x'},
	xaxis: {domain: [0, 0.45]},
  	yaxis2: {anchor: 'x2'},
  	xaxis2: {domain: [0.55, 1]}

};

Plotly.newPlot('graph', data, layout);
var myPlot = document.getElementById('graph');
myPlot.on('plotly_hover', function (eventdata){
	console.log(eventdata.xvals);
    Plotly.Fx.hover('graph',
    				[
	    				{ curveNumber: 0, pointNumber:eventdata.points[0].pointNumber },
    					{ curveNumber: 1, pointNumber:eventdata.points[0].pointNumber },
    				],
        			['xy', 'x2y2']
    );
});
