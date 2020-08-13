function loadFilter(filter) {
  var recURL = "/recommendations_data" + filter
  var toolURL = "/tools_data" + filter

  console.log(recURL)

  document.getElementById("bubble").innerHTML = '';
  function bubbleChart() {
    const width = 900;
    const height = 640;

    // location to centre the bubbles
    const centre = { x: width/2, y: height/2 };

    // strength to apply to the position forces
    const forceStrength = 0.03;

    // these will be set in createNodes and chart functions
    let svg = null;
    let bubbles = null;
    let labels = null;
    let nodes = [];

    // charge is dependent on size of the bubble, so bigger towards the middle
    function charge(d) {
      return Math.pow(d.radius, 2.0) * 0.01
    }

    // create a force simulation and add forces to it
    const simulation = d3v5.forceSimulation()
      .force('charge', d3v5.forceManyBody().strength(charge))
      // .force('center', d3v5.forceCenter(centre.x, centre.y))
      .force('x', d3v5.forceX().strength(forceStrength).x(centre.x))
      .force('y', d3v5.forceY().strength(forceStrength).y(centre.y))
      .force('collision', d3v5.forceCollide().radius(d => d.radius + 1));

    // force simulation starts up automatically, which we don't want as there aren't any nodes yet
    simulation.stop();

    // set up colour scale
    const fillColour = d3v5.scaleOrdinal()
    	.domain(["database","ml_model","visualization_library","language","text_editor","course_platform"])
    	.range(["#8583f8", "#7FDBFF", "#39CCCC", "#3D9970", "#AAAAAA","#9cb4eb","#89daae"]);



    // data manipulation function takes raw data from csv and converts it into an array of node objects
    // each node will store data and visualisation values to draw a bubble
    // rawData is expected to be an array of data objects, read in d3v5.csv
    // function returns the new node array, with a node for each element in the rawData input
    function createNodes(rawData) {
      // use max size in the data as the max in the scale's domain
      // note we have to ensure that size is a number
      var maxSize = d3v5.max(rawData, d => +d.count);

      // size bubbles based on area
      var radiusScale = d3v5.scaleSqrt()
        .domain([0, maxSize])
        .range([0, 60])

      // use map() to convert raw data into node data
      var myNodes = rawData.map(d => ({
        ...d,
        radius: radiusScale(+d.count),
        size: +d.count,
        x: Math.random() * 600,
        y: Math.random() * 400
      }))

      return myNodes;
    }

    // main entry point to bubble chart, returned by parent closure
    // prepares rawData for visualisation and adds an svg element to the provided selector and starts the visualisation process
    let chart = function chart(selector, rawData) {
      // convert raw data into nodes data
      nodes = createNodes(rawData);

      // create svg element inside provided selector
      svg = d3v5.select(selector)
        .append('svg')
        .attr('width', width)
        .attr('height', height)

      // bind nodes data to circle elements
      const elements = svg.selectAll('.bubble')
        .data(nodes, d => d.tool)
        .enter()
        .append('g')

      bubbles = elements
        .append('circle')
        .classed('bubble', true)
        .attr('r', d => d.radius)
        .attr('fill', d => fillColour(d.type))

      // labels
      labels = elements
        .append('text')
        .attr('dy', '.3em')
        .style('text-anchor', 'middle')
        .style('font-size', 10)
        .text(d => d.tool)

      // set simulation's nodes to our newly created nodes array
      // simulation starts running automatically once nodes are set
      simulation.nodes(nodes)
        .on('tick', ticked)
        .restart();
    }

    // callback function called after every tick of the force simulation
    // here we do the actual repositioning of the circles based on current x and y value of their bound node data
    // x and y values are modified by the force simulation
    function ticked() {
      bubbles
        .attr('cx', d => d.x)
        .attr('cy', d => d.y)

      labels
        .attr('x', d => d.x)
        .attr('y', d => d.y)
    }

    // return chart function from closure
    return chart;
  }

  // new bubble chart instance
  let myBubbleChart = bubbleChart();

  // function called once promise is resolved and data is loaded from csv
  // calls bubble chart function to display inside #vis div
  function display(data) {
    myBubbleChart('#bubble', data);
  }

  d3.json(toolURL, function (err, toolData) {
    toolData = toolData.filter(function (d) {
      return d.tool !== "None"
    });
    toolData = toolData.filter(function (d) {
      return d.tool !== "Other"
    });
    display(toolData)
  });




  document.getElementById("wordSVG").innerHTML = '';
    d3.json(recURL, function (err, words) {
      var maxWord = d3.max(words, d => +d.count);
      var scaleCount = d3.scale.linear()
        .domain([5,maxWord])
        .range([15,100]);
      words.forEach(function (d) {
        d.count = scaleCount(d.count);
      });
      words = words.filter(function (d) {
        return d.recommended_first_language !== "None"
      });
      words = words.filter(function (d) {
        return d.recommended_first_language !== "Other"
      });
      // Encapsulate the word cloud functionality
      function wordCloud(selector) {

          var fill = d3.scale.category20();

          //Construct the word cloud's SVG element
          var svg = d3.select(selector)
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
          function getWords(i) {
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

      //Create a new instance of the word cloud visualisation.
      var myWordCloud = wordCloud('#wordSVG');

      //Start cycling through the demo data
      showNewWords(myWordCloud);
      });

}
