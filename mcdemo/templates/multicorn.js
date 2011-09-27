$(document).ready(function(){
  setupForm();
  setupConsole();
});


function setupForm(){
  /* Remove fieldset from the dom, and append them in the dictionary */
  var fieldset_map = {};
  $('#options_panel fieldset').each(function(){
    var elem = $(this);
    fieldset_map[this.id.replace('fieldset_', '')] = this;
    elem.remove();
  });
  /* Setup the form submit event listener */
  $('#create_table_form').submit(function(){
    var table_type = $('select#table_type').val();
    var data = {}
    data.name = $('#table_name').val();
    if(table_type && table_type != ''){
      /* Collect options */
      data.table_type = table_type;
      var inputSelector = '#fieldset_' + table_type + ' input';
      data.options  = {}
      $(inputSelector).each(function(){
        var elem = $(this);
        return data.options[$.attr(this, 'data-option-name')] =  elem.val();
      });
      data.columns = []
      $('#columns_panel fieldset').each(function(){
          var name = $('input', $(this)).val();
          var type = $('select', $(this)).val();
          data.columns.push({name: name, type:type});
      });
    }
    $.ajax({
      url: "{{url_for('add_table')}}",
      data: JSON.stringify(data),
      type: 'post',
      contentType: 'application/json',
      success: function(data){
        console.log(data);
      },
      error: function(){
        alert("An error occurred");
      }
    });
    return false;
  });

  /* Setup the combobox to display the appropriate fieldset */
  $('select#table_type').change(function(){
    $(fieldset_map[$(this).data('oldvalue')]).remove();
    $('#options_panel').append(fieldset_map[$(this).val()]);
    $(this).data('oldvalue', $(this).val())
  });

  $('#columns_panel').multiInput({});

}

function setupConsole(){
  var multicorn_console = $('#console');
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
      $.ajax({
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
}
