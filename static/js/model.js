country_region_url = "/country_region_data"
// d3.json(country_url).then((data) => {
d3.json(country_region_url).then(function(data) {
        
    var countries = data.map(item => item.country);

    countries = countries.sort();
        
    // selects the dropdown menu
    var country_menu = d3.select("#selCountry");

    // adds the id of each test subject to the dropdown menu and adds the value as the same number
    for (var i = 0; i < countries.length; i++) {
        country_menu.append("option").text(countries[i]).property("value", countries[i]);
    }
});

function optionChangedCountry(value) {
    country_region_url = "/country_region_data"
    d3.json(country_region_url).then(function(data) {
        var filteredData = data.filter(record => record.country === value);
        var region = filteredData[0].region
        var region_menu = d3.select("#selRegion");
        region_menu.html("");
        region_menu.append("option").text(region).property("value", region);
    })
}

function optionChangedTitle(value) {
    var managerInput = d3.select("#manager_input");

    if (value == "Manager") {
        console.log("hi");
        managerInput.html("");
        managerInput.append("option").text("Yes").property("value", "Yes");
    }
    else {
        managerInput.html("");
        managerInput.append("option").property("style", "display:none;").property("disabled", true).property("selected", true);
        managerInput.append("option").text("Yes").property("value", "Yes");
        managerInput.append("option").text("No").property("value", "No");
    }
}

var coll = document.getElementsByClassName("collapsible");
var i;

for (i = 0; i < coll.length; i++) {
  coll[i].addEventListener("click", function() {
    this.classList.toggle("active");
    var content = this.nextElementSibling;
    if (content.style.maxHeight){
      content.style.maxHeight = null;
    } else {
      content.style.maxHeight = content.scrollHeight + "px";
    }
  });
}