var cfg = {
	xaxis: { min:0, max:15, tickSize: 3 }, 
	yaxis: { min:-20, max:20, show: false },
	series: { lines: { lineWidth: 4, }, points: { radius: 0.1, } },
	colors: ['gray'],
};
function engine(element, reaction_rate_function) {
	var e = {}; // the engine object!
	e.container = $(element);
	var q = {};
	e.reaction_rate_function = reaction_rate_function;
	e.quantities = q;
	q.temperature = {
		"update": function () {
			var old_value = this.value;
			this.value += reaction_rate_function(q)*timestep/1000
			if (this.value < 0) { this.value = 0; }
			
			if (old_value != this.value) { return true; }
		},
		"out": function () {
			e.container.find('.temp-out').html(this.value.toFixed(2));
			if (this.value > q.damage_threshhold.value) { e.container.find('.damage').show();} 
			else { e.container.find('.damage').hide(); }
			if (this.value < q.ignition_threshhold.value) { e.container.find('.noignition').show(); } 
			else { e.container.find('.noignition').hide(); }

			for (var i=0; i<this.graph_data.data.length; i++) {
				this.graph_data.data[i][0] = this.value;
			}
			this.graph_data.data[1][1] = get_current_potential(this.value);
		},
		"value": 0,
		"graph_data": {
			data: [[0,cfg.yaxis.max+2],[0,0],[0,cfg.yaxis.min-2]], 
			lines: {show: true, lineWidth: 1}, 
			points: {show: true, radius: 3}, 
			color: 'red',
		},
	};
	function get_current_potential(t) {
		var data_series = all_graph_data[0].data;
		var number_of_points = data_series.length;
		var width = e.graph_config.xaxis.max - e.graph_config.xaxis.min;
		var index = Math.floor((t / width) * number_of_points);
		var below = data_series[index], above = data_series[index+1];
		if (!below) { return 0; }
		if (!above) { return null; }
		//console.log("got current potential");
		return below[1] + ((t - below[0])/(above[0] - below[0]))*(above[1] - below[1]);
	}
	q.fuel_flow_rate = {
		"update": function () { 
			var old_value = this.value;
			this.value = parseFloat(e.container.find('[name=fuel]').val());
			
			if (old_value != this.value) {
				return true;
			}
		},
		"out": function () { generate_graph_points(); q.temperature.out(); },
		"value": 0,
	};
	q.ignition_threshhold = {
		"update": function () {},
		"out": function() {
			this.graph_data.data = [[this.value, cfg.yaxis.max+2], [this.value, cfg.yaxis.min-2], [-this.value, cfg.yaxis.min-2], [-this.value, cfg.yaxis.max+2], [this.value, cfg.yaxis.max+2]];
		},
		"value": 2,
		"graph_data": {
			data: [],
			lines: {show: true, lineWidth: 0, fill: 0.2},
			points: {show: false},
			color: 'blue',
		},
	};
	q.damage_threshhold = {
		"update": function () {},
		"out": function() {
			this.graph_data.data = [[this.value, cfg.yaxis.min-2], [this.value, cfg.yaxis.max+2], [20*this.value, cfg.yaxis.max+2], [20*this.value, cfg.yaxis.min-2], [this.value, cfg.yaxis.min-2]];
		},
		"value": 10,
		"graph_data": {
			data: [],
			lines: {show: true, lineWidth: 0, fill: 0.2},
			points: {show: false},
			color: 'yellow',
		},
	};
	q.ignition_boost = {
		"update": function () {},
		"out": function() {},
		"value": 5,
	};
	q.temperature_decay = {
		"update": function () {},
		"out": function () {},
		"value": 0.5,
	};

	var ghost_count = 1, ghost_separation = 0.05;
	var ghost_data_points = Array(1 + ghost_count*2);
	
	var all_graph_data = [{"data": [], lines: {show: true}, points: {show: false}}];
	for (var s=1; s<=ghost_count; s++) {
		all_graph_data.push({"data": [], lines: {show: true, lineWidth: 0.5}, points: {show: true}});
		all_graph_data.push({"data": [], lines: {show: true, lineWidth: 0.5}, points: {show: true}});
	}
	all_graph_data.push(q.temperature.graph_data);
	all_graph_data.push(q.ignition_threshhold.graph_data);
	all_graph_data.push(q.damage_threshhold.graph_data);
	
	e.graph_config = { 
		xaxis: { min:0, max:15, tickSize: 3 }, 
		yaxis: { min:-20, max:20, show: false },
		series: { lines: { lineWidth: 4, }, points: { radius: 0.1, } },
		colors: ['gray'],
	};
	function generate_graph_points() {
		var step_size = 0.3;

		var flow_value = q.fuel_flow_rate.value;

		ghost_data_points[0] = $.extend({}, q, {"fuel_flow_rate": {"value": flow_value}, "temperature": {"value": 0}});
		var potentials = [0];
		for (var s=1; s <= ghost_count; s++) {
			ghost_data_points[s] = $.extend({}, q);
			$.extend(ghost_data_points[s], {
				"fuel_flow_rate": {"value": flow_value + ghost_separation * s}, 
				"temperature": {"value": 0}
			});
			potentials.push(0);
			ghost_data_points[s+ghost_count] = $.extend({}, q);
			$.extend(ghost_data_points[s+ghost_count], {
				"fuel_flow_rate": {"value": flow_value - ghost_separation * s}, 
				"temperature": {"value": 0}
			});
			potentials.push(0);
		}
		for (var s=0; s<potentials.length; s++) { all_graph_data[s].data = []; }
		for (var i=e.graph_config.xaxis.min; i<e.graph_config.xaxis.max; i+=step_size) {
			for (var s=0; s<potentials.length; s++) {
				all_graph_data[s].data.push([i, potentials[s]]);
				ghost_data_points[s].temperature.value = i;
				potentials[s] += -1 * step_size * reaction_rate_function(ghost_data_points[s]);
			}
		}
		//console.log("regenerated graph points");
	}
	function update_graph() {
		e.graph_plot.setData(all_graph_data);
		e.graph_plot.draw();
	}

	var a, b;
	var timestep = 30;
	e.container.ready(function () {
		e.graph = e.container.find('.potential_plot');
		e.graph_plot = $.plot(e.graph, [[]], e.graph_config);

		jQuery.each(q, function(name, x) { x.out(); });
		e.container.find('[name=ignition]').on('click', function() { q.temperature.value += q.ignition_boost.value; });
		a = setInterval(jQuery.each, timestep, q, function(name, x) { if (x.update()) { x.out(); } });
		b = setInterval(update_graph, timestep);
	});
	return e;
}

function temperature_derivative (fn, step) {
	return function (quantities) {
		var next_input = $.extend({}, quantities);
		next_input.temperature = {"value": quantities.temperature.value + step};
		return (fn(next_input) - fn(quantities))/step;
	};
};
var step = 0.005;
function alt_engine(element, reaction_rate_potential_function) {
	return engine(element, temperature_derivative(reaction_rate_potential_function, step));
}