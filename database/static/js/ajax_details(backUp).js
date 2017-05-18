//THIS FILE MUST BE IMPORTED BEFORE THE "main" FILE.

/**
   Executes a like click. Triggered by clicks on the various yes/no links.
 */
var processDetails = function()  {

   //In this scope, "this" is the button just clicked on.
   //The "this" in processServerResponse is *not* the button just clicked
   //on.
   var $brand_just_clicked_on = $(this);

   //The value of the "data-brand_id" attribute.
   var brand_id = $brand_just_clicked_on.data('brand_id');

   var processServerResponse = function(sersverResponse_data, textStatus_ignored,
                            jqXHR_ignored)  {
      //alert("sf sersverResponse_data='" + sersverResponse_data + "', textStatus_ignored='" + textStatus_ignored + "', jqXHR_ignored='" + jqXHR_ignored + "', brand_id='" + brand_id + "'");
      $('#Detailansicht' + brand_id).html(sersverResponse_data);
   }

   var config = {
      url: LIKE_URL_PRE_ID + brand_id + '/',
      dataType: 'html',
      success: processServerResponse
      //Should also have a "fail" call as well.
   };
   $.ajax(config);
};
