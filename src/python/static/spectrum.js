
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
  , xAxis: {  type: 'value'
  					, boundaryGap: false
  					, min: -500
  					, max: 500
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
  

var newdata = function(myChart) {
            $.getJSON('/data').done( function(data) {
              var ss = [];
              for (var i = 0; i < data.freq.length; i++) {
                ss.push([data.freq[i],data.power[i]]);
              };
            	var newoption = {
            		  series : [{ name:'Spectrum', data:ss}]
            	};
            	myChart.setOption(newoption);
    });
  };
    