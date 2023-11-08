
    function sleep(ms) {
        return new Promise(resolve => setTimeout(resolve, ms));
    }

    const positions = document.getElementById("positions");
    const buttonPositions = document.getElementById('btn-position');
    const buttonPhoto = document.getElementById('btn-photo');
    const progressBar = document.getElementById('position-progress');
    const image = document.getElementById('telescope-image');
    const imageLegend = document.getElementById('telescope-image-caption');

    const long1Span = document.getElementById('longitude-1');
    const long2Span = document.getElementById('longitude-2');
    const lat1Span = document.getElementById('latitude-1');
    const lat2Span = document.getElementById('latitude-2');

    var long1=78;
    var long2=23.23;
    var lat1=-45;
    var lat2=23.34;


    async function handlePositionClick() {
        buttonPositions.disabled = true;
        buttonPhoto.disabled = true;

        var long1Delta = (Math.floor(Math.random() * 180 - 90) - long1) / 100;
        var lat1Delta = (Math.floor(Math.random() * 180 - 90) - lat1) / 100;

        for(var i=0; i<=100; i++) {
            progressBar.style.width = "" + i + "%";
            long2 = Math.random() * 60;
            lat2 = Math.random() * 60;
            long1 += long1Delta;
            lat1 += lat1Delta;
            updateCoordinates();
            await sleep(10);
        }

        buttonPositions.disabled = false;
        buttonPhoto.disabled = false;
    }

    function handlePhotoClick() {
        var text = positions.options[positions.selectedIndex].text;
        var value = positions.value;

        image.src = value + ".jpg";
        imageLegend.innerHTML = text;
    }

    function updateCoordinates() {
        long1Span.innerHTML = long1.toFixed(0);
        long2Span.innerHTML = long2.toFixed(2);
        lat1Span.innerHTML = lat1.toFixed(0);
        lat2Span.innerHTML = lat2.toFixed(2);
    }

    buttonPositions.addEventListener("click", event => handlePositionClick());
    buttonPhoto.addEventListener("click", event => handlePhotoClick());

    handlePhotoClick();
    updateCoordinates();