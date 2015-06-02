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

function isValueSelected(value) {
	var filters = document.getElementsByName('check_box');

	for (var i = 0; i < filters.length; i++)
		if (filters[i].value == value && filters[i].checked)
			return true;

	return false;
}

function filter() {
	var filters = document.getElementsByName('check_box');

	for (var i = 0; i < filters.length; i++)
		processFilter(filters[i].value);
}

function isNothingSelected() {
	var filters = document.getElementsByName('check_box');

	for (var i = 0; i < filters.length; i++)
		if (filters[i].checked)
			return false;
	return true;
}

function processFilter(value) {
	var tableChildrens = $('#tbody_conteudo').children();

	for (var i = 0; i < tableChildrens.length; i++) {
		if (isNothingSelected())
			tableChildrens[i].style.display = "none"

		else
			for (var j = 0; j < tableChildrens.length; j++) {
				if (isValueSelected(tableChildrens[i].childNodes[tableChildrens[i].childNodes.length - 1].textContent))
					tableChildrens[i].style.display = "";
				else
					tableChildrens[i].style.display = "none"
			}
	}

}

function update() {
	pagina = document.URL.split("/")[document.URL.split("/").length - 2];
	switch (pagina) {
	case 'posts':
		document.getElementById('btn_posts').className = 'active';
		document.getElementById('btn_sobre').className = '';
		break;

	case 'sobre':
		document.getElementById('btn_sobre').className = 'active';
		document.getElementById('btn_posts').className = '';
		break;
	}
	updatePagina();
}
/*
 *  
 *function updatePagina() {
	regExp = new RegExp('page=[0-9]');
	if (document.URL.match(regExp)) {
		numeroPagina = document.URL.match(regExp)[0].split('=')[1];
		objetoPaginacao = document.getElementById('paginacao');
		childNodes = objetoPaginacao.childNodes;

		for (i = 0; i < childNodes.length; i++) {
			if (i + 1 != numeroPagina) {
				childNodes[i].className = '';
			} else {
				childNodes[i].className = 'active';
			}
		}

	} else {
		document.getElementById('paginacao').childNodes[0].className = 'active';
	}
}
 
 */

function showCommentsFromPost(link, postId, page) {
	$.ajax({
		type : "GET",
		url : "../" + link + "/",
		data : {
			ACCESS_TOKEN : authResponse,
			postId : postId,
			page : page
		},
		success : function(response) {
			$("#content").html(response);
		}
	});
}

function showNavbar() {
	var navbar = document.getElementById('navbar');

	if (navbar.className == 'collapse navbar-collapse in')
		navbar.className = 'collapse navbar-collapse';

	else
		navbar.className = 'collapse navbar-collapse in';
}

function showPosts(authResponse, page) {
	debugger;
	$.ajax({
		type : "GET",
		url : "../posts/",
		data : {
			ACCESS_TOKEN : authResponse,
			page : page
		},
		success : function(response) {
			$("#content").html(response);
		},
		error: function (request, status, error) {
	        $("#content").html();
	    }
	});
}

function showCommentsFromPosts(page, postId){
	debugger;
	$.ajax({
		type : "GET",
		url : "../comments/",
		data : {
			page : page,
			postId: postId
		},
		success : function(response) {
			$("#content").html(response);
		}
	});
}

function showAbout(){
	$.ajax({
		type : "GET",
		url : "../sobre/",
		success : function(response) {
			$("#content").html(response);
		},		
	});
}

