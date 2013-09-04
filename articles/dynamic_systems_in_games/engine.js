var a=true;
function engine(element, reaction_rate_function) {
	var container = $(element);
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

	var graph, graph_plot, graph_config = { 
		xaxis: { min:0, max:15, tickSize: 3 }, 
		yaxis: { min:-4, max:4, show: false },
		series: {
			lines: {
				lineWidth: 4,
			},
			points: {
				radius: 0.1,
			}
		},
		colors: ['red'],
	};
	function update_graph() {
		var step_size = 0.5;
		var ghost_count = 1, ghost_separation = 0.03;

		var flow_value = q.fuel_flow_rate.value;
		var the_current_potential=0, delta;

		var d = [{"data": [], lines: {show: true}, points: {show: false}}];
		var points = [$.extend({}, q, {"fuel_flow_rate": {"value": flow_value}, "temperature": {"value": 0}})];
		var potentials = [0];
		
		for (var s=1; s <= ghost_count; s++) {
			d.push(	{"data": [], lines: {show: false}, points: {show: true}});
			var p1 = $.extend({}, q);
			$.extend(p1, {"fuel_flow_rate": {"value": flow_value + ghost_separation * s}, "temperature": {"value": 0}});
			points.push(p1);
			potentials.push(0)
			d.push(	{"data": [], lines: {show: false}, points: {show: true}});
			var p2 = $.extend({}, q);
			$.extend(p2, {"fuel_flow_rate": {"value": flow_value - ghost_separation * s}, "temperature": {"value": 0}});
			points.push(p2);
			potentials.push(0)
		}
		for (var i=0; i<15; i+=step_size) {
			for (var s=0; s<potentials.length; s++) {
				d[s].data.push([i, potentials[s]]);
				points[s].temperature.value = i;
				delta = -1 * reaction_rate_function(points[s]);
				if (s == 0 && (i <= q.temperature.value) && (q.temperature.value < i+step_size)) {
					the_current_potential = potentials[0] + delta * (q.temperature.value - i);
				}
				potentials[s] += delta * step_size;
			}
		}
		d.push({
			data: [[q.temperature.value, -10], [q.temperature.value, the_current_potential], [q.temperature.value, 10]], 
			lines: {show: true, lineWidth: 1}, 
			points: {show: true, radius: 3}, 
			color: 'blue',
		});
		if (a) { console.log(points); a=false; }

		graph_plot.setData(d);
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
		'poke': function () { this.graph_container = graph; this.graph_plot = graph_plot; },
	};
}
