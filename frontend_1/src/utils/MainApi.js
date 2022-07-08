class AuthApi {

    constructor(options) {
      this._authUrl = options.auth_baseUrl
      this._baseUrl = options.baseUrl;
      this._baseUrlForImages = options.baseUrlForImages;
      this._headers = {
        'Content-Type': options.headers['Content-Type'],
      };
    }

    login(data) {
        return fetch(`${this._authUrl}login`, {
            method: 'POST',
            headers: this._headers,
            body: JSON.stringify({
                login: data.email,
                password: data.password
            })
          })
        .then(this._checkResponse);
    }

    register(data) {
        return fetch(`${this._authUrl}signup`, {
            method: 'POST',
            headers: this._headers,
            body: JSON.stringify({
                name: data.name,
                login: data.email,
                email: data.email,
                password: data.password
            })
        })
        .then(this._checkResponse);
    }

    logout(jwt) {
      return fetch(`${this._authUrl}logout`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
            'Authorization' : `Bearer ${jwt}`
        }
      })
      .then(this._checkResponse);
    }

    getUser(jwt) {
        return fetch(`${this._baseUrl}users/me`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${jwt}`
            }
          })
          .then(this._checkResponse);
    }

    editUser(jwt, data) {
        return fetch(`${this._baseUrl}users/me`, {
            method: 'PATCH',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${jwt}`
            },
            body: JSON.stringify({
                name: data.name,
                email: data.email,
            })
          })
          .then(this._checkResponse);
    }

    deleteUser(jwt) {
        return fetch(`${this._baseUrl}users/me`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${jwt}`
            }
          })
          .then(this._checkResponse);
    }

    getMovies(jwt) {
        return fetch(`${this._baseUrl}movies`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${jwt}`
            }
          })
          .then(this._checkResponse);
    }

    addMovie(jwt, data) {
        return fetch(`${this._baseUrl}movies`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${jwt}`
            },
            body: JSON.stringify({
                country: data.country,
                director: data.director,
                duration: data.duration, 
                year: data.year,
                description: data.description,
                nameRU: data.nameRU,
                nameEN: data.nameEN,
                image: this._baseUrlForImages + data.image.url,
                thumbnail: this._baseUrlForImages + data.image.formats.thumbnail.url, 
                trailer: data.trailerLink,
                movieId: data.id,
            })
          })
          .then(this._checkResponse);
    }

  

    deleteMovie(jwt, id) {
        return fetch(`${this._baseUrl}movies/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'Authorization' : `Bearer ${jwt}`
            }
          })
          .then(this._checkResponse);
    }
    
    _checkResponse(res) {
        if (res.ok) {
            return res.json();
        }
        return Promise.reject(res);
    }
}

const auth_api = new AuthApi({
    auth_baseUrl: 'http://localhost/api/v1/',
    baseUrl: 'https://api.smotrelka.nomoredomains.work/',
    baseUrlForImages: 'https://api.nomoreparties.co',
    headers: {
        'Content-Type': 'application/json',
    }
});

export default auth_api;