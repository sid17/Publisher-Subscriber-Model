'use strict';

var myApp = angular.module('myApp',['ngRoute','ngNotify']);

myApp.config(function($routeProvider) {

    $routeProvider.when(
        '/', 
        {
            templateUrl: 'partials/menu.html', 
            controller: 'Menu'
        });

    $routeProvider.when(
    	'/subscriber', 
    	{
    		templateUrl: 'partials/subscriber.html', 
    		controller: 'Subscriber'
    	});
    $routeProvider.when(
    	'/publisher', 
    	{
    		templateUrl: 'partials/publisher.html', 
    		controller: 'Publisher'
    	});
    $routeProvider.otherwise(
        {
            redirectTo: '/'
        });
});
