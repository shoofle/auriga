var a=true;
function engine(element, reaction_rate_function) {
	var container = $(element);
	var graph, graph_plot;
	var q = {};
	q.temperature = {
		"update": function () {
			this.value += reaction_rate_function(q)*timestep/1000
			if (this.value < 0) { this.value = 0; }
		},
		"out": function () {
			container.find('.temp-out').html(this.value.toFixed(2));
			if (this.value > damage_threshhold) { container.find('.damage').show();} 
			else { container.find('.damage').hide(); }
			if (this.value < q.ignition_threshhold.value) { container.find('.noignition').show(); } 
			else { container.find('.noignition').hide(); }
		},
		"value": 0,
	};

	q.fuel_flow_rate = {
		"update": function () { this.value = parseFloat(container.find('[name=fuel]').val()); },
		"out": function () { update_graph(); },
		"value": 0,
	};

	q.ignition_threshhold = {
		"update": function () {},
		"out": function() {},
		"value": 2,
	};
	q.ignition_boost = {
		"update": function () {},
		"out": function() {},
		"value": 5,
	}
	var damage_threshhold = 10;
	var temperature_decay = 0.5;
	var timestep=10;

	var graph_config = { 
		xaxis: { min:0, max:15, tickSize: 3 }, 
		yaxis: { min:-4, max:4, show: false },
		series: {
			lines: {
				lineWidth: 4,
			},
			points: {
				show: true,
				radius: 0.1,
			}
		},
		colors: ['red'],
	};
	function update_graph() {
		var step_size = 0.3;

		var data = [
		{data: [], lines: {show: false}, points: {show: true}},
		{data: [], lines: {show: true}, points: {show: false}},
		{data: [], lines: {show: false}, points: {show: true}},
		];
		var points = [$.extend({}, q), jQuery.extend({}, q), jQuery.extend({}, q)];
		var flow_value = q.fuel_flow_rate.value;
		for (var series=0; series<3; series++) {
			points[series].fuel_flow_rate = {"value": flow_value + 0.01*(series-1)};
			points[series].temperature = {"value": 0};

			var prev=0;
			for (var i=0; i<15; i+=step_size) {
				points[series].temperature.value = i;
				prev = prev - step_size * reaction_rate_function(points[series]);
				data[series].data.push([i, prev]);
			}
		}
					if (a) { console.log(points); a=false; }

		graph_plot.setData(data);
		graph_plot.draw();
	}

	var a, b;
	container.ready(function () {
		container.find('[name=ignition]').on('click', function() { q.temperature.value += q.ignition_boost.value; });
		a = setInterval(jQuery.each, timestep, q, function(name, x) { x.update(); });
		b = setInterval(jQuery.each, timestep, q, function(name, x) { x.out(); });
		graph = container.find('.potential_plot');
		graph_plot = $.plot(graph, [[]], graph_config);
	});
	return {
		'container': container,
		'quantities': q,
		'graph_container': graph,
		'graph_plot': graph_plot,
	};
}
