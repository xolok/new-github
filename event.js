var events = require('events');
var util = require('util');

/*var myEmitter = new events.EventEmitter();

myEmitter.on('someEvent', function(mssg){
	console.log(mssg);

});

myEmitter.emit('someEvent','the event was emitted');
*/

var Person = function(name){
	this.name = name;
};

util.inherits(Person, events.EventEmitter);

var james = new Person('james');
var funny = new Person('funny');
var ryu = new Person('ryu');
var people = [james, funny, ryu];

people.forEach(function(person){
	person.on('speak', function(mssg){
		console.log(person.name + 'said: ' + mssg);

	});

});

james.emit('speak', 'hey dudes');
