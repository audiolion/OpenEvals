/**
 * Created by Aaron on 3/10/2016.
 */
$(function() {
  $("#id_search").autocomplete({
    source: '/search-autocomplete/',
    minLength: 2,
  });
});
