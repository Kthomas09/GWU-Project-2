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



    //end of promise function
    }).catch(function (error) {
        console.log(error);
    //end of error catching function
    });



