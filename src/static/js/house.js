var house = {
  floors: [
    {
      name: "Basement",
      rooms: [
        {
          name: "Cinema Room",
          x: 0,
          y: 0,
          points: [
            [0.00, 0.78], [0.47, 0.78],
            [0.48, 0.68], [1.13, 0.00],
            [2.32, 0.00], [2.98, 0.68],
            [2.98, 0.78], [4.55, 0.78],
            [4.55, 4.17], [0.00, 4.17],
          ],
        },
        {
          name: "Study",
          x: 0,
          y: 4.17,
          width: 3.28,
          height: 2.77,
        },
        {
          name: "Cupboard",
          x: 3.28,
          y: 5.09,
          width: 0.63,
          height: 0.92,
        },
        {
          name: "Hall",
          x: 3.28,
          y: 4.17,
          points: [
            [0.00, 0.00], [1.27, 0.00],
            [1.27, 1.84], [0.64, 1.84],
            [0.64, 0.92], [0.00, 0.92],
          ]
        }
      ]
    },
    {
      name: "Ground",
      rooms: [
        {
          name: "Living Room",
          x: 0,
          y: 0,
          points: [
            [0.00, 0.78], [0.47, 0.78],
            [0.48, 0.68], [1.13, 0.00],
            [2.32, 0.00], [2.98, 0.68],
            [2.98, 0.78], [3.33, 0.78],
            [3.33, 4.17], [0.00, 4.17],
          ]
        },
        {
          name: "Dining Room",
          x: 0,
          y: 4.17,
          width: 3.28,
          height: 2.77,
        },
        {
          name: "Hall",
          x: 3.28,
          y: 0.78,
          points: [
            [0.05, 0.00], [1.18, 0.00],
            [1.18, 6.16], [0.00, 6.15],
            [0.00, 3.39], [0.05, 3.39],
          ]
        },
        {
          name: "Kitchen",
          x: 1.93,
          y: 6.94,
          width: 2.62,
          height: 5.79,
        }
      ]
    },
    /*{
      "name": "First",
      "rooms": [
        {
          "name": "Master Bedroom",
          "x": 0,
          "y": 0,
          "points": [
            [0.00, 0.78], [0.47, 0.78],
            [0.48, 0.68], [1.13, 0.00],
            [2.32, 0.00], [2.98, 0.68],
            [2.98, 0.78], [3.33, 0.78],
            [3.33, 4.17], [0.00, 4.17],
          ]
        },
        {
          "name": "Family Bathroom",
          "x": 0,
          "y": 4.17,
          "width": 3.28,
          "height": 2.77,
        },
      ]
    }*/
  ]
};


var paper = Snap("#main_canvas");
console.log(paper);

function Flatten(lists) {
  var flattened = [];
  $.each(lists, function(i, l) {
    flattened.push(l[0]);
    flattened.push(l[1]);
  })
  return flattened;
}

function DrawFloor(i, floor) {
  floor.element = paper.group();
  house.element.add(floor.element);

  $.each(floor.rooms, function (j, room) {
    if ("points" in room) {
      room.element = paper.polygon(
        Flatten(room.points));
    } else {
      room.element =  paper.rect(
        0, 0, room.width, room.height);
    }
    floor.element.add(room.element);

    room.element
      .transform(sprintf("t%f,%f",
                         room.x, room.y))
      .attr({
        stroke: "#000",
        strokeWidth: 0.05,
        fill: "#FFF"
      });
  });

  var trans = sprintf("rotateX(20) skewX(-35)  translate(%d,%d)", -2*i, -2*i);
  floor.element.transform(trans);
  //floor.element.attr("style", "-webkit-transform: translate3d(0, 0, 0)")
  console.log(trans);
}

house.element = paper.group();
$.each(house.floors, DrawFloor);
bb = house.element.getBBox();
paper.attr("viewBox", bb.vb);
