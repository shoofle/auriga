var data, config;
$(document).ready(function() {
		data = [];
		for (var i=0; i<10; i++) {
		data.push([i, i*i/10]);
		}
		config = {};
		config.yaxis = {max: 10};
		config.xaxis = {min: 0, max: 10};
		$.plot($('#the_graph'), [data], config);
		});
