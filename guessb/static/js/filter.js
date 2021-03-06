timer = undefined;

function updateStatusButtonGroup(element) {
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
	$.ajax({
		type : "GET",
		url : "../posts/",
		data : {
			ACCESS_TOKEN : authResponse,
			page : page
		},beforeSend: function(){
			progressBar();			
		},
		success : function(response) {
			$("#content").html(response);
			finishWidthProgressBar();
		},
		error: function (request, status, error) {
	        finishWidthProgressBar();
	    }
	});
}

function showPostsPerNumber(authResponse, page, totalNumberPosts) {
	$.ajax({
		type : "GET",
		url : "../posts/",
		data : {
			ACCESS_TOKEN : authResponse,
			page : page, 
			totalNumberPosts : totalNumberPosts
		},beforeSend: function(){
			progressBar();			
		},
		success : function(response) {
			$("#content").html(response);
			finishWidthProgressBar();
		},
		error: function (request, status, error) {
	        finishWidthProgressBar();
	    }
	});
}


function showCommentsFromPosts(page, postId, numberPageFromPost){
	$.ajax({
		type : "GET",
		url : "../comments/",
		data : {
			page : page,
			postId: postId,
			numberPageFromPost : numberPageFromPost
		},
		beforeSend: function(){
			progressBar();
		},
		success : function(response) {
			$("#content").html(response);
			finishWidthProgressBar();
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
	
function progressBar(){
	document.getElementsByClassName('progress-bar progress-bar-success progress-bar-striped active')[0].style.width="35%"
	$('.loader').fadeIn(1500);	
	updateWidthProgressBar();
}

function updateWidthProgressBar(){
	var width = parseInt(document.getElementsByClassName('progress-bar progress-bar-success progress-bar-striped active')[0].style.width.replace('%',''))+10;
	document.getElementsByClassName('progress-bar progress-bar-success progress-bar-striped active')[0].style.width=width+"%";
}

function finishWidthProgressBar(){
	$('.loader').fadeOut(1500);
	document.getElementsByClassName('progress-bar progress-bar-success progress-bar-striped active')[0].style.width="100%";
	clearTimeout(timer);
	timer = undefined;
}

function showAnotherHome(){
	var param = document.getElementById('accessTokenInput').value;
	showPosts(param, 1);
}
	
