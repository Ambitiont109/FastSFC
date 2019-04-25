import _ from 'lodash';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App.jsx';
import DocumentList from './components/DocumentList.jsx';
import DocumentDetail from './components/DocumentDetail.jsx';

if (document.getElementById('app') !== null) {
  ReactDOM.render(<App />, document.getElementById('app'));
}

if (document.getElementById('document-detail') !== null) {
  ReactDOM.render(
    <DocumentDetail type="document" />,
    document.getElementById('document-detail')
  );
}

if (document.getElementById('website-document-detail') !== null) {
  ReactDOM.render(
    <DocumentDetail type="websiteDocument" />,
    document.getElementById('website-document-detail')
  );
}

if (document.getElementById('document-financials-chrono-loader')) {
  ReactDOM.render(
    <DocumentList offset={20} limit={20} format="chronological" />,
    document.getElementById('document-financials-chrono-loader')
  );
}

// Render document loader for each type
const markets = ['hk', 'us'];

const types = [
  'financials',
  'announcements',
  'ownership',
  'prospectuses',
  'proxies',
  'other',
];

_.each(markets, market => {
  _.each(types, type => {
    const el = market + '-document-' + type + '-loader';
    const node = document.getElementById(el);
    const f = 'categorized';

    if (node !== null) {
      ReactDOM.render(
        <DocumentList type={type} offset={8} format={f} market={market} />,
        node
      );
    }
  });
});
