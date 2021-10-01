$(document).ready(function() {
    $( "#datepicker" ).datepicker({showAnim: "clip", dateFormat: "yy-mm-dd"});
    $("#all_topics").on("click", function() {
        $(".topics")
            .prop("checked", this.checked)
            .toggleClass("selected", this.checked)});
    $("#country")[0].selectedIndex = 0;

    var chart = {
        plotBackgroundColor: null,
        plotBorderWidth: null,
        plotShadow: false
    };
    var title = {
        {% if valid_results %}
        {% for data in valid_results %}
        text: 'Number of News articles by topic for {{ data.country}}, {{data.date}}
        {% endfor %}
        {% else %}
        text: 'Number of News articles by topic for Place, Date'   
        {% endif %}
    };
    var tooltip = {
        pointFormat: '{series.name}: <b>{point.percentage:.1f}%</b>'
    };
    var plotOptions = {
        pie: {
            allowPointSelect: true,
            cursor: 'pointer',
            
            dataLabels: {
                enabled: true,
                format: '<b>{point.name}%</b>: {point.percentage:.1f} %',
                style: {
                color: (Highcharts.theme && Highcharts.theme.contrastTextColor)||
                'black'
                }
            }
        }
    };
    var series = [{
        type: 'pie',
        name: 'Article share',
        data: [
            {% if pie_chart_results %}
            {% for results in pie_chart_results %}
            ['{{key}}',   {{value}}],
            {% endfor %}
            {% else %}
            ['Topic1',   47],
            ['Topic2',       20],
            ['Keyword',    33],
            {% endif %}
        
        ]
    }];
    var json = {};   
    json.chart = chart; 
    json.title = title;     
    json.tooltip = tooltip;  
    json.series = series;
    json.plotOptions = plotOptions;
    $('#output_display').highcharts(json);  
    });