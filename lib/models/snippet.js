'use strict';

var mongoose = require('mongoose'),
  Schema = mongoose.Schema,
  ObjectId = Schema.Types.ObjectId;
    
/**
 * Snippet Schema
 */
var SnippetSchema = new Schema({
  docType: String,
  docSubtype: String,
  name: String,
  content: String,
  url_small: String,
  url_medium: String,
  url_large: String,
  source: String,
  sourceId: String,
  title: String,
  date: Date,
  authors: String,
  publisher: String,
  sourceURL: String,
  resource_id: ObjectId,
  upvotes: Number,
  downvotes: Number,
  upvoting_users: [ObjectId],
  downvoting_users: [ObjectId]
});

mongoose.model('Snippet', SnippetSchema, 'corpus');
