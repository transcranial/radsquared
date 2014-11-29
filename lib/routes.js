'use strict';

var api = require('./controllers/api'),
    index = require('./controllers'),
    users = require('./controllers/users'),
    session = require('./controllers/session'),
    middleware = require('./middleware');

/**
 * Application routes
 */
module.exports = function(app, passport) {

  // Server API Routes
  app.route('/api/fetchRelevant')
    .post(api.fetchRelevant);
  app.route('/api/getSnippetByIds')
    .post(api.getSnippetByIds);
  app.route('/api/upvoteSnippet')
    .post(api.upvoteSnippet);
  app.route('/api/downvoteSnippet')
    .post(api.downvoteSnippet);
  app.route('/api/getUpvotedIds')
    .post(api.getUpvotedIds);
  app.route('/api/getDownvotedIds')
    .post(api.getDownvotedIds);
  app.route('/api/saveQuery')
    .post(api.saveQuery);
  app.route('/api/getUserQueries/:id')
    .get(api.getUserQueries);
  
  app.route('/api/users')
    .post(users.create)
    .put(users.changePassword);
  app.route('/api/users/me')
    .get(users.me);
  app.route('/api/users/:id')
    .get(users.show);

  app.route('/api/session')
    .post(session.login)
    .delete(session.logout);

  // All undefined api routes should return a 404
  app.route('/api/*')
    .get(function (req, res) {
      res.send(404);
    });



  // Setting the facebook oauth routes
  app.get('/auth/facebook', passport.authenticate('facebook', {
      scope: ['email', 'user_about_me'],
      failureRedirect: '/login'
  }), function (req, res) {
    res.redirect('/login');
  });

  app.get('/auth/facebook/callback', passport.authenticate('facebook', {
      failureRedirect: '/login'
  }), function (req, res) {
    res.redirect('/');
  });

  // Setting the twitter oauth routes
  app.get('/auth/twitter', passport.authenticate('twitter', {
      failureRedirect: '/login'
  }), function (req, res) {
    res.redirect('/login');
  });

  app.get('/auth/twitter/callback', passport.authenticate('twitter', {
      failureRedirect: '/login'
  }), function (req, res) {
    res.redirect('/');
  });

  // Setting the google oauth routes
app.get('/auth/google',
  passport.authenticate('google', { scope: ['https://www.googleapis.com/auth/userinfo.profile',
                                            'https://www.googleapis.com/auth/userinfo.email'] }),
  function(req, res){
  });

app.get('/auth/google/callback', 
  passport.authenticate('google', { failureRedirect: '/login' }),
  function(req, res) {
    res.redirect('/');
  });



  // All other routes to use Angular routing in app/scripts/app.js
  app.route('/partials/*')
    .get(index.partials);
  app.route('/*')
    .get( middleware.setUserCookie, index.index);


};