///THIS FILE MUST BE IMPORTED BEFORE THE "main" FILE.
/**
  Executes a search for colors containing a substring.
 */
var processSearch = function()  {
  //The key-press listener is no longer attached

  //Get and trim the search text.
  // Ich bin mir ziemlich sicher, das trim und toLowerCase unnöting sind, da dies
  // Aktionen bereits in der views.py ausgeführt werden
  var searchText = $('#search').val().trim().toLowerCase();

  if(searchText.length < MIN_SEARCH_CHARS)  {
    //Too short. Ignore the submission, and erase any current results.
    $('#search_results').html("");

  }  else  {
    //There are at least two characters. Execute the search.

    var processServerResponse = function(sersverResponse_data, textStatus_ignored,
                        jqXHR_ignored)  {
      //alert("sersverResponse_data='" + sersverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "'");
      $('#search_results').html(sersverResponse_data);
    }

    var config = {
      /*
        Using GET allows you to directly call the search page in
        the browser:

        http://the.url/search/?search=bl

        Also, GET-s do not require the csrf_token
       */
      type: "GET",
      url: SUBMIT_URL,
      data: {
        'search' : searchText,
      },
      dataType: 'html',
      success: processServerResponse
    };
    $.ajax(config);
  }
};
