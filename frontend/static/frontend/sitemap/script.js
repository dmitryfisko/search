var margin = {
    top: 20,
    right: 120,
    bottom: 20,
    left: 120
},
width = 1366 - margin.right - margin.left,
height = 768 - margin.top - margin.bottom;

var root;
var nodes;
var node;
var nodeEnter;
var nodeExit;
var link;
var o;
var i = 0,
    duration = 750,
    rectW = 60,
    rectH = 30;
var tree;
var diagonal;
var svg;

// Toggle children on click.
click = function(d) {
    if (d.children) {
        d._children = d.children;
        d.children = null;
    } else {
        d.children = d._children;
        d._children = null;
    }
    update(d);
}

//Redraw for zoom
redraw = function() {
  //console.log("here", d3.event.translate, d3.event.scale);
  svg.attr("transform",
      "translate(" + d3.event.translate + ")"
      + " scale(" + d3.event.scale + ")");
}

update = function(source) {
    // Compute the new tree layout.
    nodes = tree.nodes(root).reverse(),
        links = tree.links(nodes);

    // Normalize for fixed-depth.
    nodes.forEach(function (d) {
        d.y = d.depth * 180;
    });

    // Update the nodes…
    node = svg.selectAll("g.node")
        .data(nodes, function (d) {
        return d.id || (d.id = ++i);
    });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
        .attr("class", "node")
        .attr("transform", function (d) {
        return "translate(" + source.x0 + "," + source.y0 + ")";
    })
        .on("click", click);

    nodeEnter.append("rect")
        .attr("width", rectW)
        .attr("height", rectH)
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .style("fill", function (d) {
        return d._children ? "lightsteelblue" : "#fff";
    });

    nodeEnter.append("text")
        .attr("x", rectW / 2)
        .attr("y", rectH / 2)
        .attr("dy", ".35em")
        .attr("text-anchor", "middle")
        .text(function (d) {
        return d.name;
    });

    // Transition nodes to their new position.
    nodeUpdate = node.transition()
        .duration(duration)
        .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
    });

    nodeUpdate.select("rect")
        .attr("width", rectW)
        .attr("height", rectH)
        .attr("stroke", "black")
        .attr("stroke-width", 1)
        .style("fill", function (d) {
        return d._children ? "lightsteelblue" : "#fff";
    });

    nodeUpdate.select("text")
        .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    nodeExit = node.exit().transition()
        .duration(duration)
        .attr("transform", function (d) {
        return "translate(" + source.x + "," + source.y + ")";
    })
        .remove();

    nodeExit.select("rect")
        .attr("width", rectW)
        .attr("height", rectH)
    //.attr("width", bbox.getBBox().width)""
    //.attr("height", bbox.getBBox().height)
    .attr("stroke", "black")
        .attr("stroke-width", 1);

    nodeExit.select("text");

    // Update the links…
    link = svg.selectAll("path.link")
        .data(links, function (d) {
        return d.target.id;
    });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
        .attr("class", "link")
        .attr("x", rectW / 2)
        .attr("y", rectH / 2)
        .attr("d", function (d) {
        o = {
            x: source.x0,
            y: source.y0
        };
        return diagonal({
            source: o,
            target: o
        });
    });

    // Transition links to their new position.
    link.transition()
        .duration(duration)
        .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
        .duration(duration)
        .attr("d", function (d) {
        o = {
            x: source.x,
            y: source.y
        };
        return diagonal({
            source: o,
            target: o
        });
    })
        .remove();

    // Stash the old positions for transition.
    nodes.forEach(function (d) {
        d.x0 = d.x;
        d.y0 = d.y;
    });
}

function drawMap(jobject)  {
    root = jobject;

    tree = d3.layout.tree().nodeSize([70, 40]);
    diagonal = d3.svg.diagonal()
        .projection(function (d) {
        return [d.x + rectW / 2, d.y + rectH / 2];
    });

    svg = d3.select("#map-body").append("svg").attr("width", 1366).attr("height", 768)
        .call(zm = d3.behavior.zoom().scaleExtent([1,3]).on("zoom", redraw)).append("g")
        .attr("transform", "translate(" + 350 + "," + 20 + ")");

    //necessary so that zoom knows where to zoom and unzoom from
    zm.translate([350, 20]);

    root.x0 = 0;
    root.y0 = height / 2;

    collapse = function(d) {
        if (d.children) {
            d._children = d.children;
            d._children.forEach(collapse);
            d.children = null;
        }
    }

    root.children.forEach(collapse);
    update(root);

    d3.select("#map-body").style("height", "768px");
}


function onButtonClick() {
    url = $('#sitemap-input').val();
    if (url.length === 0) {
        return;
    }
    var statusCode;
    $.get('/api/map?url=' + url, function(data, status) {
        json_object = data;
        statusCode = status;
        // $('#sitemap-form').empty();
        drawMap(json_object);

        //get svg element.
        var svg = d3.select("#map-body svg g")[0][0];

        //get svg source.
        var serializer = new XMLSerializer();
        var source = serializer.serializeToString(svg);

        //add name spaces.
        if(!source.match(/^<svg[^>]+xmlns="http\:\/\/www\.w3\.org\/2000\/svg"/)){
            source = source.replace(/^<svg/, '<svg xmlns="http://www.w3.org/2000/svg"');
        }
        if(!source.match(/^<svg[^>]+"http\:\/\/www\.w3\.org\/1999\/xlink"/)){
            source = source.replace(/^<svg/, '<svg xmlns:xlink="http://www.w3.org/1999/xlink"');
        }

        //add xml declaration
        source = '<?xml version="1.0" standalone="no"?>\r\n' + source;

        //convert svg source to URI data scheme.
        var url = "data:image/svg+xml;charset=utf-8,"+encodeURIComponent(source);

        //set url value to a element's href attribute.
        $("#link").href = url;
        //you can download svg file by right click menu.

        btn = d3.select("#save")[0];
        console.log(btn);
        btn.onclick = function(){
            var html = d3.select("svg")
                .attr("version", 1.1)
                .attr("xmlns", "http://www.w3.org/2000/svg")
                .node().parentNode.innerHTML;

            //console.log(html);
            var imgsrc = 'data:image/svg+xml;base64,'+ btoa(html);
            var img = '<img src="'+imgsrc+'">';
            d3.select("#svgdataurl")[0].html(img);


            var canvas = document.querySelector("canvas"),
              context = canvas.getContext("2d");

            var image = new Image;
            image.src = imgsrc;
            image.onload = function() {
              context.drawImage(image, 0, 0);

              var canvasdata = canvas.toDataURL("image/png");

              var pngimg = '<img src="'+canvasdata+'">';
            	  d3.select("#pngdataurl")[0].html(pngimg);

              var a = document.createElement("a");
              a.download = "sample.png";
              a.href = canvasdata;
                  document.body.appendChild(a);
              a.click();
            };

        };

    });
    if (statusCode == 400) {
        return;
    }
}
