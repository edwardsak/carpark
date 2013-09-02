function today() { 
	var date = new Date();
    return ((date.getDate() < 10) ? "0":"") + date.getDate() + "/" + (((date.getMonth() + 1) < 10) ? "0":"") + (date.getMonth() + 1) + "/" + date.getFullYear();
}

function pad(num, size) {
    var s = num + "";
    while (s.length < size) s = "0" + s;
    return s;
}

function toInt(str) {
	if (str.length < 1)
		return 0;
	
	return parseInt(str, 10);
}

function toFloat(str) {
	if (str.length < 1)
		return 0.0;
	
	return parseFloat(str, 10);
}

function validateInt(str, allowEmpty, allowZero, allowNegative) {
	if (str.length < 1) {
		if (allowEmpty)
			return true;
		else
			return false;
	}
	
	var f = parseInt(str, 10);
	
	if (Number.isNaN(f)) {
		return false;
	}
	
	if (f == 0.0 && !allowZero) {
		return false;
	}
	
	if (f < 0.0 && !allowNegative) {
		return false;
	}
	
	return true;
}

function validateFloat(str, allowEmpty, allowNegative) {
	if (str.length < 1) {
		if (allowEmpty)
			return true;
		else
			return false;
	}
	
	var f = parseFloat(str, 10);
	
	if (Number.isNaN(f)) {
		return false;
	}
	
	if (f == 0.0 && !allowEmpty) {
		return false;
	}
	
	if (f < 0.0 && !allowNegative) {
		return false;
	}
	
	return true;
}