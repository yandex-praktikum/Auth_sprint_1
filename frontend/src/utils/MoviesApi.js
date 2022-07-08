class MoviesApi {

    constructor(options) {
      this._baseUrl = options.baseUrl;
      this._headers = {
        'Content-Type': options.headers['Content-Type']
      };
    }

    getAllMovies() {
      return fetch(`${this._baseUrl}`, {
        headers: this._headers
      })
      .then(this._checkResponse);
    }

    _checkResponse(res) {
      if (res.ok) {
        return res.json();
      }
      return Promise.reject(`Error: ${res.status}`);
    }
  }

  const movies_api = new MoviesApi({
    baseUrl: 'https://api.nomoreparties.co/beatfilm-movies',
    headers: {
      'Content-Type': 'application/json'
    }
  });

  export default movies_api;