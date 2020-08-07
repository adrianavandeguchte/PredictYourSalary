

country_url = "/salary_visuals_data/country_dataset1"

// d3.json(country_url).then((data) => {
d3.json(country_url, function (data) {
    function init() {
        // creates array of all names/ids
        var countries = data.country;
        // selects the dropdown menu
        var menu = d3.select("#selCountry");

        // adds the id of each test subject to the dropdown menu and adds the value as the same number
        for (var i = 0; i < countries.length; i++) {
            menu.append("option").text(countries[i]).property("value", names[i]);
        }
    }
    init();
});