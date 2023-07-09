    function fileValidation() {
        var fileInput = document.getElementById('file');

        var filePath = fileInput.value;
        // var allowedExtensions = /(\.jpg|\.jpeg|\.bmb|\.png|\.gif)$/i;
		var allowedExtensions = /(\.mp3|\.wav|\.MP3)$/i;
        if (!allowedExtensions.exec(filePath)) {
            var erer = document.getElementById('info');
            erer.style.display = 'block';
            erer.innerHTML = '<i class="fa fa-close"></i> Sorry, only accepted files are .MP3, .WAV ';
            fileInput.value = '';
            return false;
        } else {
            //Image preview
            if (fileInput.files && fileInput.files[0]) {
                var reader = new FileReader();
                reader.onload = function(e) {

                    document.getElementById('info').style.display = 'block';
					document.getElementById('info').innerHTML = '<i class="fa fa-check"></i>This file is accepted';
					document.getElementById('uploadSubmit').style.display = 'block';
                };
                reader.readAsDataURL(fileInput.files[0]);
            }
        }
    }

var hiddenBtn = document.getElementById('file');
var chooseBtn = document.getElementById('upload-label');

hiddenBtn.addEventListener('change', function() {
    if (hiddenBtn.files.length > 0) {
        chooseBtn.innerText = hiddenBtn.files[0].name;
    } else {
        chooseBtn.innerText = 'Choose a File';
    }
});