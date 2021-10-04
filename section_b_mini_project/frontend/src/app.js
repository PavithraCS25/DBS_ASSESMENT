const ENDPOINT_URL = "http://127.0.0.1:8000/v1/music";

window.addEventListener('load', function() {
        //console.log('All assets are loaded')
        loadPredictionData();
        loadFiles();
        loadGenre();
    })
    // -------------------------------------------------------------------------------------------------------------

const getData = async(url) => {
    try {
        const response = await fetch(url);
        const json = await response.text();
        console.log("GetData - " + JSON.stringify(JSON.parse(json)));
        return JSON.parse(json);
    } catch (error) {
        console.log(error)
    }
}

const post = async(url, body) => {
    try {
        console.log("post - " + url + " post data - " + JSON.stringify(body));
        const response = await fetch(url, body);
        const json = await response.json();
        console.log("post response - " + JSON.stringify(json));
        return json;
    } catch (error) {
        console.log("post err - " + error);
    }
}

// -------------------------------------------------------------------------------------------------------------

function loadPredictionData(fileId) {
    var id = fileId ? fileId : "all";
    getData(ENDPOINT_URL + "/predictions/" + id + "/").then((res) => {
        if (res) {
            loadFiles();
            loadGenre();
            $("#workerdata").show();
            $('#titledata').hide();
            console.log(res);
            $('#workerdata').bootstrapTable({
                data: res,
                onClickRow: function(row, $element) {
                    console.log(JSON.stringify($element))
                }
            });
        }
    });
}

function loadSelect(key, result, text, value) {
    if (result) {
        $("#" + key).empty();
        elm = document.getElementById(key);
        df = document.createDocumentFragment();
        for (var item in result) {
            var option = document.createElement('option');
            option.value = result[item][value];
            option.appendChild(document.createTextNode(result[item][text]));
            df.appendChild(option);
        }
        elm.appendChild(df);
    }
}

function loadFiles() {
    getData(ENDPOINT_URL + "/fetchauditfile/").then((result) => {
        if (result) {
            loadSelect("selectFile", result, 'filename', 'file_id');
        }
    });
}

function loadGenre() {
    getData(ENDPOINT_URL + "/predictions/genres/").then((result) => {
        if (result) {
            loadSelect("genres", result, 'LR_classified_genre', 'LR_classified_genre');
        }
    });
}

function loadTitlesByGenre() {
    if ($("#genres").val())
        getData(ENDPOINT_URL + "/predictions/tiles/" + $("#genres").val()).then((result) => {
            if (result) {
                $("#workerdata").hide();
                $('#titledata').show();
                $('#titledata').bootstrapTable({
                    data: result,
                    onClickRow: function(row, $element) {}
                });
            }
        });

}

function LinkFormatter(value, row, index) {
    return "<a href='" + row.url + "'>" + value + "</a>";
}

/*
 if (res && res.ContentType && res.data) {
            $("#uploadfile").hide();
            $("#newphoto").hide();
        } else {
            $("#uploadfile").show();
            $("#newphoto").show();
        } */

var fileupld = document.getElementById('uploadfile');
fileupld.addEventListener('click', function() {
    var file = document.getElementById("predictfile");
    if (file.files && file.files[0]) {
        predict(file.files[0]).then((res) => {
            //alert("Uploaded successfully !")
        });
    } else {
        alert("Please select a file to proceed");
        $("#predictfile").removeAttr('value');
    }
});


var loadFileContent = document.getElementById('loadFile');
loadFileContent.addEventListener('click', function() {
    var fileId = $("#selectFile").val();
    console.log(fileId)
    if (fileId) {
        $('#workerdata').bootstrapTable('destroy');
        $('#titledata').bootstrapTable('destroy');
        loadPredictionData(fileId);
    }
});


var loadGenres = document.getElementById('loadGenres');
loadGenres.addEventListener('click', function() {
    var genre = $("#genres").val();
    console.log(genre)
    if (genre) {
        $('#workerdata').bootstrapTable('destroy');
        $('#titledata').bootstrapTable('destroy');
        loadTitlesByGenre();
        console.log("File content loaded : " + genre);
    }
});

async function predict(file) {
    const body = new FormData();
    body.append('file', file, file.name);
    const response = await fetch(ENDPOINT_URL + "/predictions/", {
        body,
        headers: {
            Accept: "application/json"
        },
        method: "POST"
    });
    //console.log(JSON.stringify(response));
    return response.json();
}

function clearImg() {
    document.getElementById('predictfile').value = "";
    $("#uploadfile").hide();
    $("#predictfile").hide();
}

// -------------------------------------------------------------------------------------------------------------

// Audit ----------

$('a[data-bs-toggle="tab"]').on('shown.bs.tab', function(e) {
    //alert("id" + e.target.id);
    /*document.getElementById("newphoto").value = "";
    switch (e.target.id) {
        case "audit-tab":
            {
                generateAccordian();
                break;
            }
    }*/
});

function generateAccordian() {
    getData(ENDPOINT_URL + "/photos?type=getPrefix").then((res) => {
        //alert("getphoto - " + JSON.stringify(res))
        if (res) {
            var accordianContent = "";
            res.forEach(function(data) {
                //console.log(data.Prefix);
                var id = "id_" + data.Prefix.substring(0, data.Prefix.length - 1);
                var dataId = id + "_data";
                accordianContent += '<div class="accordion-item">' +
                    '<h2 class="accordion-header" id="' + id + '">' +
                    '<button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#' + dataId + '" aria-expanded="false" aria-controls="' + dataId + '">' + data.Prefix +
                    '</button></h2><div id="' + dataId + '" class="accordion-collapse collapse" aria-labelledby="' + id + '" data-bs-parent="#auditData"><div class="accordion-body">DATA</div></div></div>'
                $("#auditData").html(accordianContent);
            })
        } else {
            console.log("Err: cant load audit data !!")
        }
    });
}
/*
var myCollapsible = document.getElementById('auditData')
myCollapsible.addEventListener('shown.bs.collapse', function(event) {
    var tableContent = '<div class="table-responsive-lg" style="margin:4%;"><table id="' + event.target.id + "_table" + '" class="table table-hover" style="width:80%;height: 60%;overflow-y: auto;"><thead><tr><th data-field="Key">Name</th><th data-field="LastModified" data-formatter="dateFormat">Time</th><th data-field="Size" data-formatter="numFormat">Size</th></tr></thead></table></div>'
    $("#" + event.target.id).html(tableContent);
    loadS3Content(event.target.id);

}); */
// Audit End -------


function clear() {
    $("main").hide();
}