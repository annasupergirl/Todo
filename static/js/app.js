(function() {
    'use strict';

    angular.module('app', ['ngRoute'])
		.config(config)
		.controller('TodoCtrl', TodoCtrl)
		.controller('UpdateCtrl', UpdateCtrl);

	function config($routeProvider) {
		$routeProvider
    		.when('/', {
     			controller:'TodoCtrl',
     			controllerAs: 'todoVm',
	    		templateUrl:'static/views/todo.html'
    		})
			.when('/edit/:taskId', {
    			controller:'UpdateCtrl',
    			controllerAs: 'updateVm',
    			templateUrl:'static/views/update.html'
	   		})
    		.otherwise({
				redirectTo: '/'
			});
	}

    function TodoCtrl($http) {
    	var vm = this;

    	vm.showlist = showlist;
    	vm.addTask = addTask;
    	vm.deleteTask = deleteTask;

    	vm.showlist();

    	function showlist() {
			return $http.get('/todo')
				.then(function(response) { vm.tasks = response.data; })
        		.catch(function(error) { console.log(error); });
		}

    	function addTask() {
           	$http({
               	method: 'POST',
	            url: '/todo',
                data: {
        	        task: vm.title,
            	    done: false
                },
	            headers: {'Content-Type': 'application/json'}
    	    })
           	.then(function() { vm.title = ''; })
        	.catch(function(error) { console.log(error); });

            vm.showlist();
        }

		function deleteTask(id) {
			$http.delete('/todo/' + id)
				.then(function(response) { console.log(response); })
        		.catch(function(error) { console.log(error); });

    		vm.showlist();
		}
   	}

    function UpdateCtrl($http, $routeParams, $location) {
    	var vm = this,
    	    taskId = $routeParams.taskId;

    	vm.getTask = getTask;
    	vm.updateTask = updateTask;

    	vm.getTask(taskId);

	    function getTask(id) {
			return $http.get('/todo/' + id)
    			.then(function(response) { vm.task = response.data; })
        		.catch(function(error) { console.log(error); });
    	}

    	function updateTask(id) {
			return $http({
        		method: 'PATCH',
	       		url: '/todo/' + id,
        		data: {
       	            task: vm.task.title,
           	        done: vm.task.done
               	},
	            headers: {'Content-Type': 'application/json'}
			})
			.then(function() { $location.path('/'); })
        	.catch(function(error) { console.log(error); });
		}
    }
})();
