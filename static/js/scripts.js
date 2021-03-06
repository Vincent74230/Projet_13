/*!
    * Start Bootstrap - Agency v6.0.3 (https://startbootstrap.com/theme/agency)
    * Copyright 2013-2020 Start Bootstrap
    * Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-agency/blob/master/LICENSE)
    */
    (function ($) {
    "use strict"; // Start of use strict

    // Smooth scrolling using jQuery easing
    $('a.js-scroll-trigger[href*="#"]:not([href="#"])').click(function () {
        if (
            location.pathname.replace(/^\//, "") ==
                this.pathname.replace(/^\//, "") &&
            location.hostname == this.hostname
        ) {
            var target = $(this.hash);
            target = target.length
                ? target
                : $("[name=" + this.hash.slice(1) + "]");
            if (target.length) {
                $("html, body").animate(
                    {
                        scrollTop: target.offset().top - 72,
                    },
                    1000,
                    "easeInOutExpo"
                );
                return false;
            }
        }
    });

    // Closes responsive menu when a scroll trigger link is clicked
    $(".js-scroll-trigger").click(function () {
        $(".navbar-collapse").collapse("hide");
    });

    // Activate scrollspy to add active class to navbar items on scroll
    $("body").scrollspy({
        target: "#mainNav",
        offset: 74,
    });

    // Collapse Navbar
    var navbarCollapse = function () {
        if ($("#mainNav").offset().top > 100) {
            $("#mainNav").addClass("navbar-shrink");
        } else {
            $("#mainNav").removeClass("navbar-shrink");
        }
    };
    // Collapse now if page is not at top
    navbarCollapse();
    // Collapse the navbar when page is scrolled
    $(window).scroll(navbarCollapse);
})(jQuery); // End of use strict

// Customization by https://github.com/Vincent74230


var departements = JSON.parse(document.getElementById('departements_dict').textContent);
var region=document.getElementById('region-menu');
var departement=document.getElementById('departement-menu');

var selected_region=departements[region.value];
Array.from(selected_region).forEach(function(el){
let option = new Option(el, el);
departement.appendChild(option);
});

var dep_choice_pos = document.querySelector('#dep_choice_position');
document.getElementById('departement-menu').value=(departements[region.value][dep_choice_pos.dataset.value]);

region.addEventListener('change',function(){

    var selected_region=departements[this.value];

    while(departement.options.length > 0){
        departement.options.remove(0);
    }

    Array.from(selected_region).forEach(function(el){
    let option = new Option(el, el);
    departement.appendChild(option);
});
});


var cat_choice = document.getElementById('category');
var sel_cat = document.getElementsByClassName('selected_category');
for (var x=0; x<sel_cat.length; x++){
    if (sel_cat[x].dataset.value != cat_choice.dataset.value){
        sel_cat[x].style.display='none';
    };
}
