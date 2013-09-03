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
			container.find('#temp-out').html(this.value.toFixed(2));
			if (this.value > damage_threshhold) { container.find('#damage').show();} 
			else { container.find('#damage').hide(); }
			if (this.value < q.ignition_threshhold.value) { container.find('#noignition').show(); } 
			else { container.find('#noignition').hide(); }
		},
		"value": 0,
	};

	q.fuel_flow_rate = {
		"update": function () { this.value = container.find('[name=fuel]').val(); },
		"out": function () { update_graph(); },
		"value": 0,
	};

	q.ignition_threshhold = {
		"update": function () {},
		"out": function() {},
		"value": 2,
	};
	var ignition_boost = 5;
	var damage_threshhold = 10;
	var temperature_decay = 0.5;
	var timestep=10;

	var graph_config = { xaxis: { min:0, max:15 }, yaxis: { min:-4, max:4 } };
	function update_graph() {
		var step_size = 0.2;

		var data = [], area=0;
		for (var i=0; i<15; i+=step_size) {
			area -= step_size * reaction_rate_function({
				"fuel_flow_rate": q.fuel_flow_rate, 
				"temperature": { "value":i },
				"ignition_threshhold": q.ignition_threshhold,
			});
			data.push([i, area]);
		}
		graph_plot.setData([data]);
		graph_plot.draw();
	}

	var a, b;
	container.ready(function () {
		container.find('[name=ignition]').on('click', function() { q.temperature.value += ignition_boost; });
		a = setInterval(jQuery.each, timestep, q, function(name, x) { x.update(); });
		b = setInterval(jQuery.each, timestep, q, function(name, x) { x.out(); });
		graph = container.find('#potential_plot');
		graph_plot = $.plot(graph, [[]], graph_config);
	});
	return {
		'container': container,
		'quantities': q,
		'graph_container': graph,
		'graph_plot': graph_plot,
	};
}
