function loadFilter(filter) {
  var recURL = "/recommendations_data" + filter
  var toolURL = "/tools_data" + filter

  console.log(recURL)

  document.getElementById("bubble").innerHTML = '';
  d3.json(toolURL, function (err, toolData) {
    toolData = toolData.filter(function (d) {
      return d.tool !== "None"
    });
    toolData = toolData.filter(function (d) {
      return d.tool !== "Other"
    });
    display(toolData)
  });
  document.getElementById("wordCloud").innerHTML = '';
    d3.json(recURL, function (err, rawData) {
      var maxWord = d3.max(rawData, d => +d.count);
      var scaleCount = d3.scale.linear()
        .domain([50,maxWord])
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
      wordDisplay(rawData);
    });


}
