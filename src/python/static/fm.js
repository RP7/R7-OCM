
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
              name: 'time series'
            , type: 'line'
            , smooth:false
            , symbol: 'none'
            , sampling: 'average'
            , itemStyle: { normal: { color: 'rgb(70, 255, 131)' }}
            , data: []
        }
    ]
};

function js_queue(){
    this.arr = new Array();
    this.pos = 0;
};

js_queue.prototype.put = function(obj){
    this.arr.push(obj);
};

js_queue.prototype.remove = function(){
    this.arr.shift();
    this.pos = 0;
}

js_queue.prototype.header = function()
{
    if( this.arr.length==0 )
        return null;
    else
        return this.arr[0];
};

js_queue.prototype.getPos = function()
{
    return this.pos;
};

js_queue.prototype.setPos = function( pos )
{
    this.pos = pos;
};

var xList = [];
var time_s = 0.;

var octet2int16 = function(s)
{
  var buffer = new ArrayBuffer(s.length);
  var view = new DataView(buffer);
  for(var i=0, n=s.length; i<n; i++) 
    view.setUint8(i,s.charCodeAt(i));
  var v3 = new Int16Array(buffer);
  return v3;
}

var fifo = new js_queue();

var fmload = function() {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', '/FM?data', true);
    xhr.responseType = 'arraybuffer';
     
    xhr.onload = function(e) {
      if (this.status == 200) {
        // get binary data as a response
        var buffer = this.response;
        fifo.put(buffer);
      }
    };
    xhr.send();
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
    setBuffer(output,0,bufferSize);
    
};

var setBuffer = function(o,s,l) {

    var pos = fifo.getPos();
    var data = fifo.header();
    var dataview = new DataView(data,pos*4);
    var part1 = 0;
    var part2 = 0;
    if(data==null)
        return;
    if(l>dataview.byteLength/4)
    {
        part1 = dataview.byteLength/4;
        part2 = l - dataview.byteLength/4;
    }
    else
    {
        part1 = l;
        part2 = 0;
    }
    for(var i=0;i<part1;i++) {
        o[s+i] = dataview.getFloat32(i*4,littleEndian=true);
    }
    if(part1==dataview.byteLength/4)
    {
        fifo.remove();
    }
    else
    {
        fifo.setPos(pos+part1);
    }
    if(part2!=0)
    {
        setBuffer(o,s+part1,part2);
    }
};

setInterval(fmload, 2000);
