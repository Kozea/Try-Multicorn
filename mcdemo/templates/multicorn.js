jQuery(document).ready(function(){
  var multicorn_console = jQuery('#console');
  var controller = multicorn_console.console({
    promptLabel: 'multicorn> ',
    continuedPromptLable : '> ',
    commandValidate: function(line){
      if ( line[line.length - 1] == ';'){
        this.continuedPrompt = false;
      } else {
        this.continuedPrompt = true;
      }
      return true;
    },
    commandHandle: function(line, report){
      jQuery.ajax({
        url: "{{ url_for('send_query') }}",
        data: {'query': line},
        type: 'post',
        success: function(data){
            console.log(data.result);
            report(data.result);
        },
        error: function(){
            report("An unexpected error occured");
        }
      });
    },
    autofocus: true,
    animateScroll: true,
    promptHistory: true,
  });
});
