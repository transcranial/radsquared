'use strict';

var mongoose = require('mongoose'),
  Schema = mongoose.Schema,
  ObjectId = Schema.Types.ObjectId;
    
/**
 * Query Schema
 */
var QuerySchema = new Schema({
  query: String,
  submittingUser: ObjectId,
  dateSubmitted: Date
});

mongoose.model('Query', QuerySchema, 'queries');
