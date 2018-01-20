// Grab elements, create settings, etc.
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');

// Get access to the camera!
if(navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    // Not adding `{ audio: true }` since we only want video now
    navigator.mediaDevices.getUserMedia({ video: true }).then(function(stream) {
        video.src = window.URL.createObjectURL(stream);
        video.play();
    });
}

// Trigger photo take
// document.getElementById("snap").addEventListener("click", function() {
// 	context.drawImage(video, 0, 0, 640, 480);
// });

// Add touch event listeners and prevent right click menu
video.addEventListener("touchstart", touchStart, false);
video.addEventListener("touchend", touchEnd, false);
video.addEventListener('contextmenu', (e) => {
    e.preventDefault();
    return false;
});

// Timers for hold trigger
var timer;
var holdTime = 500;

// On touch, start hold timer
function touchStart(e) {
    timer = setTimeout(function() {onHold(e);}, holdTime); 
}

// On remove, clear hold timer
function touchEnd(e) {
    if (timer)
        clearTimeout(timer);
}

// Hold timer triggers coordinate log
function onHold(e) {
    console.log(e.touches[0].clientX, e.touches[0].clientY);
    context.drawImage(video, 0, 0, 640, 480);
}
