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
            x:['Lindsay Graham(SC)', 'Chuck Grassley(IA)','Jim Inhofe(OK)', 'Richard Shelby(AL)'],
            y: [11873431,9883101,4646940, 4141799],
            type: 'bar',
            name: 'Chair Members $$'
        };
        
        var trace2 = {
            x:['Diane Feinstein(CA)', 'Ron Wyden(OR)', 'Jack Reed(RI)', 'Patrick Leahy(VT)'],
            y: [16092233,4408613,13705548, 4940984,],
            type: 'bar',
            name: 'Ranking Members $$'
        };
        
        var data = [trace1, trace2];
        
        var layout = {
            title: 'Chair and Ranking Member Contributions',
            showlegend: true
        };
        
        Plotly.newPlot('Bar_Graph', data, layout, {displayModeBar: false});

        var trace1 = {
            x: [672941,926007,588166,1335104],
            y: [11873431,9883101,4646940, 4141799],
            mode: 'markers',
            type: 'scatter'
        };

        var trace2 = {
            x: [192243,223675,1105119,6019422],
            y: [4940984,4408613,13705548,16092233],
            mode: 'lines',
            type: 'scatter'
        };

        var data = [trace1, trace2];

        Plotly.newPlot('myDiv', data);

    
//Bubble Chart

    var trace1 = {
        x: ['Lindsay Graham', 'Chuck Grassley','Jim Inhofe', 'Richard Shelby'],
        y: [1240075,1541036,820733,208744],
        text: ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100'],
        mode: 'markers',
        marker: {
          color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
          size: [6.72941,9.26007,5.88166,13.35104]
        }
      };

      var trace2 = {
        x: ['Patrick Leahy', 'Jack Reed', 'Ron Wyden','Dione Feinstein'],
        y: [320467, 316898, 1952478, 11113364],
        text: ['A<br>size: 40', 'B<br>size: 60', 'C<br>size: 80', 'D<br>size: 100'],
        mode: 'markers',
        marker: {
          color: ['rgb(93, 164, 214)', 'rgb(255, 144, 14)',  'rgb(44, 160, 101)', 'rgb(255, 65, 54)'],
          size: [1.92243,2.23675,11.05119,60.19422]
        }
      };
      
      var data = [trace1, trace2];
      
      var layout = {
        title: 'State total votes VS Candidate Vote',
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
      


