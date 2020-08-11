

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
    const maxSize = d3v5.max(rawData, d => +d.count);

    // size bubbles based on area
    const radiusScale = d3v5.scaleSqrt()
      .domain([0, maxSize])
      .range([0, 60])

    // use map() to convert raw data into node data
    const myNodes = rawData.map(d => ({
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

d3.json("/tools_data", function (err, toolData) {
  toolData = toolData.filter(function (d) {
    return d.tool !== "None"
  });
  toolData = toolData.filter(function (d) {
    return d.tool !== "Other"
  });
  display(toolData)

});
