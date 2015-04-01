function getComentarios() {
	$.ajax({
		url : 'comentarios',
		data: 
		success : function() {
			console.log('AJAKESSSS FUNFOU')
		},
		type : "GET"
	})
}