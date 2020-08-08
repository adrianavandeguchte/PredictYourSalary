function initializeViz() {
  // JS object that points at empty div in the html
  var countryDiv = document.getElementById("tableauCountry");
  // URL of the viz to be embedded
  var url = "https://public.tableau.com/profile/shrilekha.vijayakanthan8354#!/vizhome/TechSalaryAnalysis2/SalarybyCountry?publish=yes";
  // An object that contains options specifying how to embed the viz
  var options = {
    width: '600px',
    height: '600px',
    hideTabs: true,
    hideToolbar: true,
  };
  viz = new tableau.Viz(countryDiv, url, options);
