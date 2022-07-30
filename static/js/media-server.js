'use strict';

const {createApp } = Vue;

createApp({
  compilerOptions: {
    delimiters: ['${', '}']
  },
  data() {
    return {
      searchReserveString: '',
      reservedConditions: [],
      reserveConditionsHeader: ['File path', 'folder'],
    };
  },
  methods: {
    searchReserveConditions(event) {
      if (event) {
        fetch('/v1/getMoviesInfo?q=' + this.searchReserveString)
          .then(resp => {
            if (resp.ok) {
              return Promise.resolve(resp.json());
            } else {
              return Promise.reject({});
            }
          })
          .then(json => {
            this.reservedConditions = json;
            return Promise.resolve(json);
          })
      }
    }
  }
}).mount('#video-files');

