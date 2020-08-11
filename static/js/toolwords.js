var test = "/recommendations_data"

// d3.json(test, function (err, words) {
// var scaleCount = d3.scale.linear()
//   .domain([50,5300])
//   .range([15,100]);

// words.forEach(function (d) {
//   d.count = scaleCount(d.count);
// });
// words = words.filter(function (d) {
//   return d.recommended_first_language !== "None"
// });
// words = words.filter(function (d) {
//   return d.recommended_first_language !== "Other"
// });
// words = words.filter(function (d) {
//   return d.recommended_first_language !== "TypeScript"
// });
// console.log(words)
// Encapsulate the word cloud functionality
function wordCloud(selector) {

    var fill = d3.scale.category20();

    //Construct the word cloud's SVG element
    var svg = d3.select(selector).append("svg")
        .attr("width", 500)
        .attr("height", 500)
        .append("g")
        .attr("transform", "translate(250,250)");


    //Draw the word cloud
    function draw(words) {
        var cloud = svg.selectAll("g text")
                        .data(words, function(d) { return d.text; })

        //Entering words
        cloud.enter()
            .append("text")
            .style("font-family", "Impact")
            .style("fill", function(d, i) { return fill(i); })
            .attr("text-anchor", "middle")
            .attr('font-size', 1)
            .text(function(d) { return d.text; });

        //Entering and existing words
        cloud
            .transition()
                .duration(600)
                .style("font-size", function(d) { return d.size + "px"; })
                .attr("transform", function(d) {
                    return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
                })
                .style("fill-opacity", 1);

        //Exiting words
        cloud.exit()
            .transition()
                .duration(200)
                .style('fill-opacity', 1e-6)
                .attr('font-size', 1)
                .remove();
    }


    //Use the module pattern to encapsulate the visualisation code. We'll
    // expose only the parts that need to be public.
    return {

        //Recompute the word cloud for a new set of words. This method will
        // asycnhronously call draw when the layout has been computed.
        //The outside world will need to call this function, so make it part
        // of the wordCloud return value.
        update: function(words) {
            d3.layout.cloud().size([500, 500])
                .words(words)
                .padding(5)
                .rotate(function() { return ~~(Math.random() * 2) * 90; })
                .font("Impact")
                .fontSize(function(d) { return d.size; })
                .on("end", draw)
                .start();
        }
    }

}

//Some sample data - http://en.wikiquote.org/wiki/Opening_lines

// var words = [{word: "Running", size: "10"}, {word: "Surfing", size: "20"}, {word: "Climbing", size: "50"}, {word: "Kiting", size: "30"}, {word: "Sailing", size: "20"}, {word: "Snowboarding", size: "60"} ]
    //Prepare one of the sample sentences by removing punctuation,
    // creating an array of words and computing a random size attribute.
    function getWords(words) {
        return words
                // .replace(/[!\.,:;\?]/g, '')
                // .split(' ')
                .map(function(d) {
                    return {text: d.recommended_first_language, size:d.count};
                })
    }
//This method tells the word cloud to redraw with a new set of words.
//In reality the new words would probably come from a server request,
// user input or some other source.
function showNewWords(vis, i) {
    i = i || 0;

    vis.update(getWords(i ++ % words.length))
    // setTimeout(function() { showNewWords(vis, i + 1)}, 2000)
}


//Start cycling through the demo data
// showNewWords(myWordCloud);
// });

function wordDisplay(rawData) {
  //Create a new instance of the word cloud visualisation.
  var vis = wordCloud('.wordCloud')
  vis.update(getWords(rawData));

}

d3.json(test, function (err, rawData) {
  var scaleCount = d3.scale.linear()
    .domain([50,5300])
    .range([15,100]);
  rawData.forEach(function (d) {
    d.count = scaleCount(d.count);
  });
  rawData = rawData.filter(function (d) {
    return d.recommended_first_language !== "None"
  });
  rawData = rawData.filter(function (d) {
    return d.recommended_first_language !== "Other"
  });
  rawData = rawData.filter(function (d) {
    return d.recommended_first_language !== "TypeScript"
  });
  wordDisplay(rawData);
});

// function selectFilter(filter) {
//   var sel = document.getElementById('jobFilter');
// }
