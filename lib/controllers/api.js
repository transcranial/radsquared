'use strict';

var mongoose = require('mongoose'),
  ObjectId = mongoose.Types.ObjectId,
  Snippet = mongoose.model('Snippet'),
  Query = mongoose.model('Query'),
  child_process = require('child_process'),
  fetchServerSpawn = require('../../nlp_engine/fetchServerSpawn');

/**
 * Get relevant snippets
 * Returns: list of ObjectId strings
 */
exports.fetchRelevant = function(req, res) {
  var x = fetchServerSpawn.getCurrentPort();
  console.log(x);
  var fetcher = child_process.spawn('python', [
    process.env.PWD + '/nlp_engine/fetchClient.py', 
    x,
    req.body.inputText, 
    req.body.limit
  ]);
  var data_stdout, data_stderr;
  fetcher.stdout.on('data', function (data) {
    data_stdout = data;
  });
  fetcher.stderr.on('data', function (err) {
    console.log(err);
  });
  return fetcher.on('exit', function (code) {
    if (data_stdout) {
      res.set('Content-Type', 'text/json');
      return res.send(200, data_stdout);
    } else {
      return res.send(500);
    }
  });
};

/**
 * Get relevant snippets
 * Returns: json object of snippets matching id
 */
exports.getSnippetByIds = function(req, res) {
  var idArray = req.body.idArray.map(function (idstr) {
    return new ObjectId(idstr);
  });
  return Snippet.find({'_id': {$in: idArray}}, '-upvoting_users -downvoting_users', function (err, snippets) {
    if (!err) {
      return res.json(snippets);
    } else {
      return res.send(500, err);
    }
  });
};

/**
 * Get upvoted snippet IDs for a user for a set of snippet IDs
 * Returns: subset of IDs that user upvoted
 */
exports.getUpvotedIds = function(req, res) {
  var idArray = req.body.idArray.map(function (idstr) {
    return new ObjectId(idstr);
  });
  return Snippet.find({'_id': {$in: idArray}, 'upvoting_users': {$in: [req.body.userId]}}, '_id', function (err, upvotedIds) {
    if (!err) {
      return res.json(upvotedIds);
    } else {
      return res.send(500, err);
    }
  });
};

/**
 * Get downvoted snippet IDs for a user for a set of snippet IDs
 * Returns: subset of IDs that user downvoted
 */
exports.getDownvotedIds = function(req, res) {
  var idArray = req.body.idArray.map(function (idstr) {
    return new ObjectId(idstr);
  });
  return Snippet.find({'_id': {$in: idArray}, 'downvoting_users': {$in: [req.body.userId]}}, '_id', function (err, downvotedIds) {
    if (!err) {
      return res.json(downvotedIds);
    } else {
      return res.send(500, err);
    }
  });
};

/**
 * Upvotes snippet
 */
exports.upvoteSnippet = function(req, res) {
  return Snippet.findByIdAndUpdate(req.body.docId, {$inc: {'upvotes': 1}, $addToSet: {'upvoting_users': new ObjectId(req.body.userId)}}, function (err) {
    if (!err) {
      return res.send(200);
    } else {
      return res.send(500, err);
    }
  });
};

/**
 * Downvotes snippet
 */
exports.downvoteSnippet = function(req, res) {
  return Snippet.findByIdAndUpdate(req.body.docId, {$inc: {'downvotes': 1}, $addToSet: {'downvoting_users': new ObjectId(req.body.userId)}}, function (err) {
    if (!err) {
      return res.send(200);
    } else {
      return res.send(500, err);
    }
  });
};

/**
 * Saves query
 */
exports.saveQuery = function(req, res) {
  return Query.findOne({'query': req.body.query, 'submittingUser': new ObjectId(req.body.userId)}, function(err, existingQuery) {
    if (existingQuery === null) {
      var query = new Query({'query': req.body.query, 'submittingUser': new ObjectId(req.body.userId), 'dateSubmitted': req.body.dateSubmitted});
      return query.save(function(err) {
        if (!err) {
          return res.send(200);
        } else {
          return res.send(500, err);
        }
      });
    } else {
      return Query.findByIdAndUpdate(existingQuery._id, {$set: {'dateSubmitted': Date.now()}}, function (err) {
        if (!err) {
          return res.send(200);
        } else {
          return res.send(500, err);
        }
      });
    }
  });
};

/**
 * Gets user's queries
 */
exports.getUserQueries = function(req, res) {
  var userId = req.params.id;
  return Query.find({'submittingUser': new ObjectId(userId)}, function(err, userQueries) {
    if (!err) {
      return res.json(200, userQueries);
    } else {
      return res.send(500, err);
    }
  });
};