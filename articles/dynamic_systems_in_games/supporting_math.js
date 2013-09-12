function make_gaussian(mean, standard_deviation) {
	return function (x) {
		return Math.exp(-Math.pow((x-mean)/standard_deviation, 2))/(standard_deviation * Math.sqrt(2*Math.PI));
	};
}
function make_bell(mean, standard_deviation) {
	return function (x) {
		return Math.exp(-Math.pow((x-mean)/standard_deviation, 2));
	};
}
function exp_decay(height, width) {
	return function (x) {
		return height*Math.exp(-x/width);
	};
}
function exp_growth(height, width) {
	return function (x) {
		return height*Math.exp(x/width);
	};
}