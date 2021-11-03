$(document).ready(function() {
    var dateFormat = "yy-mm-dd",
        from = $( "#from" ).datepicker({
            defaultDate: "-5d",
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            maxDate: "0D",
            showAnim: "clip",
            dateFormat: "yy-mm-dd"
            })
            .on( "change", function() {
            to.datepicker( "option", "minDate", getDate( this ) );
            }),
        to = $( "#to" ).datepicker({
            defaultDate: "-1d",
            changeMonth: true,
            changeYear: true,
            numberOfMonths: 1,
            maxDate: "0D",
            showAnim: "clip",
            dateFormat: "yy-mm-dd"
        })
        .on( "change", function() {
            from.datepicker( "option", "maxDate", getDate( this ) );
        });
        function getDate( element ) {
        var date;
        try {
            date = $.datepicker.parseDate( dateFormat, element.value );
        } catch( error ) {
            date = null;
        }
        return date;
        }

    $("#all_topics").on("click", function() {
        $(".topics")
            .prop("checked", this.checked)
            .toggleClass("selected", this.checked)});
    $("#country")[0].selectedIndex = 0;
});
