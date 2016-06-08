var fmoption = {
    title: {
        text: 'FM',
        x: 'center',
        y: 0
    },
    xAxis: {
          type: 'value'
        , min: -512
        , max: 511
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
              name: 'Spectrum'
            , type: 'line'
            , smooth:true
            , symbol: 'none'
            , sampling: 'average'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , xAxisIndex: [0]
            , yAxisIndex: [0]
            , data: []
        }
    ]
};

var FMdata = function() {
    $.getJSON('/FM?data').done( function(data) {
              fmoption.series[0].data = data.data;
              fmSpectrum.setOption(fmoption);
    });
};

