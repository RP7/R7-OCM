
var option = {
    title: {
        text: 'Spectrum',
        x: 'center',
        y: 0
    },
    toolbox: {
        show : true,
        feature : {
            dataZoom : {show: true},
            dataView : {show: true},
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
          , scale:true
          , min:900000000
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
    //,
    //backgroundColor: rgba(52, 52, 52, 0.5)
};
var sData = {};
var updateSData = function(d) {
  for( var i=0;i<d.length;i++ ){
    a= d[i];
    sData[a[0]]=a[1];
  }
};
var buildData = function(){
  var ret = [];
  for ( var s in sData ){
    ret.push([s,sData[s]]);
  }
  return ret;
};

var load = function() {
    spectrum.setOption(option);
    $.getJSON('/scan?s=900e6&e=1000e6').done( function(data) {
    updateSData(data.data);
    var series = [
     {
          name: 'Spectrum'
        , data: buildData()
     }
   ];
   spectrum.setOption({series:series});
   //setTimeout(update, 5000);
    });
};

var update = function() {
    var values = $("#slider1").slider("values");
    var diff = (values[1]-values[0])
    o=spectrum.getOption()
    s = o.dataZoom[0].start*diff/100.+values[0];
    s = Math.round(s/10)*10;
    e = o.dataZoom[0].end*diff/100.+values[0];
    e = Math.round(e/10)*10+10;
    url = '/scan?s='+s+'e6&e='+e+'e6';
    $.getJSON(url).done( function(data) {
    updateSData(data.data);
    var series = [
     {
          name: 'Spectrum'
        , data: buildData()
     }
   ];
   var values = $("#slider1").slider("values");
   var xAxis = {   type: 'value'
          , data: []
          , min:values[0]*1e6
          , max:values[1]*1e6
   };
   spectrum.setOption({xAxis:xAxis,series:series});
    });
};


