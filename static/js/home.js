$(document).ready(function () {
    if (document.location.pathname === '/') {
        getData();
    } else if (document.location.pathname === '/admin') {
        if ($('#upload_file').is(':checked')) {

            uploaderBlock.show();
            setupBlock.hide();
            iqamaBlock.hide();
            // $('#file_input').attr('required', true);
        } else {
            uploaderBlock.hide();
            setupBlock.show();
            iqamaBlock.show();
            // chShipBlock.find('input').attr('required', false);
        }
    }


    // showSlides()
});

var form = $('#setting'), showUploadFile = $('#upload_file'), uploaderBlock = $('#uploader_block'),
    setupBlock = $('#setup'), iqamaBlock = $('#iqama');

uploaderBlock.hide();

showUploadFile.on('click', function () {
    console.log("checked");
    if ($(this).is(':checked')) {

        uploaderBlock.show();
        setupBlock.hide();
        iqamaBlock.hide();
        // $('#file_input').attr('required', true);
    } else {
        uploaderBlock.hide();
        setupBlock.show();
        iqamaBlock.show();
        // chShipBlock.find('input').attr('required', false);
    }
});

function jsUcfirst(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function getData() {
    const timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'];
    URL = 'http://' + document.domain + ':' + location.port + '/';
    const table_body = document.getElementById("prayer_table");
    while (table_body.firstChild) {
        table_body.removeChild(table_body.firstChild);
    }
    $.ajax({
        type: "post",
        url: URL,
        success: function (data) {
            let cellText;
            let cell;
            console.log(data);
            data = data['today'];
            for (let i = 0; i < timeNames.length; i++) {

                // console.log(key + " -> " + data[key]);
                const row = document.createElement("tr");
                cell = document.createElement("td");
                cellText = document.createTextNode(jsUcfirst(timeNames[i]));
                cell.appendChild(cellText);
                row.appendChild(cell);
                for (let j = 0; j < 2; j++) {
                    // create element <td> and text node
                    //Make text node the contents of <td> element
                    // put <td> at end of the table row
                    cell = document.createElement("td");
                    cellText = document.createTextNode(data[timeNames[i]][j]);

                    cell.appendChild(cellText);
                    row.appendChild(cell);
                }

                console.log(row);
                table_body.appendChild(row);


            }

        }
    });

    setTimeout(getData, 43200000); // Change image every 12 hours
}

// let slideIndex = 0;
// function showSlides() {
//
//   let i;
//   const slides = document.getElementsByClassName("mySlides");
//   for (i = 0; i < slides.length; i++) {
//     slides[i].style.display = "none";
//   }
//   slideIndex++;
//     if (slideIndex > slides.length) {
//
//     slideIndex = 1
//   }
//
//   slides[slideIndex - 1].style.display = "block";
//   setTimeout(showSlides, 10000); // Change image every 10 seconds
// }