
var option = {
    title: {
        text: 'Spectrum',
        x: 'center',
        y: 0
    },
    xAxis: {
            type: 'value'
          , data: []
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
              name: ''
            , type: 'line'
            , smooth:false
            , symbol: 'none'
            , sampling: 'average'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , data: []
        }
    ]
};

var load = function() {
    spectrum.setOption(option);
    $.getJSON('/scan?s=800e6&e=980e6').done( function(data) {
    var ss = data.data;
    var series = [
     {
          name: 'Spectrum'
        , data: ss
     }
   ];
   spectrum.setOption({series:series});
    });
};


