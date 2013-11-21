function vocabularyTokenInputActivate(id, newValues, oldValues) {
  $('#'+id).tokenInput(newValues, {
      theme: "facebook",
      tokenDelimiter: "\n",
      tokenValue: "id",
      preventDuplicates: true,
      prePopulate: oldValues
  });

  $("#token-input-"+id).change(function(){
    var value = $(this).val().trim();
    $("#"+id).tokenInput("add", {id: value, name: value});
  });

  $(document).keypress(function(e) {
      if(e.keyCode == 13) {
        if($("#token-input-"+id).is(":focus")) {
          e.preventDefault();
          var value = $("#token-input-"+id).val().trim();
          $("#"+id).tokenInput("add", {id: value, name: value});
          return false;
        }
      }
  });
}

