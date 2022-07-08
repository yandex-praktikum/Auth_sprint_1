import React, {useEffect} from 'react';
import { Route, Routes, Navigate, useNavigate } from 'react-router-dom';
import {CurrentUserContext} from '../../contexts/CurrentUserContext';
import Header from '../Header/Header';
import Main from '../Main/Main';
import Footer from '../Footer/Footer';
import Register from '../Register/Register';
import Login from '../Login/Login';
import Profile from '../Profile/Profile';
import SavedMovies from '../SavedMovies/SavedMovies';
import Movies from '../Movies/Movies';
import Error404 from '../Error404/Error404';
import ProtectedRoute from '../../components/ProtectedRoute/ProtectedRoute';
import movies_api from '../../utils/MoviesApi'
import auth_api from '../../utils/MainApi'

function App() {
  
  const [currentUser, setCurrentUser] = React.useState({});
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [errorFromServer, setErrorFromServer] = React.useState('');
  const [jwt, setJwt] = React.useState(localStorage.getItem('jwt'))
  const [moviesData, setMoviesData] = React.useState([]);
  const [userMovies, setUserMovies] = React.useState({});

  const navigate = useNavigate();

  useEffect(() => {
    setErrorFromServer("");
    if (jwt) {
      auth_api.getUser(jwt) 
        .then((result) => {
          setCurrentUser({name: result.name, email: result.email})
          getUserMovies(jwt);
          loadMovieFromServer();
          setIsLoggedIn(true);
          localStorage.setItem('isLoggedIn', true);
        })
        .catch((err) => {
          setIsLoggedIn(false);
          localStorage.setItem('isLoggedIn', false);
          console.log(err);
          setErrorFromServer(`Error: ${err.status}`);
        })
      }
   }, []);

  function loadMovieFromServer() {
    movies_api.getAllMovies()
        .then((movies) => {
          setMoviesData(movies);
          localStorage.setItem('allMovies', JSON.stringify(movies));
        })
        .catch((err) => {
          setErrorFromServer("Во время запроса произошла ошибка. Возможно, проблема с соединением или сервер недоступен. Подождите немного и попробуйте ещё раз");
        });
  }

  function handleSearchSubmit(query, searchShortFilms) {
    localStorage.setItem("query", JSON.stringify(query));
    localStorage.setItem("searchShortFilms", JSON.stringify(searchShortFilms));    
    if (!localStorage.getItem('allMovies')) {
      loadMovieFromServer();
    }
    return JSON.parse(localStorage.getItem('allMovies'));
  }
  

  function handleLogin(data) {
    auth_api.login(data) 
    .then((result) => {
      localStorage.setItem('jwt', result.data.token);
      setJwt(localStorage.getItem("jwt"));
      auth_api.getUser(result.data.token) 
        .then((user) => {
          setCurrentUser({name: user.name, email: user.email})
          setIsLoggedIn(true);
          localStorage.setItem('isLoggedIn', true);
          loadMovieFromServer();
          getUserMovies(result.data.token);
          navigate("/movies");
        })
        .catch((err) => {
          console.log(`Error: ${err.status}`);
          setErrorFromServer(`Error: ${err.status}`);
        });
    })
    .catch((err) => {
      if (err.status === 400) {
        console.log(`не передано одно из полей`);
        setErrorFromServer(`не передано одно из полей`);
      } else if (err.status === 401) {
        console.log(`пользователь с email не найден`);
        setErrorFromServer(`пользователь с email не найден`);
      } else {
        console.log(`Error: ${err.status}`);
        setErrorFromServer(`Error: ${err.status}`);
      }
    }); 
  }

  function getUserMovies(jwt) {
    auth_api.getMovies(jwt)
    .then((result) => {
      setUserMovies(function() {
          const movies = {};
          for (const key in result.data) {
            movies[result.data[key].movieId] = result.data[key]._id;
          }
          return movies;
        })
    })
    .catch((err) => {
      console.log(`Error: ${err.status}`);
      setErrorFromServer(`Ошибка на сервере`);
    })
  }

  function handleSignup(data) {
    auth_api.register(data) 
    .then((result) => {
      handleLogin(data);
    })
    .catch((err) => {
      if (err.status === 409) {
        console.log(`Пользователь существует`);
        setErrorFromServer(`Пользователь существует`);
      } else {
        console.log(`Error: ${err.status}`);
        setErrorFromServer(`Ошибка на сервере`);
      }
    });  
  }

  function handleProfileEdit(data) {
      auth_api.editUser(jwt, data)
      .then((result) => {
        setCurrentUser({name: data.name, email: data.email});
        setErrorFromServer('Изменения прошли успешно!');
        }
      )
      .catch((err) => {
        console.log(err);
        setErrorFromServer(`Error: ${err.status}`);
      })
  }

  function handleMovieSave(data) {
    auth_api.addMovie(jwt, data)
      .then((res) => {
        setUserMovies((userMovies) => ({...userMovies, [data.id]: res._id}))
      })
      .catch((err) => {
        console.log(`Error: ${err.status}`);
        setErrorFromServer(`Error: ${err.status}`);
      })
  }
  
  function handleMovieRemove(id) {
    const movieId = userMovies[id];
    auth_api.deleteMovie(jwt, movieId)
    .then((res) => {
      setUserMovies((userMovies) => {
        const state = {...userMovies};
        delete state[id];
        return state;
      })
    })
    .catch((err) => {
      console.log(`Error: ${err.status}`);
      setErrorFromServer(`Error: ${err.status}`);
    })
  }

  function handleLogout() {
    auth_api.logout(jwt)
    .then((res) => {
      localStorage.removeItem('isLoggedIn');
      localStorage.removeItem('jwt');
      localStorage.removeItem('searchQuery');
      localStorage.removeItem('filterShortFilms');
      localStorage.removeItem('allMovies');
      setUserMovies({});
      setIsLoggedIn(false);
      navigate("/");
    })
    .catch((err) => {
      console.log(`Error: ${err.status}`);
      setErrorFromServer(`Error: ${err.status}`);
    });
  }

  return (
    <CurrentUserContext.Provider value={{currentUser}}>
      
        <Routes>  
            <Route exact path="/movies" element={
              <ProtectedRoute>
                  <Header onLogout={handleLogout} isLogined={isLoggedIn} dark={false} parent="/movies"/>
                  <Movies 
                    handleSearchSubmit={handleSearchSubmit}
                    moviesData={moviesData}
                    userMovies={userMovies}
                    handleMovieRemove={handleMovieRemove}
                    handleMovieSave={handleMovieSave}
                    errorFromServer={errorFromServer}
                    setErrorFromServer={setErrorFromServer}
                  />
                  <Footer />
                </ProtectedRoute>
            } />
            <Route exact path="/saved-movies" element={
              <ProtectedRoute>
                <Header onLogout={handleLogout} isLogined={isLoggedIn} dark={false} parent="/saved-movies"/>
                <SavedMovies 
                  handleSearchSubmit={handleSearchSubmit}
                  moviesData={moviesData}
                  userMovies={userMovies}
                  handleMovieRemove={handleMovieRemove}
                  errorFromServer={errorFromServer}
                  setErrorFromServer={setErrorFromServer}
                  loadMovieFromServer={loadMovieFromServer}
                />
                <Footer />
                </ProtectedRoute>
            } />
            <Route exact path="/profile" element={
              <ProtectedRoute>
                <Header onLogout={handleLogout} isLogined={isLoggedIn} dark={false} />
                <Profile 
                  handleProfileEdit={handleProfileEdit}
                  isLoggedIn={isLoggedIn}
                  setCurrentUser={setCurrentUser}
                  setIsLoggedIn={setIsLoggedIn}
                  errorFromServer={errorFromServer}
                  setErrorFromServer={setErrorFromServer}
                  handleLogout={handleLogout}
                />
              </ProtectedRoute>
            } />
          
            <Route exact path="/signin" element={
              !isLoggedIn ?
                <Login 
                  handleSubmit={handleLogin}
                  errorFromServer={errorFromServer}
                  setErrorFromServer={setErrorFromServer}
                />
                :
                <Navigate to="/movies" />
            } />

            <Route exact path="/signup" element={
              !isLoggedIn ?
                <Register 
                handleSubmit={handleSignup}
                errorFromServer={errorFromServer}
                setErrorFromServer={setErrorFromServer}
                />
                :
                <Navigate to="/movies" />
            } />
            <Route exact path="/" element={
              <Navigate to="/signin" />
            } />
            <Route path="/signout" element={
              <Navigate to="/signin" />
            } />
            <Route exact path="/404" element={
              <Error404/>
            } />
            <Route exact path="*" element={
                <Error404 />
            } />  
            
        </Routes>
    </CurrentUserContext.Provider>
  );
}

export default App;
