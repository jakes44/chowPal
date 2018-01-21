// Grab elements, create settings, etc.
var video = document.getElementById('video');
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
var didElm = document.getElementById('did');
var lightbulb = document.getElementById("lightbulb");

function openNav() {
    document.getElementById("myNav").style.width = "100%";
}

function closeNav() {
    document.getElementById("myNav").style.width = "0%";
    var fd = new FormData();
    fd.append('did', didElm.href);
    fd.append('like', 0);
    $.ajax({
        type: 'POST',
        url: '/yes_no_feedback',
        data: fd,
        processData: false,
        contentType: false
    }).done(function(data) {
        console.log(data);
    });
}

function acceptFood() {
    document.getElementById("myNav").style.width = "0%";
    var fd = new FormData();
    fd.append('did', didElm.href);
    fd.append('like', 1);
    $.ajax({
        type: 'POST',
        url: '/yes_no_feedback',
        data: fd,
        processData: false,
        contentType: false
    }).done(function(data) {
        console.log(data);
    });
}

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

lightbulb.addEventListener("click", function() {
    lightbulb.src = "/static/fa-lightbulb.gif"
    var vidWidth = video.videoWidth;
    var vidHeight = video.videoHeight;
    context.drawImage(video, 0, 0, vidWidth, vidHeight);
    canvas.toBlob(function(blob) {
        // Debug stuff
        console.log(blob);
        img = new Image();
        img.src = URL.createObjectURL(blob);
        console.log(img);
        // document.body.appendChild(img);
        // context.drawImage(img, 0, 0, vidWidth, vidHeight);
        // End Debug

        // Post request      
        var reader = new FileReader()

        reader.onload = function(event) {
            var fd = new FormData();
            fd.append('image', event.target.result);

            $.ajax({
                type: 'POST',
                url: '/recommend',
                data: fd,
                processData: false,
                contentType: false
            }).done(function(data) {
                console.log(data);
                lightbulb.src = "/static/fa-lightbulb.png"
                openNav();
                didElm.href = data[0].did;
            });
        };
    
        reader.readAsDataURL(blob)
    }, 'image/jpeg');
})

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
        // document.body.appendChild(img);
        // context.drawImage(img, 0, 0, vidWidth, vidHeight);
        // End Debug

        // Post request      
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
                var blurbTitle = document.getElementById('blurb-title');
                var blurbText = document.getElementById('blurb-text');
                blurbTitle.innerHTML = data[0].name;
                blurbText.innerHTML = data[0].blurb;
                openNav();
                didElm.href = data[0].did;
            });
        };

        reader.readAsDataURL(blob)
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
