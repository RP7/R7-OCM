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
        if(fifo.length<163840)
            fifo = fifo.concat(data.data);
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
var bufferSize = 4096;
var myPCMProcessingNode = audioContext.createScriptProcessor(bufferSize, 1, 1);
myPCMProcessingNode.connect(audioContext.destination); 
myPCMProcessingNode.onaudioprocess = function(e) {    
    var output = e.outputBuffer.getChannelData(0);    
    for (var i = 0; i < bufferSize; i++) 
    {     
        if( fifo.length>0 )
            output[i] = fifo.shift();
        else
            break;  
    }
}

FMdata();   
setInterval(FMdata, 2000);
