
var option = {
    title: {
        text: 'Spectrum',
        x: 'center',
        y: 0
    },
    toolbox: {
        show : true,
        feature : {
            mark : {show: true},
            dataZoom : {show: true},
            dataView : {show: true},
            magicType : {show: true, type: ['line', 'bar']},
            restore : {show: true},
            saveAsImage : {show: true}
        }
    },
    dataZoom : {
        show : true,
        realtime : true,
        //orient: 'vertical',   // 'horizontal'
        //x: 0,
        y: 36,
        //width: 400,
        height: 20,
        //backgroundColor: 'rgba(221,160,221,0.5)',
        //dataBackgroundColor: 'rgba(138,43,226,0.5)',
        //fillerColor: 'rgba(38,143,26,0.6)',
        //handleColor: 'rgba(128,43,16,0.8)',
        //xAxisIndex:[],
        //yAxisIndex:[],
        start : 40,
        end : 60
    },
    xAxis: {
            type: 'value'
          , data: []
          , min:600000000
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
    $.getJSON('/scan?s=900e6&e=1000e6').done( function(data) {
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
    $.getJSON('/scan?s=900e6&e=1000e6').done( function(data) {
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


