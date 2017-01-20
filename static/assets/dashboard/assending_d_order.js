function accordionTable(i,elem) {
    var table = $(elem),
        tbody = table.find('tbody'),
        th_index = 0,
        th_sortType = "string";

    //accordion on tbody > tr
    tbody.find('tr:first').addClass('table-acc-header');
    tbody.find('tr:last').addClass('table-acc-body');
    $('.table-acc-header').click(function() {
        table.find('.table-acc-body').addClass('collapse');
        $(this).next('.table-acc-body').removeClass('collapse');
    });

    function mapTDs(i, elem){
        var txt = $("td", elem).eq(th_index).text();
        $(elem).attr("data-sortval", txt);
    }
    function sortAsc(a, b){
        var aData = $(a).attr("data-sortval"),
            bData = $(b).attr("data-sortval");
        if(th_sortType==="int"){
            return +bData < +aData ? 1 : -1; // Integer
        }else{
            return  bData <  aData ? 1 : -1; // String or else
        }
    }

    //header sort
    table.on("click", "th", function() {
        th_sortType = $(this).data('sort');
        th_index = $(this).index();
        tbody = table.find('tbody').each(mapTDs);
        tbody.sort(sortAsc).detach().appendTo(table);
    });
}

$('.jAccordionTable').each(accordionTable);
