 var MATRIX_CATMULL_ROM = [
 	[-1.0/2.0,  3.0/2.0, -3.0/2.0,  1.0/2.0],
 	[ 2.0/2.0, -5.0/2.0,  4.0/2.0, -1.0/2.0],
 	[-1.0/2.0,  0.0/2.0,  1.0/2.0,  0.0/2.0],
 	[ 0.0/2.0,  2.0/2.0,  0.0/2.0,  0.0/2.0]
 ]; 

 var DEF_SUBDIVISION = 1.0;

function smoothTheWay(points, callBack, subdivision) {
	setTimeout(function() {
		if(points.length < 4) return points;
		if(subdivision == null || subdivision <= 0) subdivision = DEF_SUBDIVISION;

		// Extra points
		var p1 = JSON.parse(JSON.stringify(points[0]))
		var p2 = JSON.parse(JSON.stringify(points[points.length - 1]))
		//points.push(p1, 0);
		points.push(p2);

		var finalVector = [];

		// Getting number of curves
		// One curve for each 4 points
		var numOfCurves = points.length - 3;

		// Prepare the points
		var preparedPoints = [];
		for(var i = 0; i < points.length; i++) {
			point = points[i];
			preparedPoints.push( [point.lat, point.lng, point.alt] );
		}

		for(var i = 0; i < numOfCurves; i++) {
			
			var controlPoints = [
				preparedPoints[i + 0],
				preparedPoints[i + 1],
				preparedPoints[i + 2],
				preparedPoints[i + 3]
			];

			for(var j = 0; j <= subdivision; j++) {
				var u = (j * 1.0 / subdivision);

				point = getPointAt(u, controlPoints);

				finalVector.push({
					lat: point[0],
					lng: point[1],
					alt: point[2]
				});
			}
		}

		callBack(finalVector);

	}, 0); 
 
}

function getPointAt(u, controlPoints) {
	var ut = [[u*u*u , u*u, u, 1]];
	var M = MATRIX_CATMULL_ROM;
	var p = controlPoints;

	var res = multiplyMatrices(ut, M);
	var res = multiplyMatrices(res, p);

	return res[0];
}

function multiplyMatrices(a, b) {
	if(a.length == 0 || b.length == 0) return [[]];
	// Discovering size
	var width = b[0].length;
	var height = a.length;

	// Creating a new matrix to result
	var c = [];
	for(var i = 0; i < height; i++) {
		c.push(new Array(width));
		for(var j = 0; j < width; j++) {
			c[i][j] = 0;
		}
	}	

	// Multiplying matrices
	for(var i = 0; i < height; i++) {
		for(var j = 0; j < width; j++) {
			for(var k = 0; k < a[0].length; k++) {
				c[i][j] += a[i][k] * b[k][j];
			}	
		}
	}

	return c;
}
