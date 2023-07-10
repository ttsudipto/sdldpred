function makeDensityPlot(div_id, jsonData, distances, drugs) {
    var data = JSON.parse(jsonData);
    var graphDiv = document.getElementById(div_id);
    var density_curve = {
        x: data.x,
        y: data.y,
        name: 'Probability density of distance between two drugs (<i>f<sub>dist</sub></i>)',
        line: {
            width: 3,
            color: 'slategray'
        }
    };
    var traces = [density_curve];
    var pt_colors = ['red', 'green', 'purple', 'darkorange', 'cyan', 'blue', 'magenta', 'blue', 'yellowgreen', 'saddlebrown'];
    for (var i=0; i<distances.length; ++i){
        traces.push({
            mode: 'markers',
            x: [distances[i]],
            y: [0],
            name: drugs[i],
            marker: {
                color: pt_colors[i],
                size: 6
            }
        });
    }
    var shapes = [];
    for (var i=0; i<distances.length; ++i) {
        shapes.push({
            type: 'line',
            yref: 'paper',
            x0: distances[i],
            y0: 0,
            x1: distances[i],
            y1: 1,
            name: drugs[i],
            line:{
                dash:'dot',
                color: pt_colors[i],
                width:1
            }
        });
    }
    shapes.push({
        type: 'rect',
        yref: 'paper',
        x0: 0,
        y0: 0,
        x1: 1.6295,
        y1: 1,
        fillcolor: 'darkslategray',
        opacity: 0.15,
        line: {width:0}
    });
    var layout = {
        plot_bgcolor: 'white',
        paper_bgcolor: 'white',
        height: 500,
//         title : {
//             text: 'Density plot and the predicted CT severity score',
//             font: {size: 24}
//         },
        shapes: shapes,
        xaxis: {
            visible : true,
            range: ((distances[distances.length - 1] < 6.3) ? [0, 6.3] : [0, 17.4642]),
            color: 'black',
            linewidth: 2,
            ticks: 'outside',
            ticklen: 10,
            tickwidth: 2,
            tickfont: {size: 14},
            title : {
                text : 'Euclidean distance between two drugs',
                font: {size: 18}
            }
        },
        yaxis: {
            visible : true,
            color: 'black',
            linewidth: 2,
            ticks: 'outside',
            ticklen: 10,
            tickwidth: 2,
            tickfont: {size: 14},
            title : {
                text : 'Probability',
                font: {size: 18}
            }
        },
        legend: {
            orientation: 'h',
            x: 0.15,
            y: 50,
            font: {size: 16}
        },
        hoverlabel: {
            font: {size: 16}
        },
        margin: {t:20}
    };

    Plotly.plot(graphDiv, traces, layout, {showSendToCloud:false});
}

function plotDensity(div_id, distances, drugs){
    var httpReq = new XMLHttpRequest();
    httpReq.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            makeDensityPlot(div_id, this.responseText, distances, drugs);
        }
    };
    httpReq.open('GET', 'get_density.php', true);
    httpReq.setRequestHeader("Content-type", "text/json");
    httpReq.send();
}
