
var option = {
    title: {
        text: 'Spectrum',
        x: 'center',
        y: 0
    },
    xAxis: {
            type: 'value'
          , data: []
          , min:930000000
    },
    yAxis: {
          type: 'value'
        , boundaryGap: [0, '100%']
        , min:0
        , max:100
            
    },
    series: [
        {
              name: ''
            , type: 'line'
            , smooth:false
            , symbol: 'none'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , data: []
        }
    ]
};

var load = function() {
    spectrum.setOption(option);
    $.getJSON('/scan?s=930e6&e=960e6').done( function(data) {
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

var update = function() {
    $.getJSON('/scan?s=930e6&e=960e6').done( function(data) {
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


