var xList = [];
for (var i = -500; i <=500; i++) {
  xList.push(i);
};
var option = {  
    tooltip: {  trigger: 'axis'
              , position: function (pt) {
                return [pt[0], '10%'];
                }
              }
  , title: {  left: 'center'
            , text: 'Spectrum'
            }
  , legend: { top: 'bottom'
            , data:['power']
            }
  , toolbox: {  show: true
              , feature: {  dataView: {show: true, readOnly: false}
                          , magicType: {show: true, type: ['line', 'bar', 'stack', 'tiled']}
                          , restore: {show: true}
                          , saveAsImage: {show: true}
                }
            }
  , xAxis: {  type: 'category'
            , boundaryGap: false
            , data: []
            }
  , yAxis: {  type: 'value'
            , boundaryGap: [0, '100%']
            , min: 70
            , max: 120
            }
  , dataZoom: [
                {   type: 'inside'
                  , start: 0
                  , end: 100
                }
              , {   start: 0
                  , end: 100
                }
              ]
  , backgroundColor:'rgb(255, 255, 255)'
  , series: [
              {
                  name:'Spectrum'
                , type:'line'
                , smooth:true
                , symbol: 'none'
                , sampling: 'average'
                , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
                , areaStyle: {
                        normal: {
                            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, 
                              [{  offset: 0
                                , color: 'rgb(158, 255, 68)' }
                              ,{  offset: 1
                                , color: 'rgb(70, 255, 131)' }
                              ]) } }
                , data : []
                }
            ]
  };
var initG = function() {
  $.getJSON('/data').done( function(data) {
              option.xAxis.data=data.freq;
              option.series[0].data=data.power;
              myChart.setOption(option);
    });
};  
var newdata = function() {
            $.getJSON('/data').done( function(data) {
              var newoption = {
                  xAxis : {data:data.freq}
            		, series : [{ name:'Spectrum', data:data.power}]
            	};
            	myChart.setOption(newoption);
    });
  };
    