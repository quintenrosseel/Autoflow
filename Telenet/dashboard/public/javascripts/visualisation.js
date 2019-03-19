var $ = require('jquery');
var d3 = require('d3');



module.exports = function visualisation() {

/*    var n = 5;

    var nodes = d3.range(n * n).map(function(i) {
        return {
            index: i
        };
    });*/

// Auto Link generation
    //var links = [];
    //for (var y = 0; y < n; ++y) {
    //    for (var x = 0; x < n; ++x) {
    //        if (y > 0) links.push({source: (y - 1) * n + x, target: y * n + x});
    //        if (x > 0) links.push({source: y * n + (x - 1), target: y * n + x});
    //    }
    //}


    var nodes = [
        {"id": 1, "r": 3},
        {"id": 2, "r": 3},
        {"id": 3, "r": 3},
        {"id": 4, "r": 3},
        {"id": 5, "r": 3},
        {"id": 6, "r": 3},
        {"id": 7, "r": 3}];

    var links = [
        {"source": 1, "target": 2},
        {"source": 2, "target": 3},
        {"source": 3, "target": 4},
        {"source": 4, "target": 5},
        {"source": 5, "target": 6},
        {"source": 0, "target": 1}];

    var simulation = d3.forceSimulation(nodes)
        .force("charge", d3.forceManyBody().strength(-30))
        .force("link", d3.forceLink(links).strength(1).distance(20).iterations(10))
        .on("tick", ticked);

    var canvas = document.querySelector("canvas"),
        context = canvas.getContext("2d"),
        width = canvas.width,
        height = canvas.height;

    d3.select(canvas)
        .call(d3.drag()
            .container(canvas)
            .subject(dragsubject)
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    function ticked() {
        context.clearRect(0, 0, width, height);
        context.save();
        context.translate(width / 2, height / 2);

        context.beginPath();
        links.forEach(drawLink);
        context.strokeStyle = "#aaa";
        context.stroke();


        context.fillStyle = "#fff";
        context.beginPath();
        nodes.forEach(drawNode);
        context.closePath();
        context.fill();
        //context.strokeStyle = "#fff";
        //context.stroke();

        context.restore();
    }


    function dragsubject() {
        return simulation.find(d3.event.x - width / 2, d3.event.y - height / 2);
    }

    function dragstarted() {
        if (!d3.event.active) simulation.alphaTarget(0.3).restart();
        d3.event.subject.fx = d3.event.subject.x;
        d3.event.subject.fy = d3.event.subject.y;
    }

    function dragged() {
        d3.event.subject.fx = d3.event.x;
        d3.event.subject.fy = d3.event.y;
    }

    function dragended() {
        if (!d3.event.active) simulation.alphaTarget(0);
        d3.event.subject.fx = null;
        d3.event.subject.fy = null;
    }

    function drawLink(d) {
        context.moveTo(d.source.x, d.source.y);
        context.lineTo(d.target.x, d.target.y);
    }


   function updateRadius(d, r) {
        d.r = r;
   }

    function drawNode(d) {
        context.moveTo(d.x + 3, d.y);
        context.arc(d.x, d.y, d.r, 0, 2 * Math.PI);
    }


    function interpolateTo(node, r) {
        var curNodeR = node.r;
        if(r < curNodeR) {
            for (i = 0; r < cars.length; i++) {

            }
        } else if (r > curNodeR) {

        }
    }

    var start = 3;

    // Establish Socket.io connection:
    var socket = io.connect('http://localhost:3000');

    socket.on('updateGraph', function(data) {
        var node = nodes[0];
        updateRadius(node, start);
        ticked();

        start = start + 3;
    });

    // Set canvas resolution
    context.scale(1.8,1.8);
};