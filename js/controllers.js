'use strict';

myApp.controller("Menu" ,function ($scope,$location,$window,ngNotify) 
{
	$scope.username="";
	$scope.chosen="";

	$scope.processStep1 = function()
	{
		$window.userName=$scope.username;
		if ($scope.chosen=="pub")
			$location.path("/publisher");
		else if ($scope.chosen=="sub")
			$location.path("/subscriber");
		else
			$location.path("/");

	};
    $scope.pubBtnClicked = function ()
    {
    	$scope.chosen="pub";
    };

    $scope.subBtnClicked= function ()
    {
    	$scope.chosen="sub";
    };

});

myApp.controller("Publisher" ,function ($scope,$window,$location,ngNotify) 
{
    $scope.addedChannelName="";
    $scope.removedChannelName="";
    $scope.publishChannel="";
    $scope.newEmail="";
    $scope.userName=$window.userName;
    $scope.channelList=[];

    $scope.RemovePublishChannel = function()
    {
    	if (!$window.userName)
    		$location.path('/');
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/pubRemoveChannel?username='+$window.userName+'&channel='+$scope.removedChannelName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    ngNotify.set("channel removed successfully");
                    var index=$scope.channelList.indexOf($scope.removedChannelName);
                    $scope.channelList.splice(index,1);
                }
                else
                {
                    ngNotify.set("error occured while removing channel");
                }
                $scope.removedChannelName="";
                $scope.$apply();
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                ngNotify.set("error occured while removing channel");
                $scope.removedChannelName="";
                $scope.$apply();
            },
        });

    };

    $scope.AddPublishChannel = function()
    {
        if (!$window.userName)
            $location.path('/');
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/pubAddChannel?username='+$window.userName+'&channel='+$scope.addedChannelName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    ngNotify.set("channel added successfully");
                    $scope.channelList.push($scope.addedChannelName);
                }
                else
                {
                    ngNotify.set("error occured while adding channel");
                }
                $scope.addedChannelName="";
                $scope.$apply();
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                ngNotify.set("error occured while adding channel");
                $scope.addedChannelName="";
                $scope.$apply();
            },
        });

    };


    $scope.ChangeEmail = function()
    {
        ngNotify.set($scope.newEmail);
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/changePubEmail?username='+$window.userName+'&email='+$scope.newEmail+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    ngNotify.set("email changed successfully");
                    $window.userName=$scope.newEmail;
                    $scope.userName=$window.userName;
                }
                else
                {
                    ngNotify.set("An error occured while changing email");
                }
                $scope.newEmail="";
                $scope.$apply();
                
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                ngNotify.set("An error occured while changing email");
                $scope.newEmail="";
                $scope.$apply();
            },
        });

    };

    $scope.pubChannelList = function()
    {
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/pubChannelList?username='+$window.userName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    for (var i=0;i<response.data.channels.length;i++)
                    {
                        $scope.channelList.push(response.data.channels[i]);
                    }
                    $scope.$apply();
                }
                else
                {
                    console.log("An error occured while getting channels");
                }
                
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                console.log("An error occured while getting channels");
            },
        });

    }
 
    $scope.PublishMessage = function()
    {
    	if (!$window.userName)
    	{
    		$location.path('/');
    	}

        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/pub?username='+$window.userName+'&channel='+$scope.publishChannel+'&message='+$scope.message+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) 
            {
                ngNotify.set(response);
                if (response.status)
                {
                    ngNotify.set("message published successfully");
                }
                else
                {
                    ngNotify.set("An error occured while publishing message");
                }
                $scope.publishChannel="";
                $scope.message="";
                $scope.$apply();
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                ngNotify.set("An error occured while publishing message");
                $scope.publishChannel="";
                $scope.message="";
                $scope.$apply();
            },
        });

    	
    }
    if (!$window.userName)
        $location.path('/');
    else
        $scope.pubChannelList()
    
});


myApp.controller("Subscriber" ,function ($scope,$window,$location,$timeout,ngNotify) 
{
	$scope.addedChannelName="";
    $scope.removedChannelName="";
    $scope.newEmail="";
    $scope.userName=$window.userName;
    $scope.messages=[];
    $scope.channelList=[];
    $scope.history=[];
	$scope.subscribeChannel = function()
    {

        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/subChannel?username='+$window.userName+'&channel='+$scope.addedChannelName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    ngNotify.set("successfully subscribed to the channel");
                    $scope.channelList.push($scope.addedChannelName);
                }
                else
                {
                    ngNotify.set("An error occured while subscribing the channel");
                }
                $scope.addedChannelName="";
                $scope.$apply();
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                $scope.addedChannelName="";
                $scope.$apply();
                ngNotify.set("An error occured while subscribing the channel");
            },
        });


    	
    	
    };


    $scope.unsubscribeChannel = function()
    {

        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/unsubChannel?username='+$window.userName+'&channel='+$scope.removedChannelName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    ngNotify.set("successfully unsubscribed to the channel");
                    var index = $scope.channelList.indexOf($scope.removedChannelName);
                    $scope.channelList.splice(index, 1);
                }
                else
                {
                    ngNotify.set("An error occured while unsubscribing the channel");
                }
                $scope.removedChannelName="";
                $scope.$apply();
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                $scope.removedChannelName="";
                $scope.$apply();
                ngNotify.set("An error occured while unsubscribing the channel");
            },
        });
  
    };


    $scope.ChangeEmail = function()
    {
        ngNotify.set($scope.newEmail);
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/changeSubEmail?username='+$window.userName+'&email='+$scope.newEmail+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
               
                if (response.status)
                {
                    $window.userName=$scope.newEmail;
                    $scope.userName=$window.userName;
                    ngNotify.set("email changed successfully");
                }
                else
                {
                    ngNotify.set("An error occured while changing email");
                }
                
                $scope.newEmail="";
                $scope.$apply();
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                ngNotify.set("An error occured while changing email");
                $scope.newEmail="";
                $scope.$apply();
            },
        });

    }

    $scope.subChannelList = function()
    {
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/subChannelList?username='+$window.userName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    for (var i=0;i<response.data.channels.length;i++)
                    {
                        $scope.channelList.push(response.data.channels[i]);
                    }
                    $scope.$apply();
                }
                else
                {
                    console.log("An error occured while getting channels");
                }
                
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                console.log("An error occured while getting channels");
            },
        });

    }


    $scope.getHistory = function()
    {
        $.ajax
        ({
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/getHistory?username='+$window.userName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // process a successful response
            success: function(response) {
                if (response.status)
                {
                    $scope.history=[];
                    for (var i=0;i<response.data.history.length;i++)
                    {
                        $scope.history.push(response.data.history[i]);
                    }
                    ngNotify.set("History Updated");
                    $scope.$apply();
                }
                else
                {
                    console.log("An error occured while getting history");
                }
                
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                console.log("An error occured while getting history");
            },
        });

    }


    $scope.longPoll = function() 
    {
        console.log("Long Polling Started");
        $.ajax(
        {
            type: "GET",
            // set the destination for the query
            url: 'http://172.27.30.175:8000/sub?user='+$window.userName+'&callback=?',
            // define JSONP because we're using a different port and/or domain
            dataType: 'jsonp',
            // needs to be set to true to avoid browser loading icons
            async: true,
            cache: false,
            // timeout after 5 minutes
            timeout:300000,
            // process a successful response
            success: function(response) {
                // append the message list with the new message
                if (response.status)
                {
                    for (var i=0;i<response.data.messages.length;i++)
                    {
                        $scope.messages.push(response.data.messages[i]);
                    }
                    console.log($scope.messages);
                    ngNotify.set("New Message");
                    $scope.$apply();
                }
                
                $timeout( function(){ $scope.longPoll(); }, 1000);
            },
            // handle error
            error: function(XMLHttpRequest, textStatus, errorThrown){
                // try again in 10 seconds if there was a request error
                console.log("error occured while long polling");
                $timeout( function(){ $scope.longPoll(); }, 1000);
            },
        });
    };

    if (!$window.userName)
        $location.path('/');
    else
    {
        $scope.longPoll();
        $scope.subChannelList();
    }
        



});
