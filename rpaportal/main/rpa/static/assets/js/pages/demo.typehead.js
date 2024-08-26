function initializeTypeahead(jsonDataArray, pkid) {
  var filmsData = jsonDataArray;
  var filmsBloodhound = new Bloodhound({
    datumTokenizer: Bloodhound.tokenizers.obj.whitespace("value"),
    queryTokenizer: Bloodhound.tokenizers.whitespace,
    local: filmsData
  });

  $('#custom' + pkid).typeahead(null, {
    name: 'best-pictures',
    display: 'value',
    source: filmsBloodhound,
    templates: {
      empty: [
        '<div class="typeahead-empty-message">',
        "조회 내역 없음",
        '</div>'
      ].join('\n'), // Make sure to close the div here
      suggestion: Handlebars.compile('<div title={{EMAIL}}><strong>{{value}}</strong> | {{CLNM}}</div>')
    }
  });
}
