'use strict';

module.exports = {
  env: 'development',
  mongo: {
    uri: 'mongodb://localhost:27017/radsquared-dev'
  },
  facebook: {
    clientID: process.env.FACEBOOK_CLIENT_ID || 'id',
    clientSecret: process.env.FACEBOOK_CLIENT_SECRET || 'secret',
    callbackURL: "http://localhost:9000/auth/facebook/callback"
  },
  twitter: {
    clientID: process.env.TWITTER_CLIENT_ID || 'id',
    clientSecret: process.env.TWITTER_CLIENT_SECRET || 'secret',
    callbackURL: "http://127.0.0.1:9000/auth/twitter/callback"
  },
  google: {
    clientID: process.env.GOOGLE_CLIENT_ID || 'id',
    clientSecret: process.env.GOOGLE_CLIENT_SECRET || 'secret',
    callbackURL: "http://localhost:9000/auth/google/callback"
  }
};