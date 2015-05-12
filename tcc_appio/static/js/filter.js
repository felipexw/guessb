function showFilters(element) {
	if (element.className == 'btn-group open')
		element.className = 'btn-group';
	else
		element.className = 'btn-group open';
}

function containsValue(value) {
	for (var i = 0; i < filtersValues.length; i++) {
		if (value == filtersValues[i])
			return true;
	}
	return false;
}

function isValueSelected(value){
	var filters = document.getElementsByName('check_box');
	
	for(var i = 0; i < filters.length; i++)
		if (filters[i].value == value && filters[i].checked)
			return true;
	
	return false;
}

function filter(){
	var filters = document.getElementsByName('check_box');
	
	for(var i = 0; i < filters.length; i++)
		processFilter(filters[i].value);	
}

function isNothingSelected(){
	var filters = document.getElementsByName('check_box');
	
	for(var i = 0; i < filters.length; i++)
		if (filters[i].checked)
			return false;
	return true;
}

function processFilter(value){
	var tableChildrens = $('#tbody_conteudo').children();

	for (var i = 0; i < tableChildrens.length; i++) {
		if (isNothingSelected())
			tableChildrens[i].style.display="none"

		else
			for (var j = 0; j < tableChildrens.length; j++) {
				if (isValueSelected(tableChildrens[i].childNodes[tableChildrens[i].childNodes.length-1].textContent))
					tableChildrens[i].style.display = "";
				else
					tableChildrens[i].style.display = "none"
			}
	}

}
