country_region_url = "/country_region_data"

// calls api to retrieve country and region data
d3.json(country_region_url).then(function(data) {
    // extracts only the countries of the api
    var countries = data.map(item => item.country);
    // puts countries in alphebetical order
    countries = countries.sort();   
    // selects the dropdown menu for countries input
    var country_menu = d3.select("#selCountry");
    // adds the list of countries to the dropdown menu on the form
    for (var i = 0; i < countries.length; i++) {
        country_menu.append("option").text(countries[i]).property("value", countries[i]);
    }
});

// this function is called when a user selects a country
function optionChangedCountry(value) {
    country_region_url = "/country_region_data"
    // calls api to retrieve country and region data
    d3.json(country_region_url).then(function(data) {
        // finds the record of the country that the user selected
        var filteredData = data.filter(record => record.country === value);
        // takes the region of the country that use user selected
        var region = filteredData[0].region
        // selects the dropdown menu for region input
        var region_menu = d3.select("#selRegion");
        // makes the region input blank
        region_menu.html("");
        // makes the region input only have 1 option- the matching region of the country the user selected
        region_menu.append("option").text(region).property("value", region);
    })
}

// this function is called when a user selects a job title
function optionChangedTitle(value) {
    // selects the dropdown menu for manager input
    var managerInput = d3.select("#manager_input");
    // if the user select manager as a job title, make the "are you a manager" drop down only have "yes" as an option
    if (value == "Manager") {
        console.log("hi");
        managerInput.html("");
        managerInput.append("option").text("Yes").property("value", "Yes");
    }
    // if the user selects any other job title, make both yes and no options available for manager
    else {
        managerInput.html("");
        managerInput.append("option").property("style", "display:none;").property("disabled", true).property("selected", true);
        managerInput.append("option").text("Yes").property("value", "Yes");
        managerInput.append("option").text("No").property("value", "No");
    }
}

// function submitForm() {
//   console.log("hi")
//     var features = d3.select("#features");
//     features.html("");
//     features.html("n\
//             Order of importance of the variables in predicting your salary:n\
//             1. Country<br>n\
//             2. Primary Dtabase<br>n\
//             3. Years With This Database<br>n\
//             4. Are You a Manager?<br>n\
//             5. Is Education is Computer Related?<br>n\
//             6. Years With This Type of Job<br>n\
//             7. Amount of Telecommute Days Per Week<br>n\
//             8. Employment Sector<br>n\
//             9. Job Title<br>n\
//             Change the factors around to see how your predicted salary will change!");
// }

var coll = document.getElementsByClassName("collapsible");
var i;

// makes form collapsable
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