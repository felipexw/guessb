var aFiltros = [ 'neu', 'pos', 'neg' ];

function containsValue(value) {
	for (var i = 0; i < aFiltros.length; i++) {
		if (value == aFiltros[i])
			return true;
	}
	return false;
}

function addUniqueValue(value) {
	if (!containsValue(value))
		aFiltros.push(value);
	else
		aFiltros.splice(aFiltros.indexOf(value), 1);
}

function filtrar(radio) {
	var filhosTabela = $('#tbody_conteudo').children();
	debugger;
	addUniqueValue(radio.value);

	for (var i = 0; i < filhosTabela.length; i++) {
		for (var j = 0; j < aFiltros.length; j++) {
			if (containsValue(filhosTabela[i].childNodes[2].textContent))
				filhosTabela[i].className = 'mostrar';
			else
				filhosTabela[i].className = 'ocultar';
		}
	}
	$('.ocultar').hide();
	$('.mostrar').show();
}
