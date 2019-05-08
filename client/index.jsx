import _ from 'lodash';
import React from 'react';
import ReactDOM from 'react-dom';
import DocumentList from './components/DocumentList.jsx';
import DocumentDetail from './components/DocumentDetail.jsx';
import Search from './components/Search';

const inputSearch = document.getElementById('input-search');
if (inputSearch !== null) {
  ReactDOM.render(<Search />, inputSearch);
}

const documentDetail = document.getElementById('document-detail');
if (documentDetail !== null) {
  ReactDOM.render(<DocumentDetail type="document" />, documentDetail);
}

const websiteDocumentDetail = document.getElementById(
  'website-document-detail'
);
if (websiteDocumentDetail !== null) {
  ReactDOM.render(
    <DocumentDetail type="websiteDocument" />,
    websiteDocumentDetail
  );
}

const documentFinancialChronoLoader = document.getElementById(
  'document-financials-chrono-loader'
);
if (documentFinancialChronoLoader !== null) {
  ReactDOM.render(
    <DocumentList offset={20} limit={20} format="chronological" />,
    documentFinancialChronoLoader
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
