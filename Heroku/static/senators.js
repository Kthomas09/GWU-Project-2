function buildPlot() {
    d3.json("/votersinfo").then(function (data) {
        var state = data.votersinfo.state;
        var total_votes = data.votersinfo.totalvotes;
            //var trace1 = { 
        //type: "bar"
        //mode: "lines",
        /*name: state_po,
        x: state,
        y: totalvotes,
        line: {
        color: "#17BECF"
        }};  
        var data = [trace1];
        type: “bar”
    };
    var data = [trace1];var layout = {
      title: “‘Bar’ Chart”
    };Plotly.newPlot(“plot”, data, layout);      
        //var layout = //{
        //title: `${total_votes} totalvotes`,
        //xaxis: {
          //range: [startDate, endDate],
          //type: “date”
        },
        //yaxis: {
          //autorange: true,
          //type: "linear"
        //}
     // };     // Plotly.newPlot("plot", data, layout);    });
 // }  buildPlot();
     // return render_te
  
    */buildPlot();
        return render_template("index.html")
    })};