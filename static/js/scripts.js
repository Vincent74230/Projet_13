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


var departements = {
    Toute:[
    "Departements", 
    "Ain", 
    "Aisne", 
    "Allier",
    "Alpes-de-Haute-Provence",
    "Hautes-Alpes",
    "Alpes-Maritimes",
    "Ardèche",
    "Ardennes",
    "Ariège",
    "Aube",
    "Aude",
    "Aveyron",
    "Bouches-du-Rhône",
    "Calvados",
    "Cantal",
    "Charente",
    "Charente-Maritime",
    "Cher",
    "Corrèze",
    "Corse-du-Sud",
    "Haute-Corse",
    "Côte-d'Or",
    "Côtes d'Armor",
    "Creuse",
    "Dordogne",
    "Doubs",
    "Drôme",
    "Eure",
    "Eure-et-Loir",
    "Finistère",
    "Gard",
    "Haute-Garonne",
    "Gers",
    "Gironde",
    "Hérault",
    "Ille-et-Vilaine",
    "Indre",
    "Indre-et-Loire",
    "Isère",
    "Jura",
    "Landes",
    "Loir-et-Cher",
    "Loire",
    "Haute-Loire",
    "Loire-Atlantique",
    "Loiret",
    "Lot",
    "Lot-et-Garonne",
    "Lozère",
    "Maine-et-Loire",
    "Manche",
    "Marne",
    "Haute-Marne",
    "Mayenne",
    "Meurthe-et-Moselle",
    "Meuse",
    "Morbihan",
    "Moselle",
    "Nièvre",
    "Nord",
    "Oise",
    "Orne",
    "Pas-de-Calais",
    "Puy-de-Dôme",
    "Pyrénées-Atlantiques",
    "Hautes-Pyrénées",
    "Pyrénées-Orientales",
    "Bas-Rhin",
    "Haut-Rhin",
    "Rhône",
    "Haute-Saône",
    "Saône-et-Loire",
    "Sarthe",
    "Savoie",
    "Haute-Savoie",
    "Paris",
    "Seine-Maritime",
    "Seine-et-Marne",
    "Yvelines",
    "Deux-Sèvres",
    "Somme",
    "Tarn",
    "Tarn-et-Garonne",
    "Var",
    "Vaucluse",
    "Vendée",
    "Vienne",
    "Haute-Vienne",
    "Vosges",
    "Yonne",
    "Territoire de Belfort",
    "Essonne",
    "Hauts-de-Seine",
    "Seine-St-Denis",
    "Val-de-Marne",
    "Val-D'Oise",
    "Guadeloupe",
    "Martinique",
    "Guyane",
    "La Réunion",
    "Mayotte"
    ],
    auvergne:[
    "Ain",
    "Allier",
    "Ardèche",
    "Cantal",
    "Drôme",
    "Haute-Loire",
    "Haute-Savoie",
    "Isère",
    "Loire",
    "Puy-de-Dôme",
    "Rhône",
    "Savoie"
    ],
    bourgogne:[
    "Côte-d'Or",
    "Doubs",
    "Haute-Saône",
    "Jura",
    "Nièvre",
    "Saône-et-Loire",
    "Territoire de Belfort",
    "Yonne"
    ],
    bretagne:[
    "Côtes d'Armor",
    "Finistère",
    "Ille-et-Vilaine",
    "Morbihan"
    ],
    centre:[
    "Cher",
    "Eure-et-Loir",
    "Indre",
    "Indre-et-Loire",
    "Loir-et-Cher",
    "Loiret"
    ],
    corse:[
    "Corse-du-Sud",
    "Haute-Corse"
    ],
    grandest:[
    "Ardennes",
    "Aube",
    "Bas-Rhin",
    "Haut-Rhin",
    "Haute-Marne",
    "Marne",
    "Meurthe-et-Moselle",
    "Meuse",
    "Moselle",
    "Vosges"
    ],
    guadeloupe:[
    "Guadeloupe"
    ],
    guyanne:[
    "Guyane",
    ],
    hautsdefrance:[
    "Aisne",
    "Nord",
    "Oise",
    "Pas-de-Calais",
    "Somme"
    ],
    iledefrance:[
    "Essonne",
    "Hauts-de-Seine",
    "Paris",
    "Seine-et-Marne",
    "Seine-St-Denis",
    "Val-D'Oise",
    "Val-de-Marne",
    "Yvelines"
    ],
    martinique:[
    "Martinique"
    ],
    mayotte:[
    "Mayotte"
    ],
    normandie:[
    "Calvados",
    "Eure",
    "Manche",
    "Orne",
    "Seine-Maritime"
    ],
    nouvelleaquitaine:[
    "Charente",
    "Charente-Maritime",
    "Corrèze",
    "Creuse",
    "Deux-Sèvres",
    "Dordogne",
    "Gironde",
    "Haute-Vienne",
    "Landes",
    "Lot-et-Garonne",
    "Pyrénées-Atlantiques",
    "Vienne"
    ],
    occitanie:[
    "Ariège",
    "Aude",
    "Aveyron",
    "Gard",
    "Gers",
    "Haute-Garonne",
    "Hautes-Pyrénées",
    "Hérault",
    "Lot",
    "Lozère",
    "Pyrénées-Orientales",
    "Tarn",
    "Tarn-et-Garonne"
    ],
    paysdelaloire:[
    "Loire-Atlantique",
    "Maine-et-Loire",
    "Mayenne",
    "Sarthe",
    "Vendée"
    ],
    paca:[
    "Alpes-de-Haute-Provence",
    "Alpes-Maritimes",
    "Bouches-du-Rhône",
    "Hautes-Alpes",
    "Var",
    "Vaucluse"
    ],
    reunion:[
    "La Réunion"
    ]
}

var region=document.getElementById('region-menu');
var departement=document.getElementById('departement-menu');


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
