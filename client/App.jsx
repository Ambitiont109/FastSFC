import $ from 'jquery';
import 'typeahead.js/dist/typeahead.jquery.js';
import Handlebars from 'handlebars/dist/handlebars.js';
import Bloodhound from 'typeahead.js/dist/bloodhound.js';
import { Component } from 'react';
import { hot } from 'react-hot-loader';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  componentDidMount() {
    this.$searchInput = $('.mt-input-search');
    this.jqueryRenderSearch();
  }

  jqueryRenderSearch() {
    const companies = new Bloodhound({
      datumTokenizer: Bloodhound.tokenizers.obj.whitespace(
        'short_name',
        'ticker'
      ),
      queryTokenizer: Bloodhound.tokenizers.whitespace,
      prefetch: '/static/json/companies.json',
      remote: {
        url: '/api/v1/company/?search=%QUERY&limit=5&format=json',
        wildcard: '%QUERY',
        filter(res) {
          return res.results;
        },
      },
      sufficient: 5,
      identify(obj) {
        return obj.ticker;
      },
    });

    // search autocomplete
    this.$searchInput
      .typeahead(
        {
          hint: true,
          highlight: true,
          minLength: 1,
        },
        {
          name: 'companies',
          displayKey: 'ticker',
          source: companies,
          limit: 10,
          templates: {
            empty: '<div class="empty-message">Nothing found</div>',
            suggestion: Handlebars.compile(
              '<a href="/company/{{ticker}}"><span class="suggestion"><strong>{{ticker}}</strong> – {{short_name}}</span></a>'
            ),
          },
        }
      )
      .on('typeahead:select', (e, selected) => {
        window.location = '/company/' + selected.ticker;
      });

    // redirect to URL when complete
    $('.query-form').submit(e => {
      e.preventDefault();
      window.location = '/search?q=' + this.$searchInput.val();
    });
  }

  render() {
    return null;
  }
}

export default hot(module)(App);
