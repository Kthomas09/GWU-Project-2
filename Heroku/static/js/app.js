// //Format needed for files
// d3.json("/static/data/votersinfo.json").then(function (data) {
//   console.log(data);
// });

Promise.all([
    d3.json("static/data/Chair_Members.json"),
    d3.json("/static/data/votersinfo.json"),]).then(function(files){
        //testing promise
        // console.log(files[0]);
        // console.log(files[1]);

        //getting data from chair_members.json

        // for (const [key, value] of Object.entries(files[0])){
        //     console.log(`${key}: ${value}`)
        // }

        var chairNames = files[0].Chair_Names;
        console.log("chairNames");
        console.log(chairNames);
        var chairLastName = files[0].C_Last_Name;
        console.log("chairLastName");
        console.log(chairLastName);

        //Getting data from votersinfo.json
        var candidateVotes = files[1].candidatevotes;
        console.log("candidateVotes");
        console.log(candidateVotes);
        var totalVotes = files[1].totalvotes;
        console.log("totalVotes");
        console.log(totalVotes);
        var stateVotes = files[1].state;
        console.log("stateVotes")
        console.log(stateVotes);
        let varList = [chairNames, chairLastName, candidateVotes, totalVotes, stateVotes];

        var trace1 = {
            x:['Zebras', 'Lions', 'Pelicans'],
            y: [90, 40, 60],
            type: 'bar',
            name: 'New York Zoo'
        };
        
        var trace2 = {
            x:['Zebras', 'Lions', 'Pelicans'],
            y: [10, 80, 45],
            type: 'bar',
            name: 'San Francisco Zoo'
        };
        
        var data = [trace1, trace2];
        
        var layout = {
            title: 'Hide the Modebar',
            showlegend: true
        };
        
        Plotly.newPlot('Bar_Graph', data, layout, {displayModeBar: false});

        var trace1 = {
            x: [1, 2, 3, 4],
            y: [10, 15, 13, 17],
            mode: 'markers',
            type: 'scatter'
        };

        var trace2 = {
            x: [2, 3, 4, 5],
            y: [16, 5, 11, 9],
            mode: 'lines',
            type: 'scatter'
        };

        var trace3 = {
            x: [1, 2, 3, 4],
            y: [12, 9, 15, 12],
            mode: 'lines+markers',
            type: 'scatter'
        };

        var data = [trace1, trace2, trace3];

        Plotly.newPlot('myDiv', data);

    


    var trace1 = {
        x: ['Alabama', 'Alaska', 'Colorado'],
        y: [25029181, 4141799, 14766949],
        text: ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100'],
        mode: 'markers',
        marker: {
          color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
          size: [81.8090, 28.2400, 204.1058]
        }
      };
      
      var data = [trace1];
      
      var layout = {
        title: 'Bubble Chart Hover Text',
        showlegend: false,
        height: 600,
        width: 600
      };
      
      Plotly.newPlot('BubbleChart', data, layout);

    //end of promise function
}).catch(function (error) {
    console.log(error);
//end of error catching function
});
      


