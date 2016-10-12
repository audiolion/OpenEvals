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


  $(".toggle").click(function(){
    $(".form").toggle(250);
  });


    $(".btn-main-search").click(function(){
        $(".search-bar-hide").fadeIn(1000);
        $(".btn-main-search-x").fadeIn(1000);
        $(".btn-main-search").hide();

    });

  $(".btn-main-search-x").click(function(){
        $(".btn-main-search-x").hide();
        $(".search-bar-hide").hide();
        $(".btn-main-search").fadeIn(1000);
    });

});

