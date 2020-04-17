var state = false;

function lightsToggle(this_ajax_token) {
	if(state==false){
		$("#btn_lights").removeClass('lightbulb icon').addClass('lightbulb outline icon');
		state = true;
        $.ajax({ url: "/control?token="+ this_ajax_token +"&lights=1", context: document.body	}).done(function() { $( this ).addClass( "done" );});
        console.log('here')
	}
	else if(state==true){
		$("#btn_lights").removeClass('lightbulb outline icon').addClass('lightbulb icon');
		state = false;
		$.ajax({ url: "/control?token="+ this_ajax_token +"&lights=0", context: document.body	}).done(function() { $( this ).addClass( "done" );});
	}
}

function ajax_cmd_resp(this_ajax_token, ajax_cmd){
    $.ajax({ url: "/control?token="+ this_ajax_token +"&move=" + ajax_cmd, context: document.body	}).done(function() { $( this ).addClass( "done" );});
};