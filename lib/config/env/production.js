'use strict';

module.exports = {  
  env: 'production',  
  ip:   process.env.IP ||
        '0.0.0.0',  
  port: process.env.PORT ||
        8080,  
  mongo: {
    uri: process.env.MONGOLAB_URI ||
         'mongodb://localhost:27017/radsquared-dev'
  },
  facebook: {
    clientID: process.env.FACEBOOK_CLIENT_ID,
    clientSecret: process.env.FACEBOOK_CLIENT_SECRET,
    callbackURL: "http://www.radsquared.com/auth/facebook/callback"
  },
  twitter: {
    clientID: process.env.TWITTER_CLIENT_ID,
    clientSecret: process.env.TWITTER_CLIENT_SECRET,
    callbackURL: "http://www.radsquared.com/auth/twitter/callback"
  },
  google: {
    clientID: process.env.GOOGLE_CLIENT_ID,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET,
    callbackURL: "http://www.radsquared.com/auth/google/callback"
  }
};