
var fmoption = {
    title: {
        text: 'FM',
        x: 'center',
        y: 0
    },
    xAxis: {
          type: 'category'
        , data: []  
    },
    yAxis: {
        type: 'value'
    },
    series: [
        {
              name: 'Spectrum'
            , type: 'line'
            , smooth:false
            , symbol: 'none'
            , sampling: 'average'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , data: []
        }
    ]
};

var fifo = Array();

var FMdata = function() {
    $.getJSON('/FM?data').done( function(data) {
        xList = []
        console.log(fifo.lenght);
                
        {
            for (var i = 0; i < data.data.length; i++) {
                xList.push(i);
                data.data[i] = data.data[i]/32767.;
                if(fifo.length<4800000)
                {
                    fifo.push(data.data[i]);
                }
            }
        }
        fmoption.xAxis.xList = xList; 
        fmoption.series[0].data = data.data;
        fmSpectrum.setOption(fmoption);
    });
};

function myPCMSource() {
     return Math.random() * 2 - 3;
    }
    
var audioContext;
try {    window.AudioContext = window.AudioContext || window.webkitAudioContext;    
        audioContext = new AudioContext();
    } 
    catch(e) {    
        alert('Web Audio API is not supported in this browser');
    }
var bufferSize = 16384;
var myPCMProcessingNode = audioContext.createScriptProcessor(bufferSize, 1, 1);
myPCMProcessingNode.connect(audioContext.destination); 
myPCMProcessingNode.onaudioprocess = function(e) {    
    var output = e.outputBuffer.getChannelData(0);    
    for (var i = 0; i < bufferSize; i++) 
    {     
        if( fifo.length>0 )
            output[i] = fifo.shift();
        else
            output[i] = 0.;  
    }
}

FMdata();   
setInterval(FMdata, 2000);
