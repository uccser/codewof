const Fuse = require('fuse.js');
var fuse;
var faq = [];
var faq_search_results;
var faq_all;

$(document).ready(function() {
  faq_search_results = $('#faq-search-results');
  faq_all = $('#faq-all');

  // Load FAQ into array
  load_faq();
  // Create fuse search function
  fuse = new Fuse(faq, {
    shouldSort: true,
    threshold: 0.6,
    location: 0,
    distance: 100,
    maxPatternLength: 32,
    minMatchCharLength: 1,
    keys: [
      'question',
      'answer'
    ]
  });
  // // Change on each input
  $('#faq-search').on('input', function(event){
    display_results(event.target.value);
  });
  // // Call display function on load
  display_results('');

  $('#clear-search').click(function() {
    $('#faq-search').val('');
    display_results('');
  });
});

function load_faq() {
  $('#faq-all .faq').each(function() {
    var item = {};
    item.question = $('h5', this).text().trim();
    item.answer = $('p', this).text().trim();
    item.html = $(this).html();
    faq.push(item);
  });
}

function display_results(query) {
  // Empty questions
  faq_search_results.empty();

  // If no query, show all QA's, otherwise filter by search
  if (query.length == 0) {
    faq_search_results.hide();
    faq_all.show();
  } else {
    faq_all.hide();
    faq_search_results.show();
    $.each(fuse.search(query), function(i, item) {
      faq_search_results.append($(item.html));
    });
  }
}
