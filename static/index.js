function copyToClipboard() {
  let clip = navigator.clipboard;
  if (clip === undefined) {
    console.log("Upgrade your browser to use the clipboard feature.");
  } else {
    if (document.getElementById("text").value != "") {
      navigator.clipboard.writeText(document.getElementById("text").value);
      var copy = document.getElementById("clipImg");
      copy.classList.add('fa-check-circle');
      copy.classList.remove('fa-copy');
      setTimeout(() => {
        var temp = document.getElementById("clipImg");
        temp.classList.add('fa-copy');
        temp.classList.remove('fa-check-circle');
      }, 1000);
    } else alert("Please First Upload Image");
  }
}

function changeTheme() {
  document.body.classList.toggle("theme");
  if (document.getElementById('img-icon').classList.contains("fa-sun")) {
    document.getElementById('img-icon').classList.remove("fa-sun")
    document.getElementById('img-icon').classList.add("fa-moon")
  } else {
    document.getElementById('img-icon').classList.add("fa-sun")
    document.getElementById('img-icon').classList.remove("fa-moon")
  }
};



var imageName = document.getElementById('hasImage').innerHTML;
if(imageName != "") {
  let path = "../static/img/";
  path = path.concat(imageName);
  document.getElementById('fileImage').src = path;
  document.getElementById("fileImage").classList.add("fileCss");
  $(".imgupload").hide("slow");
  $("#namefile").html(imageName);
  $("#namefile").css({ color: "black", "font-weight": 700 });
}


$("#fileup").change(function () {
  var res = $("#fileup").val();
  var arr = res.split("\\");
  var filename = arr.slice(-1)[0];
  filextension = filename.split(".");
  filext = "." + filextension.slice(-1)[0];
  valid = [".jpg", ".png", ".jpeg"];
  document.getElementById("fileImage").classList.remove("fileCss");
  if (valid.indexOf(filext.toLowerCase()) == -1) {
    $(".imgupload").hide("slow");
    $(".imgupload.ok").hide("slow");
    $(".imgupload.stop").show("slow");

    $("#namefile").css({ color: "red", "font-weight": 700 });
    $("#namefile").html("File " + filename + " is not  pic!");

    $("#submitbtn").hide();
    $("#fakebtn").show();
  } else {
    //if file is valid we show the green alert and show the valid submit
    $(".imgupload").hide("slow");
    $(".imgupload.stop").hide("slow");
    let path = "../static/";
    path = path.concat(filename);
    // console.log(path);
    // document.getElementById("check").innerHTML="<img src='' alt='file'></img>";
    // document.getElementById("check").src=path;
    // $(".imgupload.ok")[0].innerHTML="<img id='check' src='#' alt='file'></img>";
    // document.getElementById("check").src=path;

    $(".imgupload.ok").show("slow");

    $("#namefile").css({ color: "green", "font-weight": 700 });
    $("#namefile").html(filename);

    $("#submitbtn").show();
    $("#fakebtn").hide();
  }
});

function saveTextAsFile(textToWrite, checkId) {
  if (textToWrite != "") {
    if (checkId == "txtFile") {
      var textFileAsBlob = new Blob([textToWrite], { type: "text/plain" });
      var downloadLink = document.createElement("a");
      downloadLink.download = "Download.txt";
      downloadLink.innerHTML = "Download File";
      if (window.webkitURL != null) {
        // Chrome allows the link to be clicked
        // without actually adding it to the DOM.
        downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
      } else {
        // Firefox requires the link to be added to the DOM
        // before it can be clicked.
        downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
        downloadLink.onclick = destroyClickedElement;
        downloadLink.style.display = "none";
        document.body.appendChild(downloadLink);
      }

      downloadLink.click();
    } else if(checkId == "pdf") {
      var doc = new jsPDF();
      doc.text(20, 20, textToWrite);
      // Save the PDF
      doc.save("Download.pdf");
    }
    else document.getElementById("wordText").value = text;
  } else alert("Please First Upload Image");
}


function clickFileup() {
  document.getElementById('fileup').click();
};

function clickSubmit() {
  document.getElementById('word').click();
};

