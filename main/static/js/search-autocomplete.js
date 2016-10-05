/**
 * Created by Aaron on 3/10/2016.
 */
$(document).ready(function() {
  $("#id_search").autocomplete({

    // gets the data from get_results in views.py
    source: '/search-autocomplete/',
    minLength: 2,

    // Goes to appropriate link on click through
    select: function (event, ui) {
      window.location.href=ui.item.url;
    },

  });
});
