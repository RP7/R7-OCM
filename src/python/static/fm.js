var xList = [];
for (var i = -1024; i <=1023; i++) {
  xList.push(i);
};
var fmoption = {
    title: {
        text: 'FM',
        x: 'center',
        y: 0
    },
    xAxis: {
          type: 'category'
        , data: xList  
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

