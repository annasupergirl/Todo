angular.module('app', ['ngRoute'])
	.config(function($routeProvider) {
		$routeProvider
    		.when('/', {
     			controller:'TodoCtrl as myCtrl',
    			templateUrl:'todo.html'
    		})
    		.when('/edit/:taskId', {
    			controller:'UpdateCtrl',
    			templateUrl:'update.html'
    		})
    		.otherwise({
				redirectTo: '/'
			});
	})

    .controller('TodoCtrl', function($http) {
    	const todoList = this;

    	todoList.showlist = function() {
    		$http({
        		method: 'GET',
        		url: '/todo'
			}).then(function(response) {
        		todoList.tasks = response.data;
    		}, function(error) {
        		console.log(error);
    		});
		},

		todoList.showlist();

    	todoList.addTask = function() {
            $http({
                method: 'POST',
                url: '/todo',
                data: {
                    task: todoList.title,
                    done: false
                },
                headers: {'Content-Type': 'application/json'}
            }).then(function(response) {
            	todoList.title = '';
            }, function(error) {
                console.log(error);
            });

            todoList.showlist();
        },

		todoList.deleteTask = function(id) {
			$http({
        		method: 'DELETE',
        		url: '/todo/' + id
			}).then(function(response) {
				console.log(response);
    		}, function(error) {
        		console.log(error);
    		});

    		todoList.showlist();
		}
    })

    .controller('UpdateCtrl', function() {
    	console.log(123);
    	/* const update = this;
    	const taskId = $routeParams.taskId;

    	update.getTask = function(id) {
    		console.log(id);

    		$http({
        		method: 'GET',
        		url: '/todo/' + id
			}).then(function(response) {
				console.log(update.task);
        		update.task = response.data;
    		}, function(error) {
        		console.log(error);
    		});
    	},

    	update.getTask(taskId);

    	update.updateTask = function(id) {
			$http({
        		method: 'PUT',
        		url: '/todo/' + id,
        		data: {
                    task: update.title
                }
			}).then(function(response) {
				console.log(response.data);
				// $scope.ServerResponse = data;
        		// $scope.tasks = response.data;
    		}, function(error) {
        		console.log(error);
    		});
		}*/
    })
