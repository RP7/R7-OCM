/*
var xList = [];
for (var i = -500; i <=500; i++) {
  xList.push(i);
};
var Soption = {  
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

  var IQoption = {  
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
                          , restore: {show: true}
                          , saveAsImage: {show: true}
                }
            }
  , xAxis: {  type: 'value'
            , boundaryGap: false
            , min: -2048
            , max: 2048
            }
  , yAxis: {  type: 'value'
            , boundaryGap: false
            , min: -2048
            , max: 2048
            }
  , backgroundColor:'rgb(255, 255, 255)'
  , series: [
              {
                  name:'IQ'
                , type:'line'
                , symbol: 'none'
                , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
                , data : []
                }
            ]
  };

var initG = function() {
  $.getJSON('/data').done( function(data) {
              Soption.xAxis.data=data.freq;
              Soption.series[0].data=data.power;
              mySpectrum.setOption(Soption);
              var ss = [];
              for (var i = 0; i < data.i.length; i++) {
                ss.push([data.i[i],data.q[i]]);
              };
              IQoption.series[0].data = ss;
              myIQ.setOption(IQoption);
    });
};  
var newdata = function() {
            $.getJSON('/data').done( function(data) {
              var newoption = {
                  xAxis : {data:data.freq}
            		, series : [{ name:'Spectrum', data:data.power}]
            	};
            	mySpectrum.setOption(newoption);
              var ss = [];
              for (var i = 0; i < data.i.length; i++) {
                ss.push([data.i[i],data.q[i]]);
              };
              myIQ.setOption({series : [{ name:'IQ', data:data.power}]});
    });
  };
*/
var option = {
    title: {
        text: 'AD9361',
        x: 'center',
        y: 0
    },
    grid: [
        {x: '7%', y: '7%', width: '38%', height: '38%'},
        {x2: '7%', y: '7%', width: '38%', height: '38%'},
        {x: '7%', y2: '7%', width: '38%', height: '38%'},
        {x2: '7%', y2: '7%', width: '38%', height: '38%'}
    ],
    tooltip: {
        formatter: 'Group {a}: ({c})'
    },
    xAxis: [
        {gridIndex: 0, min: -500, max: 500},
        {gridIndex: 1, min: -2048, max: 2048},
        {gridIndex: 2, min: 0, max: 1920},
        {gridIndex: 3, min: 0, max: 1920}
    ],
    yAxis: [
        {gridIndex: 0, min: 70, max: 150},
        {gridIndex: 1, min: -2048, max: 2048},
        {gridIndex: 2, min: -2048, max: 2048},
        {gridIndex: 3, min: -2048, max: 2048}
    ],
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
        },
        {
            name: 'IQ',
            type: 'scatter',
            xAxisIndex: [1],
            yAxisIndex: [1],
            data: []
        },
        {
              name: 'I'
            , type: 'line'
            , smooth:true
            , symbol: 'none'
            , sampling: 'average'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , xAxisIndex: [2]
            , yAxisIndex: [2]
            , data: []
        },
        {
              name: 'Q'
            , type: 'line'
            , smooth:true
            , symbol: 'none'
            , sampling: 'average'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , xAxisIndex: [3]
            , yAxisIndex: [3]
            , data: []
        }
    ]
};

var genData = function(d) {
  var ss = [[],[],[],[]];
  for (var i = 0; i < d.freq.length; i++) {
    ss[0].push([d.freq[i],d.power[i]]);
  };
  for (var i = 0; i < d.i.length; i++) {
    ss[1].push([d.i[i],d.q[i]]);
    ss[2].push([i,d.i[i]]);
    ss[3].push([i,d.q[i]]);
  };
  return ss;
};

var initG = function() {
  $.getJSON('/data').done( function(data) {
              var ss = genData(data);
              for (var i = 0; i < 4; i++) {
                option.series[i].data = ss[i];
              };
              myChart.setOption(option);
    });
};  
var newdata = function() {
 $.getJSON('/data').done( function(data) {
   var ss = genData(data);
   var series = [
     {
          name: 'Spectrum'
        , data: ss[0]
     },
     {
          name: 'IQ'
        , data: ss[1]
     },
     {
          name: 'I'
        , data: ss[2]
     },
     {
          name: 'Q'
        , data: ss[3]
     }
   ];
   myChart.setOption({series:series});
  });
};