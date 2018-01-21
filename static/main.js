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
        // video.onloadedmetadata = function() {
            
        // }
    });
}

// console.log(vidWidth);
// console.log(vidHeight);

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
    var winWidth = window.innerWidth;
    var winHeight = window.innerHeight;
    var vidWidth = video.videoWidth;
    var vidHeight = video.videoHeight;
    var xOffset = 0;
    var yOffset = 0;
    var ratio = 1;
    if(winWidth/winHeight < vidWidth/vidHeight) {
        xOffset = (vidWidth/vidHeight*winHeight - winWidth)/2.0;
        ratio = winHeight/vidHeight;
    }
    else {
        yOffset = (vidHeight/vidWidth*winWidth - winHeight)/2.0;
        ratio = winWidth/vidWidth;
    }
    var x = parseInt(parseFloat(e.touches[0].clientX + xOffset)/ratio);
    var y = parseInt(parseFloat(e.touches[0].clientY + yOffset)/ratio);
    console.log(x, y);
    context.drawImage(video, 0, 0, vidWidth, vidHeight);
    canvas.toBlob(function(blob) {
        // Debug stuff
        console.log(blob);
        img = new Image();
        img.src = URL.createObjectURL(blob);
        console.log(img);
        document.body.appendChild(img);
        // context.drawImage(img, 0, 0, vidWidth, vidHeight);
        // End Debug
        // Post request

        // var reader = new FileReader();
        // reader.onload = function(event){
        //     var fd = new FormData();
        //     fd.append('fname', 'image.jpg');
        //     fd.append('data', event.target.result);
        //     fd.append('x', x);
        //     fd.append('y', y);
        //     var xhr = new XMLHttpRequest();
        //     console.log(fd);
        //     xhr.open('POST', '/process_menu', true);
        //     xhr.setRequestHeader('Content-Type', 'application/json');
        //     xhr.send(fd);
        // };      
        // reader.readAsDataURL(blob);
        
        var reader = new FileReader()

        reader.onload = function(event) {
            var fd = new FormData();
            fd.append('x', x);
            fd.append('y', y);
            fd.append('image', event.target.result);

            $.ajax({
                type: 'POST',
                url: '/process_menu',
                data: fd,
                processData: false,
                contentType: false
            }).done(function(data) {
                console.log(data);
            });
        };

        reader.readAsDataURL(blob)

        //var xhr = new XMLHttpRequest();
        //xhr.open('POST', '/process_menu', true);
        //var fd = {
        //    'image': blob,
        //    'x': x,
        //    'y': y
        //};
        //var fd = new FormData();
        //fd.set('image', blob);
        //fd.set('x', x);
        //fd.set('y', y);
        //console.log("HIIII")
        //console.log(fd);
        //xhr.setRequestHeader('Content-Type', 'application/json');
        //console.log(fd)
        //xhr.send(JSON.stringify(fd));
    }, 'image/jpeg');
}

function init() {
    var fd = new FormData();
    fd.append('restaurant', 'sangkee');
    fd.append('uid', 11223344);
    $.ajax({
                    type: 'POST',
                    url: '/init',
                    data: fd,
                    processData: false,
                    contentType: false
                }).done(function(data) {
                    console.log(data);
    });

    console.log("HELLO");
};

init();
