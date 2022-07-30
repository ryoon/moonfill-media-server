/* Use jQuery.ajax */
'use strict';

let videoElement = document.getElementById('myMovie')
let filepath = document.getElementById('movie-name').innerHTML;

function saveProgress()
{

  var progress = videoElement.currentTime;
  console.log(progress);

  var lastseenOption = {
    hour12: false
  };
  var timezone = {
    timeZone: 'Asia/Tokyo'
  };
  var lastseen = new Date().toLocaleString(timezone, lastseenOption);
  console.log(lastseen);

  $.ajax('/v1/saveProgress',
    {
      type: 'put',
      data: {
        filepath: filepath,
        user: 'ryoon', // FIXME
        progress: progress,
        lastseen: lastseen
      }
    }
  )
}


function initProgress(event) {
  $.ajax('/v1/getProgress',
    {
      type: 'get',
      data: {
        filepath: filepath,
        userid: 'ryoon', // FIXME
      }
    }
  ).done(function(data) {
    console.log('data');
    console.log(data);
    var progress = 0;
    if (data != undefined) {
      progress = data;
      videoElement.currentTime = progress;
    }
    videoElement.removeEventListener('play', initProgress);
    //window.setInterval(saveProgress, 10000);
  });
};

videoElement.onplay = initProgress;
videoElement.onpause = saveProgress;
videoElement.onseeked = saveProgress;
window.onunload = saveProgress;
