function jsUcfirst(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}
function getData() {
  var timeNames = ['fajr', 'dhuhr', 'asr', 'maghrib', 'isha'];
  URL = 'https://' + document.domain + ':' + location.port + '/';
  var table_body = document.getElementById("prayer_table");
  while (table_body.firstChild) {
    table_body.removeChild(table_body.firstChild);
  }
  $.ajax({
    type: "post",
    url: URL,
    success: function (data) {
      console.log(data);
      for (i = 0; i < timeNames.length; i++) {

        // console.log(key + " -> " + data[key]);
        var row = document.createElement("tr");
        var cell = document.createElement("td");
        var cellText = document.createTextNode(jsUcfirst(timeNames[i]));
        cell.appendChild(cellText);
        row.appendChild(cell);
        for (var j = 0; j < 2; j++) {
          // create element <td> and text node
          //Make text node the contents of <td> element
          // put <td> at end of the table row
          var cell = document.createElement("td");
          var cellText = document.createTextNode(data[timeNames[i]][j]);

          cell.appendChild(cellText);
          row.appendChild(cell);
        }

        console.log(row);
        table_body.appendChild(row);


      }

    }
  });
}

$(document).ready(function () {

  getData();
  setInterval(function () {
    getData();
  }, 86400000); //86400000 milliseconds = 1 day
});
